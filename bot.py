import discord
from discord.ext import commands

client = commands.Bot(
    command_prefix="^",
    intents=discord.Intents.all(),
    help_command=None,
    case_insensitive=True,
)