import nltk
import math
import re
import os
import urllib.request
from bs4 import BeautifulSoup
from collections import Counter

from nltk.corpus import stopwords


####    WORD FILTERING
BEST_WORDS = 10

#Returns list of reasonable words from html page
def get_html_words(url):
    page = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(page,"html.parser")
    for script in soup(["script","style"]):
        script.extract()

    text = soup.get_text()

    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split(" "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    text = re.sub("[^a-zA-Z]"," ",text)
    return text

#Common generic words that should not be considered
more_crap = get_html_words("http://www.wordfrequency.info/free.asp?s=y").lower().split()
more_crap = [w for w in more_crap if not w in stopwords.words("english")]
more_crap.extend(stopwords.words("english"))
more_crap.extend(["com","hours","minutes","seconds","org","ca","co","www","days","years"])

#Returns list of the top <BEST_WORDS> words in a given word set based on the amount of occurances
def get_decent_words(words):
    words = [w for w in words if not w in more_crap]
    word_counter = {}
    for word in words:
        if word in word_counter:
            word_counter[word] += 1
        else:
            word_counter[word] = 1
    popular_words = sorted(word_counter,key=word_counter.get, reverse = True)
    return popular_words[:BEST_WORDS]

#Returns dictionary of (word, amount of word occurances)
def get_word_count(words):
    word_counter = {}
    for word in words:
        if word in word_counter:
            word_counter[word] += 1
        else:
            word_counter[word] = 1
    return word_counter

#Returns list of words sorted by the amount of occurances
def get_popular_words(words):
    words = [w for w in words if not w in more_crap]
    word_counter = {}
    for word in words:
        if word in word_counter:
            word_counter[word] += 1
        else:
            word_counter[word] = 1
    popular_words = sorted(word_counter,key=word_counter.get, reverse = True)
    return popular_words
####    END WORD FILTERING


####    MATH
NUM_ITERS = 30      #Number of iterations of gradient descent
LEARNING_RATE = 0.8 #Sensitivity of learning
xs = []             #Stores the vectors describing websites in the training set
curwords = []       #Stores the current list of words that are encoded in the vectors in xs
theta = []          #Stores the weight values of each word
y = []              #Stores 1 if corresponding x site is enjoyed, 0 otherwise

#Dot product of integral vectors
def dot(u,v):
    total = 0
    while(len(u) < len(v)): u.append(0)
    while(len(v) < len(u)): v.append(0)
    for i in range(0,len(u)):
        total += u[i] * v[i]

    return total

#Subtraction of integral vectors
def sub(u,v):
    r = []
    for i in range(0,len(u)):
        r.append(u[i]-v[i])
    return r
####    END MATH

####    MACHINE LEARNING
#Logistic regression godfather
def sigmoid(x):
    if(x < -10): return 0
    return 1/(1 + math.exp(-x))

#Wrapper log function that doesn't crash on log(0)
def pseudolog(x):
    if(x <= 0): return -1000000000
    else: return math.log(x)

#Cost function corresponding to the current theta vector. Returns a lower number for better thetas.
def cost():
#    x = [[]]
#    for i in range(0,len(x)):
#        x.append(list(xs[i].values()))
    global xs
    global theta
    global y
    if len(y) == 0: return 0
    sum = 0
    for i in range(0,len(y)):
        sum += y[i] * pseudolog(sigmoid(dot(xs[i],theta))) + (1-y[i])*pseudolog(1-sigmoid(dot(xs[i],theta)))

    return (-1/len(y)) * sum

#Updates the theta values based on the gradient of the cost function
def modifyThetas():
    global theta
    dtheta = []

    for j in range (0,len(theta)):
        sum = 0
        for i in range(0,len(y)):
            sum += (sigmoid(dot(xs[i],theta)) - y[i]) * xs[i][j]
        dtheta.append((LEARNING_RATE/len(y))*sum)
    
    theta = sub(theta,dtheta)
    return theta

#Implements gradient descent optimization routine with up to <NUM_ITERATIONS> iterations
def gradientDescent():
    global theta
    for i in range(0,NUM_ITERS):
        if(cost() < 0.00000001): 
            print("Good enough")
            break
        print("Cost: " + str(cost()))
        theta = modifyThetas()
    print("===========")
####    END MACHINE LEARNING

#Returns vector corresponding to words in a given site
def morphToVector(url):
    x = []
    website = get_html_words(url).lower().split()
    wordcount = get_word_count(website)
    for i in range(0,len(curwords)):
        if(curwords[i] in website):
            x.append(wordcount[curwords[i]])
        else: x.append(0)
    return x

#Adds a website to the training set
def addWebsite(url,enjoyed):
    y.append(enjoyed)
    website = get_html_words(url).lower().split()
    popularwords = get_decent_words(website)
    newwords = [w for w in popularwords if not w in curwords]
    curwords.extend(newwords)
    wordcount = get_word_count(website)
    x = []
    for i in range(0,len(curwords)):
        if (curwords[i] in website): 
            x.append(wordcount[curwords[i]])
        else: x.append(0)

    xs.append(x)
    while(len(theta) < len(curwords)): theta.append(0)
    gradientDescent()

####    TESTS
addWebsite("http://www.archlinux.org",1)
addWebsite("http://www.vim.org",1)
addWebsite("http://programming.reddit.com",1)
addWebsite("https://www.gnu.org/s/emacs",0)
addWebsite("http://www.apple.com",0)

#print(curwords)
#print(theta)

tests = ["http://www.archlinux.org","https://www.gnu.org/s/emacs","http://www.mchacks.io","https://www.debian.org","http://www.python.ca","https://www.twitter.com/realDonaldTrump","https://feraligatr.tumblr.com","https://thingsprogrammersshout.tumblr.com","http://www.ratemypoo.com"]

for test in tests:
    x = morphToVector(test)
    odds = sigmoid(dot(theta,x))
    print("Odds of enjoying " + test + ": " + str(100 * odds) + "%")
