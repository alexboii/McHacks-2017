import cherrypy
import main
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
            </body>
            </html>"""

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
cherrypy.quickstart(Test())
