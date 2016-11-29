import time
import os

import watson
import news

class ChatBot(object):
    def __init__(self, bot_name, slack_client, delay):
        self.slack_client = slack_client 
        self.delay = float(delay)
        self.bot = {}
        self.bot['name'] = bot_name
        self.watson = watson.Conversation()
     
        # Get Bot ID from Slack API during init.
        api_call = slack_client.api_call("users.list")
        if api_call.get('ok'):
            users = api_call.get('members')
            for user in users:
                if 'name' in user and user.get('name') == bot_name:
                    self.bot['id'] = user.get('id')

                    # this is the id sandwiched between <@ID>. We use this to filter out messages not addressed to us.
                    self.bot['at_id'] = "<@" + self.bot['id'] + ">"


        # If we didn't get a Bot ID, destroy the bot
        if 'id' not in self.bot:
            raise ValueError("Chatbot Class failed to find Bot ID during initialisation. Are you sure you entered the right bot name?")

    def run(self):
        """
            Runs the main loop of the bot. Every time a chat message
            is sent in the channel, the bot picks up on this, parses it
            and responds appropriately.
        """
        if self.slack_client.rtm_connect():
            print("Watson Bot is connected and running!")
            while True: 
                command, channel = self.parse(self.slack_client.rtm_read())
                if command and channel: 
                    # Oh! The bot has had something addressed to it!
                    self.handle_message(command, channel)

                # Sleep for a bit...
                time.sleep(self.delay)
        pass
    

    def handle_message(self, command, channel):
        """
            The bot itself only recognises when it's been addressed and
            passes off to this function. This function will eventually
            push to the Watson Conversations API.
        """

        print("The Watson Bot has received a message!") 
        n = news.NewsAPI()
        n.source = "abc-news-au"

        result = self.watson.post(command)
        for message in result['output']['text']: 
            self.post_to_slack(message, channel)

        for intent in result['intents']:
            if intent['intent'] == "TellMeTheNews":
                for article in n.request()['articles']:
                    self.post_to_slack(article['url'], channel)
              
       

    def post_to_slack(self, response, channel):
        """
            Posts to slack
        """
        self.slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)


    def parse(self, slack_output):
        """ 
            Private helper function to make sure the bot only speaks
            when spoken to using the @ symbol.
        """ 
        for output in slack_output:
            if output and 'text' in output and self.bot['at_id'] in output['text']:
                return output['text'].split(self.bot['at_id'])[1].strip().lower(), output['channel']
        
        return None, None 

