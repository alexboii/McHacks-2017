import main
from main import addWebsite, testWebsite

addWebsite("http://www.archlinux.org",1)
addWebsite("http://programming.reddit.com",1)
addWebsite("http://www.apple.ca",0)

testWebsite("http://www.debian.org")
testWebsite("http://www.stackoverflow.com")
testWebsite("https://www.twitter.com/realDonaldTrump")
