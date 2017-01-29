import os, os.path
import random
import string

import cherrypy


class StringGenerator(object):
    @cherrypy.expose
    def index(self):
        return """<!DOCTYPE html>
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
                <p id="welcome-text" class="lead" style="margin-bottom: 1em; display: none">Invisible at first</p>

                    <center>
                    <div align="center" id="readroot" style="text-align:center; display: none;">
                        <input type="url" id="input-website" name="websiteURL" placeholder="Enter website URL" style="width: 65%; margin-top: 0.5em; margin-bottom: 0.5em; display: block">
                        </div>
                            <span id="writeroot"></span>
                        </div>
                    </div>

                    </center>

                    <div id="buttons-fields-add" style="text-align: center; display: none;">
                        <input type="image" align="center" id="add-field" value="Give me more fields!" src="/static/images/plus.png" height="25px" width="25px" style="margin-top: 1em;" />
                        <input type="image" align="center" id="remove-field" value="Remove field" src="/static/images/minus.png" height="25px" width="25px" style="margin-top: 1em;" />
                        <hr>
                    </div>

                    <center>
                            <a onclick="myFacebookLogin()" style="margin-top: 10em" class="btn center btn-social btn-facebook" id="facebook-login">
                                    <i class="fa fa-facebook"></i> Connect with Facebook
                            </a>
                    </center>
            
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

    @cherrypy.expose
    def generate(self, length=8):
        some_string = ''.join(random.sample(string.hexdigits, int(length)))
        cherrypy.session['mystring'] = some_string
        return some_string

    @cherrypy.expose
    def display(self):
        return cherrypy.session['mystring']

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


if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }
    cherrypy.server.socket_host = '127.0.0.1'
    cherrypy.server.socket_port = 80
    cherrypy.quickstart(StringGenerator(), '/', conf)