import discord
import openai
from dotenv import load_dotenv
import os

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

token = os.getenv("DISCORD_TOKEN")
openai.api_key = os.getenv("OPENAI_API_KEY")

model_engine = "gpt-4o"

@client.event
async def on_ready():
  print(f'We have logged in as {client.user}')

@client.event
async def on_message():
  global model_engine
  if message.author.bot:
    return
  if message.author == client.user:
    return
  
    if client.user in message.mentions:
                #botに話しかけて待機中に表示されるメッセージ
        msg = await message.reply("少々お待ちください..", mention_author=False)
        try:
            prompt = message.content.replace('1239748545612091464', '')
            if not prompt:
                await msg.delete()
                await message.channel.send("質問内容がありません")
                return
            completion = openai.ChatCompletion.create(
            model=model_engine,
            messages=[
                {
                    "role": "system",
                    #↓この命令を一文書くことですべての会話に犬っぽく返してくれるようになる
                    "content": "日本語で返答してください。"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],)

            response = completion["choices"][0]["message"]["content"]
            await msg.delete()
            await message.reply(response, mention_author=False)
        except:
            import traceback
            traceback.print_exc()
            await message.reply("エラーです", mention_author=False)

client.run(token)