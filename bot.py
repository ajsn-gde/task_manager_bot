import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
import database

# load environment variables from .env file
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# configure required intents
intents = discord.Intents.default()
intents.message_content = True  # enable reading message content for commands

# initialize bot instance
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    # set custom bot activity status
    activity = discord.Activity(type=discord.ActivityType.watching, name="your tasks | !show_tasks")
    await bot.change_presence(status=discord.Status.online, activity=activity)
    
    print(f"🤖 bot logged in as: {bot.user.name} (id: {bot.user.id})")
    print("--------------------------------------------------")


async def main():
    async with bot:
        # initialize database tables on startup
        await database.init_db()

        # load discord commands cog asynchronously
        await bot.load_extension("commands")

        # start the discord bot
        await bot.start(TOKEN)


if __name__ == "__main__":
    if not TOKEN:
        raise ValueError("DISCORD_TOKEN is missing in .env file")
    
    asyncio.run(main())