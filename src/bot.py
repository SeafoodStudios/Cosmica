from tinydb import TinyDB, Query
import urllib.robotparser
from urllib.parse import urlparse
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
            try:
                parsed = urlparse(all_items[dice]["link"])
                domain = f"{parsed.scheme}://{parsed.netloc}"
                res = requests.get(domain.rstrip("/") + "/robots.txt", timeout=10)
                rp.parse(res.text.splitlines())
                
                if rp.crawl_delay("*") == None:
                    time.sleep(5)
                else:
                    time.sleep(rp.crawl_delay("*"))
            except Exception as e:
                print("ERROR: " + str(e))
                time.sleep(5)
                
            headers = {"User-Agent": "Mozilla/5.0 (compatible; CosmicaBot/1.0)"}
            data = requests.get(all_items[dice]["link"],headers=headers, timeout=10)
            links = re.findall(r'https?://[^\s"\'<>]+', str(data.text))
            
            for i in range(len(links)):
                if not db.search(User.link == str(links[i])):
                    if not re.search(r'\.(jpg|jpeg|png|gif|svg|css|js|pdf|zip|mp3|mp4|avi)(\?|$)', links[i], re.IGNORECASE):
                        db.insert({'link': str(links[i])})
                        print(links[i])
        except Exception as e:
            print("ERROR: " + str(e))
    else:
        db.insert({'link': "https://alltop.com"})
