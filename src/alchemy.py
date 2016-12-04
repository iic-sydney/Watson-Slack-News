import os
import requests
import json

from watson_developer_cloud import AlchemyLanguageV1

class AlchemyAPI(object):
    def __init__(self):
       
        token = os.environ.get("ALCHEMY_TOKEN")
        #token="b661dc0ca544455a4fedf2274d28e39573a3ae16"
          
        self.alchemy = AlchemyLanguageV1(api_key=token)

    
    def request_entities(self, text):
        result = self.alchemy.combined(text=text, extract=['entity'])
        return result['entities']
