import os

from dotenv import load_dotenv
import discord
from discord.ext import commands
from utils.db_utils import *
import logging

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
# intents.members = True

client = discord.Client(intents=intents)
db_session = create_dbsession()

bot = commands.Bot(command_prefix='!', intents=intents)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    # db_session.


# @client.event
# async def on_private_channel(private_channel):
#     print("Hello")
#     await private_channel.author.send("Привет, это твой личный диалог с БОГОМ!")
@bot.command(name="user_list")
async def user_list(ctx):
    # print("hellos")
    # text_channel = ctx.message.channel
    # members = text_channel.members
    # for member in members:
    #     print(member.name)
    # print(client.get_all_members())
    # for member in ctx.guild.members:
    #     print(member.name)
    for member in ctx.guild.members:
        print(member)



@client.event
async def on_message(message):
    # print(message.guild.members)
    for member in message.guild.members:
        print(member)
    if message.author == client.user:
        return
    # print(message.author)
    if message.content.startswith('!hello'):
        await message.author.send('Hello!')

    if message.content.startswith('!help'):
        await message.author.send('Need some help?')


client.run(TOKEN)

# config = {
#     'token': 'ODMxMjAwMTM2ODk2OTcwODMz.GNU1E_.MgyuVsIFxza0wIVaJnjQzBh2BMIAyqrMtWiMsM',
#     'prefix': '!',
# }
# intents = discord.Intents.default()
# bot = commands.Bot(command_prefix=config['prefix'], intents=intents)
# db_session = create_dbsession()
# @bot.command()
# async def user(ctx):
#     logging.info("hello")
# bot.run(config['token'])
