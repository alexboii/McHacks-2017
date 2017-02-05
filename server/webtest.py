import cherrypy
import main
import scraper
import requests
import html.parser
import urllib
import random
import math
from random import randrange
from requests.exceptions import HTTPError
from socket import error as SocketError
from http.cookiejar import CookieJar
from main import addWebsite, testWebsite, cost, curwords, xs, theta, y

html = """<html>
            <head></head>
            <body>
                <form method="get" action="add">
                    <input type="text" value="" name="site" />
                    <button type="submit">Love it</button>
                    <button type="submit" formaction="addNeg">Hate it</button>
                </form>
                <form method="get" action="test">
                    <input type="text" value="" name="site" />
                    <button type="submit">Test For Enjoyment</button>
                </form>
                <form method="get" action="superiorrecommend">
                    <button type = "submit">Get Recommendation</button>
                </form>
            </body>
            </html>"""

likes = ["Barack Obama","SNL","Montreal","NHL", "Sports", "Spotify", "Disney","Ellen Degeneres", "Movie", "Politics", "Science", "Programming"]

for i in range(0,len(likes)):
    likes[i] = likes[i].replace(' ','')

#print(likes)

urls = scraper.getURLs(likes[randrange(len(likes))],40)
#scores = []
#print("Beginning score generation")
#for i in range(0,len(urls)):
#    print("Appending score for " + urls[i] + "...")
#    scores.append(testWebsite(urls[i]))
#print("Ended score generation.")
#print("Beginning sorting process")
#for i in range(0,len(urls)):
#    for j in range(i+1,len(urls)):
#        if scores[j] > scores[i]:
#            tmp = urls[j]
#            urls[j] = urls[i]
#            urls[i] = tmp
#            tmp = scores[j]
#            scores[j] = scores[i]
#            scores[i] = tmp
#
#urls.sort(key=lambda x: testWebsite(str(x,'utf-8')))
count = 0

class Test(object):
    @cherrypy.expose
    def index(self):
        return html

    @cherrypy.expose
    def add(self,site="http://www.archlinux.org"):
        addWebsite(site,1)
        return html + ("Cost: " + str(cost()) + ", amount of words: " + str(len(curwords)))

    @cherrypy.expose
    def addNeg(self,site):
        addWebsite(site,0)
        return html + ("Cost: " + str(cost()) + ", amount of words: " + str(len(curwords)))

    @cherrypy.expose
    def test(self,site):
        odds = testWebsite(site)
        return html + "Odds that you'll enjoy " + site + ": " + str(100*odds) + "%"

    @cherrypy.expose
    def recommend(self):
        global count
        urls = scraper.getURLs(likes[randrange(len(likes))],40)
        result = html + "Recommended site: <a href=" + urls[count%len(urls)] + ">" + urls[count%len(urls)] + "</a>"
        count = (count + 1)%len(urls)
        return result
    @cherrypy.expose
    def superiorrecommend(self):
        global count
        global theta
        if(len(main.theta) < 50): return self.recommend()
        else:
            probs = []
            for i in range(0,len(main.theta)):
                if main.theta[i] < 0: continue
                for j in range(0,math.floor(main.theta[i])):
                    probs.append(i)

            word = curwords[probs[randrange(len(probs))]]
            urls = scraper.getURLs(word,40)
#            max_val = max(main.theta)
#            max_index = main.theta.index(max_val)
            while(main.countNonBlacklisted(urls) < 5):
                word = curwords[probs[randrange(len(probs))]]
                urls = scraper.getURLs(word,40)
            pos = randrange(len(urls))
            while main.isBlacklisted(urls[pos]): pos = randrange(len(urls))
            result = html + "Recommended site: <a href=" + urls[pos] + ">" + urls[pos] + "</a>"
            count = (count + 1)%len(urls)
            return result

cherrypy.quickstart(Test())
