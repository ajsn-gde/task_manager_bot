import discord
from discord.ext import commands
import database

class TaskCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    