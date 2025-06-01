from tinydb import TinyDB, Query
import urllib.robotparser
import requests
import re
import time
import random

db = TinyDB("CosmicaLinkDatabase")
rp = urllib.robotparser.RobotFileParser()
User = Query()

while True:
    all_items = db.all()
    if all_items:
        try:
            dice = random.randint(0, len(all_items)-1)
            print((str(all_items[dice]["link"].rstrip("/"))) + "/robots.txt")
            rp.set_url((str(all_items[dice]["link"].rstrip("/"))) + "/robots.txt")
            rp.read()
            
            if rp.crawl_delay("*") == None:
                time.sleep(5)
            else:
                time.sleep(rp.crawl_delay("*"))

            headers = {"User-Agent": "Mozilla/5.0 (compatible; CosmicaBot/1.0)"}
            data = requests.get(all_items[dice]["link"],headers=headers)
            links = re.findall(r'https?://[^\s"\'<>]+', str(data.text))
            
            for i in range(len(links)):
                if not db.search(User.link == str(links[i])):
                    if not re.search(r'\.(jpg|jpeg|png|gif|svg|css|js|pdf|zip|mp3|mp4|avi)(\?|$)', links[i], re.IGNORECASE):
                        db.insert({'link': str(links[i])})
                        print(links[i])
        except Exception as e:
            print("ERROR: " + str(e))
    else:
        db.insert({'link': "https://news.ycombinator.com/"})
