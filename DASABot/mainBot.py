import os
from connectRankDB import connectDB
from dotenv import load_dotenv

import discord
from discord.ext import commands

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = commands.Bot(command_prefix="?", intents=discord.Intents.all())

# Initialize the connectDB object
db = connectDB()

@bot.event
async def on_ready():
    print("Bot connected")

@bot.command()
async def cutoff(ctx):
    try:
        # Prompt user for year
        await ctx.send("Please enter the year:")
        year_msg = await bot.wait_for("message", check=lambda m: m.author == ctx.author)
        year = year_msg.content

        # Validate the year
        valid_years = ["2021", "2022"]
        while year not in valid_years:
            await ctx.send("Invalid year, re-enter")
            year_msg = await bot.wait_for("message", check=lambda m: m.author == ctx.author)
            year = year_msg.content

        # Prompt user for round
        await ctx.send("Please enter the round:")
        round_msg = await bot.wait_for("message", check=lambda m: m.author == ctx.author)
        round = round_msg.content

        # Validate the round
        valid_rounds = ["1", "2", "3"]
        while round not in valid_rounds:
            await ctx.send("Invalid round, re-enter")
            round_msg = await bot.wait_for("message", check=lambda m: m.author == ctx.author)
            round = round_msg.content

        # Prints college List
        college_list = db.request_college_list(year, round)
        colleges = "\n".join(college_list)  # Join the colleges into a single string
        await split_message(ctx, colleges)

        # Prompt user for college
        await ctx.send("Please enter the college:")
        college_msg = await bot.wait_for("message", check=lambda m: m.author == ctx.author)
        college = college_msg.content
        breaker = True
        while breaker:
            breaker = False
            try:
                college = db.nick_to_college(year, round, college)
            except ValueError:
                await ctx.send("Invalid college name, re-enter")
                breaker = True
                college_msg = await bot.wait_for("message", check=lambda m: m.author == ctx.author)
                college = college_msg.content

        # Prompt user for branch
        await ctx.send("Please enter the branch:")
        branch_msg = await bot.wait_for("message", check=lambda m: m.author == ctx.author)
        branch = branch_msg.content

        # Check if the branch is valid for the selected college
        branch_list = db.request_branch_list(year, round, college, False)  # Assuming CIWG status is False
        while branch.upper() not in branch_list:
            await ctx.send("Invalid branch name, re-enter")
            branch_msg = await bot.wait_for("message", check=lambda m: m.author == ctx.author)
            branch = branch_msg.content

        # Prompt user for CIWG status
        await ctx.send("Are you CIWG? (Y/N)")
        ciwg_msg = await bot.wait_for("message", check=lambda m: m.author == ctx.author)
        ciwg = ciwg_msg.content.lower() == "y"

        # Get the cutoff statistics
        stats = db.get_statistics(year, round, college, branch, ciwg)

        # Send the cutoff statistics as a response
        response = f"Cutoff for {college}, {branch}\n"
        response += f"JEE Opening Rank: {stats[0]}\n"
        response += f"JEE Closing Rank: {stats[1]}\n"
        response += f"DASA Opening Rank: {stats[2]}\n"
        response += f"DASA Closing Rank: {stats[3]}\n"

        await ctx.send(response)
    except ValueError as e:
        await ctx.send(str(e))


@bot.command()
async def rank(ctx):
    try:
        # Prompt user for rank
        await ctx.send("Please enter your rank:")
        rank_msg = await bot.wait_for("message", check=lambda m: m.author == ctx.author)
        rank = int(rank_msg.content)

        # Prompt user for year
        await ctx.send("Please enter the year:")
        year_msg = await bot.wait_for("message", check=lambda m: m.author == ctx.author)
        year = year_msg.content

        # Validate the year
        valid_years = ["2021", "2022"]
        while year not in valid_years:
            await ctx.send("Invalid year, re-enter")
            year_msg = await bot.wait_for("message", check=lambda m: m.author == ctx.author)
            year = year_msg.content

        # Prompt user for round
        await ctx.send("Please enter the round:")
        round_msg = await bot.wait_for("message", check=lambda m: m.author == ctx.author)
        round = round_msg.content

        # Validate the round
        valid_rounds = ["1", "2", "3"]
        while round not in valid_rounds:
            await ctx.send("Invalid round, re-enter")
            round_msg = await bot.wait_for("message", check=lambda m: m.author == ctx.author)
            round = round_msg.content

        # Prompt user for CIWG status
        await ctx.send("Are you CIWG? (Y/N)")
        ciwg_msg = await bot.wait_for("message", check=lambda m: m.author == ctx.author)
        ciwg = ciwg_msg.content.lower() == "y"

        # Prompt the user for branch
        await ctx.send("Which Branch?")
        branch_msg = await bot.wait_for("message", check=lambda m: m.author == ctx.author)
        branch = branch_msg.content.upper()

        # Get the cutoff statistics
        lowclg, midclg, highclg = db.analysis(rank, ciwg, branch)

        # Send the cutoff statistics as separate messages
        response = f"\n\nLow chances in: \n\n"
        response += "\n".join(lowclg)
        await split_message(ctx, response)

        response = f"\n\nMid chances in: \n\n"
        response += "\n".join(midclg)
        await split_message(ctx, response)

        response = f"\n\nHigh chances in: \n\n"
        response += "\n".join(highclg)
        await split_message(ctx, response)

    except ValueError as e:
        await ctx.send(str(e))

@bot.command()
async def dasahelp(ctx):
    """
    Displays information about the available commands and their usage.

    Usage: ?dasahelp
    """
    # Help message content
    help_message = """
    **Available Commands:**

    **1. Cutoff Command**
    Retrieves cutoff statistics for a specific college, branch, and round.

    Usage: `?cutoff`
    Follow the prompts to enter the required information.

    **2. Rank Command**
    Performs analysis based on the user's rank, CIWG status, and branch.

    Usage: `?rank`
    Follow the prompts to enter the required information.
    """

    # Send the formatted help message as a response
    await split_message(ctx, help_message)

# Splits the message into chunks to follow discord charecter limit
async def split_message(ctx, message):
    if len(message) <= 2000:
        await ctx.send(message)
    else:
        chunks = [message[i:i + 2000] for i in range(0, len(message), 2000)]
        for chunk in chunks:
            await ctx.send(chunk)


async def load():
    for file in os.listdir("DASABot/cogs"):
        if file.endswith(".py"):
            await bot.load_extension(f"cogs.{file[:-3]}")

bot.run(BOT_TOKEN)
