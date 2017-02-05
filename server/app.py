#!flask/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for

import main
import scraper
import requests
import html.parser
import urllib
import random
import math
from flask.ext.cors import CORS
from random import randrange
from requests.exceptions import HTTPError
from socket import error as SocketError
from http.cookiejar import CookieJar
from main import addWebsite, testWebsite, cost, curwords, xs, theta, y


app = Flask(__name__, static_url_path = "")
CORS(app)


likes = ["Barack Obama","SNL","Montreal","NHL", "Sports", "Spotify", "Disney","Ellen Degeneres", "Movie", "Politics", "Science", "Programming"]

for i in range(0,len(likes)):
    likes[i] = likes[i].replace(' ','')

urls = scraper.getURLs(likes[randrange(len(likes))],40)

count = 0

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

@app.route('/script/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201


@app.route('/script/api/positive/<path:site>', methods = ['PUT'])
def add(site="http://www.archlinux.org"):
    addWebsite(site, 1)
    return "Website " + site + " added."

@app.route('/script/api/negative/<path:site>', methods = ['PUT'])
def addNeg(site):
    addWebsite(site,0)
    return html + ("Cost: " + str(cost()) + ", amount of words: " + str(len(curwords)))

@app.route('/script/api/testwebsite/<path:site>', methods = ['GET'])
def test(site):
    odds = testWebsite(site)
    return "Odds that you'll enjoy " + site + ": " + str(100*odds) + "%"

def recommend():
    global count
    urls = scraper.getURLs(likes[randrange(len(likes))],40)
    result = html + "Recommended site: <a href=" + urls[count%len(urls)] + ">" + urls[count%len(urls)] + "</a>"
    count = (count + 1)%len(urls)
    return "Negative website added"

def superiorrecommend():
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
        while(main.countNonBlacklisted(urls) < 5):
            word = curwords[probs[randrange(len(probs))]]
            urls = scraper.getURLs(word,40)
        pos = randrange(len(urls))
        while main.isBlacklisted(urls[pos]): pos = randrange(len(urls))
        result = html + "Recommended site: <a href=" + urls[pos] + ">" + urls[pos] + "</a>"
        count = (count + 1)%len(urls)
        return result

if __name__ == '__main__':
    app.run(debug=True)