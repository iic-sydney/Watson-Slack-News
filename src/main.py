

import sys
import time
import os
from os.path import join, dirname

from slackclient import SlackClient
from dotenv import load_dotenv

from chatbot import ChatBot

def init(): 
    dotenv_path = join(dirname(__file__), ".env") 
    load_dotenv(dotenv_path)
    
def main():
    slack_client = SlackClient(SLACK_TOKEN)

    watson_bot = ChatBot(BOT_NAME, slack_client, WEBSOCKET_READ_DELAY)
    watson_bot.run()    

if __name__ == "__main__":
    init()

    # Push environment variables to constants
    SLACK_TOKEN = os.environ.get("SLACK_TOKEN")
    BOT_NAME = os.environ.get("BOT_NAME")
    WEBSOCKET_READ_DELAY = os.environ.get("WEBSOCKET_READ_DELAY")

    main()
