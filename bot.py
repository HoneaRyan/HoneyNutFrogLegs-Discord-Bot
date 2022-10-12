import discord
import random
import string
import glob
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
        file_path_type = "tuna-images\\*.jpg"
        images = glob.glob(file_path_type)
        with open(str(random.choice(images)), 'rb') as f:
            picture = discord.File(f)
            if (message.author.nick != None):
                await message.channel.send('Thanks {}!'.format(message.author.nick), file=picture)
            else:
                await message.channel.send('Thanks {}!'.format(message.author.name), file=picture)


client.run(BOT_SECRET)