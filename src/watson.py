import json
import os

from watson_developer_cloud import ConversationV1

class Conversation(object):
    def __init__(self):
        self._username = os.environ.get("WATSON_USERNAME")
        self._password = os.environ.get("WATSON_PASSWORD")
        self._version = os.environ.get("WATSON_VERSION")
        
        # Instantiates watson conversation class for making API requests to conversations ervice
        self.conversation = ConversationV1 (
                username=self._username,
                password=self._password,
                version=self._version
        )

        self.workspace = os.environ.get("WATSON_WORKSPACE_ID")
        self.context=  {}
        

    def post(self, text):
        """
            Sends text to watson conversations service
        """
        response = self.conversation.message (
                workspace_id=self.workspace,
                message_input={'text': text},
                context=self.context
        )

        # passes the context to the class object so your next request to conversations doesn't
        # just blank on where you were up to
        if 'context' in response:
            self.context = response['context']
 
        return response

    def parse_response(self, response):
        pass

# When you send multiple requests for the same conversation, include the context object from the previous response.
# response = conversation.message(workspace_id=workspace_id, message_input={'text': 'turn the wipers on'},
#                                context=response['context'])
# print(json.dumps(response, indent=2))
