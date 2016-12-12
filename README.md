# IIC Sydney's Watson Slack Bot

A Slack bot that takes advantage of various Bluemix services to demonstrate the ease of use of IBM's cognitive APIs for an upcoming roadshow.

This project was largely completed in about 2 days or so.

### API Usage
The Slack bot demonstrates usage of the following Bluemix services:

* Watson Conversations
* Alchemy Language API
* Weather Company API

And the following external services:

* news-api.org

### Running the Bot
The Watson bot takes advantage of python-dotenv to load environment variables that are used in the program. This mostly covers credentials and URLs for the various services.

To run the service, ensure you have the following .env file in the ./src folder:

```
SLACK_TOKEN= // Your slack token
BOT_NAME= // the registered name of the slack bot
WEBSOCKET_READ_DELAY= // time step for reading from the slack chat

WATSON_USERNAME= // Watson conversations username credential
WATSON_PASSWORD= // Watson conversations password credential
WATSON_VERSION= // Watson conversations version
WATSON_WORKSPACE_ID= // Watson conversations workspace ID

NEWS_API_TOKEN= // token for news-api.org
NEWS_API_URL= // url for retrieving articles from news-api.org

WEATHER_USERNAME= // username credentials for weather company service
WEATHER_PASSWORD= // password credentials for weather company service
WEATHER_URL= // URL for weather company service

ALCHEMY_URL= // URL for Alchemy API service
ALCHEMY_TOKEN = // token for Alchemy API Service
```
