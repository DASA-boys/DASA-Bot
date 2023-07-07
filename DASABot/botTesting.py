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
    print("Bot is ready.")


@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')


@bot.command(description='Reload a cog.')
async def reload(ctx, extension):
	try:
		await bot.reload_extension(f'cogs.{extension}')
		await ctx.send(f'`{extension}` `has been reloaded.`')
	except:
		await ctx.send("`Invalid module.`")

async def load():
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            await bot.load_extension(f"cogs.{file[:-3]}")

async def main():
    await load()
    await bot.start(BOT_TOKEN)

asyncio.run(main())