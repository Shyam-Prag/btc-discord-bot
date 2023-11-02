from discord_webhook import DiscordWebhook, DiscordEmbed
from discordwebhook import Discord
import json
import requests
import math
import os

DISCORD_WEBHOOK_URL= os.environ["DISCORD_WEBHOOK_URL"]
API_KEY = os.environ["API_KEY"]
BTC_URL = os.environ["BTC_URL"]
webhook = DiscordWebhook(url=f"{DISCORD_WEBHOOK_URL}")
discord = Discord(url=DISCORD_WEBHOOK_URL)

def lambda_handler(event, context):

    url = BTC_URL
    
    querystring = {"referenceCurrencyUuid":"yhjMzLPhuIDl"}
    
    headers = {
        "X-RapidAPI-Key": f"{API_KEY}",
        "X-RapidAPI-Host": "coinranking1.p.rapidapi.com"
    }
    
    response = requests.get(url, headers=headers, params=querystring)
    
    # Convert the response object to a Python dictionary
    response_dict = json.loads(response.text)
    
    # Extract the price value
    BTC_Price = response_dict["data"]["price"]
    
    floated_value = float(BTC_Price)
    
    BTC_Price_rounded = round(floated_value, 2)
    
    BTC_message = f'The price of Bitcoin is: ${BTC_Price_rounded}'
    
    discord.post(content = BTC_message)
    
    
    return BTC_message
