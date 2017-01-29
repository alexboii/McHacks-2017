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

more_crap = get_html_words("http://www.wordfrequency.info/free.asp?s=y").lower().split()
more_crap = [w for w in more_crap if not w in stopwords.words("english")]
more_crap.extend(stopwords.words("english"))

def get_decent_words(words):
#    words = words.lower().split()
    words = [w for w in words if not w in more_crap]
    word_counter = {}
    for word in words:
        if word in word_counter:
            word_counter[word] += 1
        else:
            word_counter[word] = 1
    popular_words = sorted(word_counter,key=word_counter.get, reverse = True)
    return popular_words[:BEST_WORDS]

def get_word_count(words):
    word_counter = {}
    for word in words:
        if word in word_counter:
            word_counter[word] += 1
        else:
            word_counter[word] = 1
    return word_counter

def get_popular_words(words):
#    words = words.lower().split()
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
NUM_ITERS = 30 #Number of iterations of gradient descent
LEARNING_RATE = 0.01
xs = []
curwords = []
theta = []
y = []

def dot(u,v):
    total = 0
    while(len(u) < len(v)): u.append(0)
    while(len(v) < len(u)): v.append(0)
    for i in range(0,len(u)):
        total += u[i] * v[i]

    return total

def sub(u,v):
    r = []
    for i in range(0,len(u)):
        r.append(u[i]-v[i])
    return r
####    END MATH

####    MACHINE LEARNING
def sigmoid(x):
    if(x < -10): return 0
    return 1/(1 + math.exp(-x))

def pseudolog(x):
    if(x <= 0): return -1000000000
    else: return math.log(x)

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

def modifyThetas():
#    x = [[]]
    global theta
    dtheta = []
#    for i in range(0,len(x)):
#        x.append(list(xs[i].values()))

    for j in range (0,len(theta)):
        sum = 0
        for i in range(0,len(y)):
            sum += (sigmoid(dot(xs[i],theta)) - y[i]) * xs[i][j]
#            print("xs[" + str(i) + "] = " + str(xs[i]))
        dtheta.append((LEARNING_RATE/len(y))*sum)
    
    theta = sub(theta,dtheta)
#    print("===========")
    return theta

def gradientDescent():
    global theta
    for i in range(0,NUM_ITERS):
        print("Cost: " + str(cost()))
#        print("Theta: " + str(theta))
        theta = modifyThetas()
    print("===========")
####    END MACHINE LEARNING

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
#            print(url + " has instance of " + curwords[i] + " " + str(wordcount[curwords[i]]) + " times.")
        else: x.append(0)

    xs.append(x)
    while(len(theta) < len(curwords)): theta.append(0)
    gradientDescent()
#    for i in range(0,len(xs)):
#        print("xs["+str(i)+"]: " + str(xs[i]))

####    TESTS
addWebsite("http://www.archlinux.org",1)
addWebsite("http://www.vim.org",1)
addWebsite("http://programming.reddit.com",1)

print(curwords)
print(theta)

#mchacks = get_html_words("http://www.mcgill.ca").lower().split()
#mchacks = get_decent_words(mchacks)
#print(mchacks)
