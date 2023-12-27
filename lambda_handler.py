import os 
import boto3
from PIL import Image, ImageDraw, ImageFont
import requests
from discord_webhook import DiscordWebhook, DiscordEmbed
from discordwebhook import Discord
import json

DISCORD_WEBHOOK_URL= os.environ["DISCORD_WEBHOOK_URL"]
API_KEY = os.environ["API_KEY"]
BTC_URL = os.environ["BTC_URL"]
webhook = DiscordWebhook(url=f"{DISCORD_WEBHOOK_URL}")
discord = Discord(url=DISCORD_WEBHOOK_URL)

def lambda_handler(event, context):
    # LETS GET THE PRICE OF BTC
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
    
    #################################################################
    # CREATES IMAGE
    print(os.listdir('/opt'))
    print(os.listdir('/opt/python'))
    
    
    new = Image.new('RGB', (200,100), color=(255, 153, 0))
    
    d = ImageDraw.Draw(new)
    
    font = ImageFont.truetype(r'/opt/python/verdanaz.ttf', 25)  #ADDED verdanaz.ttf FILE IN LAMBDA LAYER
    
    d.text((65,5), "BTC", font = font, fill=(0,0,0), align = "left")
    d.text((80,30), "=", font = font, fill=(0,0,0), align = "left")
    d.text((30,60), f"${BTC_Price_rounded}", font = font, fill=(0,0,0), align = "left")
    
    new.save('/tmp/new_bitcoin_img.png')
    
    #CHECKS IF IMG IS SAVED TO /TMP
    print(os.listdir('/tmp'))
    
    #################################################################
    # LETS SEND MESSAGE TO DISCORD VIA WEBHOOK
    webhook = DiscordWebhook(url=f"{DISCORD_WEBHOOK_URL}")

    with open("/tmp/new_bitcoin_img.png", "rb") as f:
        webhook.add_file(file=f.read(), filename="new_bitcoin_img.png")
    
    embed = DiscordEmbed(title="BTC UPDATE", description= f"The price of BTC is ${BTC_Price_rounded}", color="03b2f8")
    
    embed.set_thumbnail(url="attachment://new_bitcoin_img.png")
    
    webhook.add_embed(embed)
    response = webhook.execute()
    
    
    return "hello"
    
