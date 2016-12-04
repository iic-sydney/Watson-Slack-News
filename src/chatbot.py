import time
import os

import watson
import weather
import news
import alchemy

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
                    #self.bot['at_id'] = "<@" + self.bot['id'] + ">"


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
            Given a message on the correct channel, sends it over to Conversations API for analysis, then responds
            accordingly based on intent. 
        """

        print("The Watson Bot has received a message!") 
        print(": Message: ", command)
       
        # Push to watson conversations API
        result = self.watson.post(command) 
        
        # This is how watson conversations has decided to respond 
        for message in result['output']['text']: 
            self.post_to_slack(message, channel)

        # These are the intents that watson conversations got. 
        intents = result['intents']
        
        # If an intent exists that requires the bot to fetch some data, like news or weather,
        # pass it off to the relevant function. Otherwise it's just conversational, and Watson Conversations API
        # has probably already handled it
        for intent in intents:
            if intent['intent'] == "TellMeTheNews":
                self.say_the_news(command, channel)
            if intent['intent'] == "TellMeTheWeather":
                self.say_the_weather(command, channel)
                
    def say_the_news(self, command, channel):
        """
            Fetches 5 articles from the abc and regurgitates them to the user.

            Activates when the intent in handle_message is "TellMeTheNews"
        """
        news_api = news.NewsAPI()
        news_api.source = "abc-news-au"

        status_code, content = news.request()

        if status_code == 200:
            for article in content['articles'][:5]:
                self.post_to_slack(article['url'], channel)
        else:
            error = "Sorry, there seems to have been an error when fetching the news. Looks like my news resource might be down right now. I'm sure the administrator can help get me back online."
            print "ERROR: Status Code: {0}".format(status_code)
            print "{}".format(content)
            self.post_to_slack(error, channel)

    def say_the_weather(self, command, channel):
        """
            Fetches the current weather in celsius. To do this it posts the message over to alchemy API for further analysis to extract entities - something that we didn't need
            to do for news or general conversation. Once it receives an entity with enough details it'll post the weather.

            Activates when the intent in handle_message is "TellMeTheWeather"
        """
        alchemy_api = alchemy.AlchemyAPI()
        weather_api = weather.WeatherAPI() 

        entities = alchemy_api.request_entities(command)

        if entities and len(entities) > 0:
            for entity in entities:
                if 'type' in entity and entity['type'] == 'City' and 'disambiguated' in entity:
                    entity_details = entity['disambiguated'] 
                    if 'geo' in entity_details:
                        geocodes = entity_details['geo'].split()
                        latitude = geocodes[0]
                        longitude = geocodes[1]
                        city_name = entity_details['name']

                        weather_status, weather_response = weather_api.request_weather(latitude, longitude)

                        if weather_status == 200:
                            temp = weather_content['observation']['temp']
                            response = "The weather in {0} is currently {1} degrees celsius.".format(city_name)
                            self.post_to_slack(response, channel)
                        else:
                            # Error - bad request made (shouldn't happen) or maybe the service is down or has reached its limit of calls for the month
                            print "ERROR: Bad Request made, or maybe the service is down / has reached its API call limit"
                            error = "Sorry, there seems to have been an error fetching for {}. Looks like my weather resource might be down. I'm sure the administrator can get me back online.".format(city_name)
                            self.post_to_slack(error, channel)
                    else:
                        # Error because you specified a city, but for whatever reason AlchemyAPI isn't giving the bot the geocodes. Sometimes this happens, not your fault, nothing you can do.
                        print "ERROR: A city was found, but the AlchemyAPI is not providing the geocodes necessary to make a request to the Weather API. This might be because of lack of detail, but it also might be because of limitations in the Alchemy API"
                        error = "Sorry, you did give me a city but I'm afraid I just can't find it. Maybe try specifying it in a different way."
                        self.post_to_slack(error, channel)
                else:
                    # Error because you specified a city, but not in enough detail
                    print "ERROR: Request for Weather in City does not provide enough detail to find the correct city along with its accompanying information."
                    error = "I couldn't find the city based on that request. Could you perhaps try to provide a little more detail?"
                    self.post_to_slack(error, channel)
            else:
                # Error because you didn't specify a city
                print "ERROR: User didn't specify a city"
                error = "Please try again, this time specifying a city."
                self.post_to_slack(error, channel)

                    

    def post_to_slack(self, response, channel):
        """
            Posts to slack
        """
        self.slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)


    def parse(self, slack_output):
        """ 
            Parses every message to ensure the bot only speaks to others and not in itself - prevents a feedback loop. Used in run() so that only the correct messages
            are passed to handle_message method
        """ 
        for output in slack_output:
            if output and 'text' in output and 'user' in output:
                if output['user'] != self.bot['id']:
                    return output['text'].strip().lower(), output['channel']
        
        return None, None 

