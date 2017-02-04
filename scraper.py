import re, urllib.request
import requests
import html.parser
import urllib
from requests.exceptions import HTTPError
from socket import error as SocketError
from http.cookiejar import CookieJar
from re import findall

urls = []

def getURLs(s,n):
    url = "https://www.bing.com/search?q=" + s + "&num=" + str(n)
    urls = []
    hdr = {'User-Agent': 'Mozilla/5.0'}
    try:
        req = urllib.request.Request(url,None, hdr)
        cj = CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        response = opener.open(req)
        raw_response = response.read().decode('utf8',errors='ignore')
        response.close()
    except urllib.request.HTTPError as inst:
        output = format(inst)
        print(output)
    matches = findall(b'''href=["'](.[^"']+)["']''',urllib.request.urlopen(req).read(),re.I)
    matches = [urllib.parse.quote((w.split(b"&")[0]).strip()) for w in matches if not b"google" in w and not b"youtube" in w and not b"wikipedia" in w and not b"search" in w and not b"blogger" in w and not b"bing" in w and not b"go.microsoft" in w and not b"choice.microsoft" in w and b"http" in w]
    if n < len(matches): n = len(matches)
    for i in matches[:n]:
        if((i.startswith("/url?q="))): i = i[7:]
        if("%3A" in i): i = i.replace("%3A",":")
        urls.append(i)
    return urls

