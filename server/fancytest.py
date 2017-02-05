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

#html = """<html>
#            <head></head>
#            <body>
#                <form method="get" action="add">
#                    <input type="text" value="" name="site" />
#                    <button type="submit">Love it</button>
#                    <button type="submit" formaction="addNeg">Hate it</button>
#                </form>
#                <form method="get" action="test">
#                    <input type="text" value="" name="site" />
#                    <button type="submit">Test For Enjoyment</button>
#                </form>
#                <form method="get" action="recommend">
#                    <button type = "submit">Get Recommendation</button>
#                </form>
#            </body>
#            </html>"""
html = """<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>Trottier</title>

    <!-- Bootstrap Core CSS -->
    <link href="/static/css/bootstrap.min.css" rel="stylesheet">

    <link rel="stylesheet" href="/static/css/stylesheet.css">
    <link rel="stylesheet" href="/static/css/assets/css/font-awesome.min.css">

    <script
            src="https://code.jquery.com/jquery-3.1.1.min.js"
            integrity="sha256-hVVnYaiADRTO2PzUGmuLJr8BLUSjGIZsDYGmIJLv2b8="
            crossorigin="anonymous">
    </script>

    <script src="/static/js/fb_plugin.js"></script> 
    <script src="/static/js/page.js"></script> 

    <link rel="stylesheet" href="https://yui.yahooapis.com/pure/0.6.0/pure-min.css">

    <!-- Custom CSS -->
    <style>

    body {
        padding-top: 70px;
        /* Required padding for .navbar-fixed-top. Remove if using .navbar-static-top. Change if height of navigation changes. */
    }
    </style>

    <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
        <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
        <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->

</head>

<body>

    <script>
        window.fbAsyncInit = function() {
            FB.init({
            appId      : '406246069709180',
            xfbml      : true,
            version    : 'v2.8'
            });

            FB.AppEvents.logPageView();

            $(document).trigger('fbload');
        };

        (function(d, s, id){
            var js, fjs = d.getElementsByTagName(s)[0];
            if (d.getElementById(id)) {return;}
            js = d.createElement(s); js.id = id;
            js.src = "//connect.facebook.net/en_US/sdk.js";
            fjs.parentNode.insertBefore(js, fjs);
        }(document, 'script', 'facebook-jssdk'));

    </script>

    <!-- Page Content -->
    <div class="container">

        <div class="row">
            <div class="col-lg-12 text-center">
                <h1>Get website recommendations!</h1>
                <p id="welcome-text" class="lead" style="margin-bottom: 5em; visibility: hidden;">Invisible at first</p>

                <form method="get" action="add" style="text-align: center; margin-bottom: 1em;">
                    <input type="text" value="" name="site" style="width: 70%; margin-top: 1em; display: inline;" />
                    <input type="image" align="center" id="love -field" value="Love it" src="static/images/thumbs_up.png" height="25px" width="25px" style="display: inline;" />
                    <input type="image" formaction="addNeg" align="center" id="hate-field" value="Hate it" src="static/images/thumbs_down.png" height="25px" width="25px" style="display: inline;" />

                </form>
                <form method="get" action="test" style="margin-top: 3em; text-align: center">
                    <input type="text" value="" name="site" style="width: 70%; margin-top: 1em; display: inline;"/>
                    <button class="btn blue" type="submit" style="padding: 4px; width: 200px; height: 30px; font-size: 14px; display: inline;" >Test For Enjoyment</button>
                </form>
                <form method="get" action="recommend">
                    <button class="btn blue" type="submit" style="margin-top: 5em">Get Recommendation</button>
                </form>
            
            </div>
        </div>
        <!-- /.row -->

    </div>
    <!-- /.container -->

    <!-- jQuery Version 1.11.1 -->
    <script src="/static/js/jquery.js"></script>

    <!-- Bootstrap Core JavaScript -->
    <script src="/static/js/bootstrap.min.js"></script>
    <script src="/static/js/page.js"></script> 
    

</body>

</html>
"""

likes = ["Barack Obama","SNL","Shia Labeouf","British Museum", "Kermit the Frog", "Lin-Manuel Miranda", "Disney","Ellen Degeneres", "Earth Day Network", "Aubrey Plaza", "CNN International", "Natural History Museum London"]

for i in range(0,len(likes)):
    likes[i] = likes[i].replace(' ','')

print(likes)

urls = scraper.getURLs(likes[0],10)
scores = []
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
        result = html + "Recommended site: <a href=" + urls[count] + ">" + urls[count] + "</a>"
        count = (count + 1)%len(urls)
        return result
cherrypy.quickstart(Test())
