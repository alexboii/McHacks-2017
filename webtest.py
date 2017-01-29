import cherrypy
import main
import scraper
import requests
import html.parser
import urllib
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
                <form method="get" action="recommend">
                    <button type = "submit">Get Recommendation</button>
                </form>
            </body>
            </html>"""

likes = ["BarackObama","SNL","Shia Labeouf","British Museum", "Kermit the Frog", "Lin-Manuel Miranda", "Disney","Ellen Degeneres", "Earth Day Network", "Aubrey Plaza", "CNN International", "Natural History Museum London"]

urls = scraper.getURLs(likes[6],10)
scores = []
#for i in urls:
#    scores.append(testWebsite(str(i,'utf-8')))
#for i in range(0,len(urls)):
#    for j in range(i+1,len(urls)):
#        if scores[j] > scores[i]:
#            tmp = urls[j]
#            urls[j] = urls[i]
#            urls[i] = tmp
#            tmp = scores[j]
#            scores[j] = scores[i]
#            scores[i] = tmp

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
        result = html + "Recommended site: <a href=" + urls[count] + ">" + urls[count] + "</a>"
        count = (count + 1)%len(urls)
        return result
cherrypy.quickstart(Test())
