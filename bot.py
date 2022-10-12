import discord
import random
import string
from tokens import BOT_SECRET

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!give-hewwo'):
        tuna_message = []
        for i in range(random.randint(0,20)):
            tuna_message.append(random.randint(0,25)*random.choices(string.ascii_lowercase)[0])

        await message.channel.send(''.join(tuna_message))

    if message.content.startswith('!give-treat'):
        await message.channel.send('meow', {files: ["https://i.imgur.com/XxxXxXX.jpg"]})

client.run(BOT_SECRET)