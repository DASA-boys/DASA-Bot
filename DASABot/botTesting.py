import os
from dotenv import load_dotenv
from connectRankDB import connectDB

import discord
from discord.ext import commands
import asyncio

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix = "?", intents = intents)

# Initialize the connectDB object
# db = connectDB()

@bot.event
async def on_ready():
    print("Bot is running.")


@bot.command()
async def ping(ctx):
    await ctx.channel.send("Pong!")


async def load():
    for file in os.listdir("DASABot/cogs"):
        if file.endswith(".py"):
            await bot.load_extension(f"cogs.{file[:-3]}")

async def main():
    await load()
    await bot.start(BOT_TOKEN)

asyncio.run(main())