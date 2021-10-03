# Importing modules/libraries
import tweepy
import time
import requests
import json
import os
from os import environ

CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_KEY = environ['ACCESS_KEY']
ACCESS_SECRET = environ['ACCESS_SECRET']
MENTION_ID = environ['MENTION_ID']

print("Hello Making the connection with twitter!!")

# Initialization code

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

api = tweepy.API(auth)
print("Connection Done!")

# Some important variables which will be used later
bot_id = int(api.me().id_str)
mention_id = MENTION_ID
message = "Hi, {}, Current Stock Price of {} is {}"
retweetMessage = ''
# The actual bot
while True:
    if mention_id != 0:
        mentions = api.mentions_timeline(since_id=mention_id)  # Finding mention tweets
        # Iterating through each mention tweet
        for mention in mentions:
            # print("Mention tweet found")
            print(f"{mention.author.screen_name} - {mention.text}")
            mention_id = mention.id
            print("this is the mention id", mention_id)
            if mention.author.id != bot_id:
                try:
                    stockName = mention.text.replace("@IndianStockBot ", "")
                    url = "https://stock-price-bot.netlify.app/.netlify/functions/stock-price?queryStock=" + stockName
                    print('calling stock api ', url)
                    request = requests.get(url)
                    if request.status_code == 200:
                        responseData = request.json()
                        print(responseData)
                        data = json.loads(json.dumps(responseData))
                        if 'StockName' in data:
                            retweetMessage = message.format(mention.author.name, data['StockName'], data['price'])
                        else:
                            retweetMessage = 'Hi, {}, Sorry! No Stock Found'.format(mention.author.name)
                        # api.update_status(message.format(mention.author.screen_name),
                        #                  in_reply_to_status_id=mention.id_str)
                        print("Successfully replied!!!  ", retweetMessage)
                    else:
                        print("Server Not Reachable")
                except Exception as exc:
                    print('I am in exception')
                    print(exc)
            print('going for sleep for 15 Seconds.')
        time.sleep(15)  # The bot will only check for mentions every 15 seconds, unless you tweak this value
    else:
        print("Mention ID is not set, closing app.")
        break
