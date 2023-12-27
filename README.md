# btc-discord-bot

Workflow:
1. EventBridge triggers Lambda on CRON schedule
2. Lambda receives price of BTC from external API (coinranking1.p.rapidapi.com)
3. Create image using Pillow library -> write BTC price to image
4. Send embedded message, which contains newly created image, to Discord server using discord's webhook URL. 

Notes:
- ATTACHED verdanaz.ttf FONT FILE AS LAMBDA LAYER - https://github.com/gasharper/linux-fonts/tree/master
- Other dependencies added as Layers. Create Layer -> https://repost.aws/knowledge-center/lambda-layer-simulated-docker
- works with Lambda3.11 runtime (haven't tested other runtimes)
