import configparser
import discord
from discord.ext import commands
import os

config = configparser.ConfigParser()
config.read('config.ini')

token = config['BASE']['token']

intents = discord.Intents.default()
intents.message_content = True  
bot = commands.Bot(command_prefix="$aip ", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="$aip help | " + config['BASE']['version']))
    
    await load_cogs()

async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and filename != "__init__.py":
            print("module detected",filename)
            await bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(token)