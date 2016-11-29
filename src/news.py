
import requests
import json
import os

class NewsAPI(object):
    def __init__(self):
        self.key = os.environ.get("NEWS_API_TOKEN")
        self.source="techcrunch"
        self.url = os.environ.get("NEWS_API_URL")
    
        #self.key = "9205122fd6eb4766b854ef6930797ad6"
        #self.url = "https://newsapi.org/v1/articles"

    def request(self):
        params = {'source': self.source, 'apiKey': self.key}
        ret = requests.get(self.url, params=params)
        return json.loads(ret.content) 
