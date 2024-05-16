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
model_engine = "gpt-3.5-turbo"

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    global model_engine
    if message.author.bot:
        return
    if message.author == client.user:
        return
    if client.user in message.mentions:
        print(f"Received message: {message.content}")
        msg = await message.reply("少々お待ちください..", mention_author=False)
        try:
            prompt = message.content.replace(f'@{client.user.name}', '').strip()
            if not prompt:
                await msg.delete()
                await message.channel.send("質問内容がありません")
                return
            thread = await message.create_thread(name=f"{message.author.name}の質問")
            completion = openai.ChatCompletion.create(
                model=model_engine,
                messages=[
                    {
                        "role": "system",
                        "content": "日本語で返答してください。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
            )
            response = completion["choices"][0]["message"]["content"]
            print(f"OpenAI API response: {response}")
            await msg.delete()
            await thread.send(response)
        except Exception as e:
            print(f"Error: {str(e)}")
            await message.reply("エラーが発生しました", mention_author=False)

client.run(token)