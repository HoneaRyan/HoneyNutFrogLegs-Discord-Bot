import discord
import random
import string
import glob
from tokens import BOT_SECRET
from db_manage import create_connection, get_treats, update_treats, get_treaterboard

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

    if message.content.startswith('!treaterboard'):
        conn = create_connection()
        res = get_treaterboard(conn)
        if len(res) <= 10:
            nbr_display = len(res)
        else:  
            nbr_display = 10
        name_list = []
        for i in range(nbr_display):
            user = await client.fetch_user(res[i][0])
            name_list.append(str(i+1) + ': ' + user.display_name)
        score_list = ['{}'.format(res[i][1]) for i in range(nbr_display)]
        

        embed = {
            'title' : 'Treaterboard',
            'type' : 'rich',
            'fields' : [
                {
                    'name' : 'Tuna\'s Top {}'.format(nbr_display),
                    'value' : '\n'.join(name_list),
                    'inline' : True
                },
                {
                    'name' : 'Treats',
                    'value': '\n'.join(score_list),
                    'inline' : True
                }
            ]
        }
        await message.channel.send(embed = discord.Embed.from_dict(embed))


    if message.content.startswith('!give-treat'):
        file_path_type = "tuna-images\\*.jpg"
        images = glob.glob(file_path_type)
        conn = create_connection()
        id = message.author.id
        name = message.author.name
        if name == 'Sabertooth18':
            await message.channel.send('no dick pic for you')
        mess, nbr_treats = get_treats(conn, id)
        if (mess != ''):
            await message.channel.send(mess)
        else: 
            update_treats(conn, id, nbr_treats + 1)
            with open(str(random.choice(images)), 'rb') as f:
                picture = discord.File(f)
                if (message.author.nick != None):
                    await message.channel.send('Thanks {}! You have given me {} treats!'.format(message.author.nick, nbr_treats + 1), file=picture)
                else:
                    await message.channel.send('Thanks {}! You have given me {} treats!'.format(message.author.name, nbr_treats + 1), file=picture)
            conn.commit()


client.run(BOT_SECRET)