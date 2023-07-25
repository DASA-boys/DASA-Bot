import os
from dotenv import load_dotenv
from connectRankDB import connectDB

import discord
from discord.ext import commands
from discord import app_commands
import asyncio

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix="/",
                    intents=intents)
bot.remove_command('help')

@bot.group(invoke_without_command = True)
async def help(ctx):
    em = discord.Embed(title = "DASA Bot Commands", description = "use /help <command> for information about commands", color = discord.Color.random())
    em.add_field(name='</cutoff:1131246029531004968>',
                    value = 'college, year, ciwg, round, branch(optional)',
                    inline=False)
    em.add_field(name='</analyse:1131969029968502918>',
                    value='rank, ciwg, branch(optional)',
                    inline=False)
    em.add_field(name='</airport:1133054254203011082>',
                    value='college',
                    inline=False)
    em.set_footer(text = "This message will be deleted after 1 minute.")
    await ctx.send(embed = em, delete_after = 60)

@help.command()
async def cutoff(ctx):
    em = discord.Embed(title='</cutoff:1131246029531004968>',
                       description='Retrieve cutoffs for various colleges and/or branches', color=discord.Color.random())
    em.add_field(name = "Syntax: ", value = "</cutoff:1131246029531004968> `<college> <year> <ciwg> <round> [branch]`", inline = True)
    em.set_footer(text="This message will be deleted after 1 minute.")
    await ctx.send(embed = em, delete_after = 60)


@help.command()
async def airport(ctx):
    em = discord.Embed(
        title='</airport:1133054254203011082>', description='Retrieves closest airport to the given college', color=discord.Color.random())
    em.add_field(name="Syntax: ",
                 value="</airport:1133054254203011082> `<college>`", inline=True)
    em.set_footer(text="This message will be deleted after 1 minute.")
    await ctx.send(embed=em, delete_after = 60)


@help.command()
async def analyse(ctx):
    em = discord.Embed(
        title='</analyse:1131969029968502918>', description='Retrieve cutoffs closes to your rank', color = discord.Color.random())
    em.add_field(name="Syntax: ",
                 value="</analyse:1131969029968502918> `<rank ><ciwg> [branch]`", inline=True)
    em.set_footer(text="This message will be deleted after 1 minute.")
    await ctx.send(embed=em, delete_after=60)

@bot.event
async def on_ready():
    print("Bot is online")
    try:
        synched = await bot.tree.sync()
        print(f'Synched {len(synched)} command(s)')

    except Exception as e:
        print(e)

@bot.tree.command(name = 'ping')
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f'Pong! {round(bot.latency * 1000)}ms')

@bot.command(description='Reload a cog.')
@commands.is_owner()
async def reload(ctx, extension):
    try:
        await bot.reload_extension(f'cogs.{extension}')
        await ctx.send(f'`{extension}` `has been reloaded.`')
    except:
        await ctx.send("`Invalid module.`")

@bot.command(description='Turns off the bot.')
@commands.is_owner()
async def shut(ctx):
    await ctx.send('`Bot going offline!`👋')
    await bot.change_presence(status=discord.Status.offline)
    await bot.close()
    exit()

async def load():
    for file in os.listdir("DASABot\cogs"):
        if file.endswith(".py"):
            await bot.load_extension(f"cogs.{file[:-3]}")

async def main():
    await load()
    await bot.start(BOT_TOKEN)

asyncio.run(main())
