import connectRankDB
from connectRankDB import connectDB
import discord
from discord.ext import commands
import Paginator
db = connectDB()


class DASACommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.dbconnect = connectRankDB.connectDB()

    @commands.Cog.listener()
    async def on_ready(self):
        print("DASA COMMANDS cog loaded")

    @commands.command()
    async def cutoff(self, ctx, college: str, year: str, ciwg: str, round: str,  branch: str = None):
        """Get cutoffs.
                usage : ?cutoff <college>, <year>, <ciwg>, <round> [,branchcode]"""
        college = college.lower()
        if year not in ['2021', '2022']:  # checks if the year is given as 2021 or 2022
            return await ctx.send("Invalid year.")

        """await ctx.send('Which Round?(1,2,3): ')
		round_msg = await self.bot.wait_for("message", check=lambda m: m.author == ctx.author)
		round = str(round_msg.content)"""

        if int(round) not in [1, 2, 3]:  # checks if the round is 1,2 or 3
            await ctx.send("Invalid round.")
            return

        """await ctx.send('CIWG?(y/n): ')
		ciwg_msg = await self.bot.wait_for("message", check=lambda m: m.author == ctx.author)
		ciwg = ciwg_msg.content"""

        if ciwg.lower() not in "yn":
            await ctx.send("Invalid Category.")

        try:
            college = db.nick_to_college(str(year), str(round), str(college))
        except:
            return await ctx.send("Invalid college name.")

        ciwg = True if ciwg == 'y' else False
        branch_list = db.request_branch_list(year, round, college, ciwg)

        if branch is not None:
            if ciwg:
                branch = f"{branch.upper()}1"
            while branch.upper() not in branch_list:
                await ctx.send("Invalid branch name, re-enter. Press Q to Quit.")
                branch_msg = await self.bot.wait_for("message", check=lambda m: m.author == ctx.author)
                branch = branch_msg.content
                if branch == 'Q':
                    return await ctx.send('Quitting...')

            stats = db.get_statistics(
                year, round, college, branch.upper(), ciwg)
            embed = discord.Embed(
                title=f'Cutoffs for {college}',
				description=f'Course: {branch[:-1]} (CIWG)\n Round {round}' if ciwg else f'Course: {branch.upper()}\n Round {round}',
				color=discord.Color.random())
            embed.set_thumbnail(
                url='https://dasanit.org/dasa2023/images/dasa_new.png')
            embed.add_field(name="JEE Opening Rank: ", value=stats[0])
            embed.add_field(name="JEE Closing Rank: ", value=stats[1])
            embed.add_field(
                name="DASA Opening Rank: " if not ciwg else f"CIWG Opening Rank: ", value=stats[2])
            embed.add_field(
                name="DASA Closing Rank: " if not ciwg else f"CIWG Closing Rank: ", value=stats[3])
            await ctx.send(embed=embed)

        else:
            stats = db.get_statistics_for_all(year, round, college, ciwg)
            embed = discord.Embed(
                title=f"Cutoffs for {college}", description=f"Round {round}", color=discord.Color.random())
            embed.set_thumbnail(
                url='https://dasanit.org/dasa2023/images/dasa_new.png')
            for i in stats:
                if ciwg == False:
                    embed.add_field(
                        name=i[0],
                        value=f"JEE OPENING: {i[1][0]}\nJEE CLOSING: {i[1][1]}\nDASA OPENING: {i[1][2]}\nDASA CLOSING: {i[1][3]}",
                        inline=True)
                else:
                    embed.add_field(
                        name=f"{i[0][:-1]} (CIWG)",
                        value=f"JEE OPENING: {i[1][0]}\nJEE CLOSING: {i[1][1]}\nCIWG OPENING: {i[1][2]}\nCIWG CLOSING: {i[1][3]}",
                        inline=True)

            await ctx.send(embed=embed)

    @commands.command()
    async def rank(self, ctx, rank: int, ciwg: str, branch: str):
        if rank < 0:
            await ctx.send("Invalid rank.")
            return
        if ciwg.lower() not in "yn":
            await ctx.send("Invalid Category.")
        branch = branch.upper()
        lowclg, midclg, highclg = db.analysis(rank, True if ciwg == 'y' else False, branch)

        lowemb = discord.Embed(title=f"Low Chances for {branch} in: ", color = discord.Color.random())
        for num, name in enumerate(lowclg,1):
            lowemb.add_field(
                name=f"{num}. {name.split('Clos')[0]}", value=f"Clos{name.split('Clos')[1]}")

        midemb = discord.Embed(title=f"Mid Chances for {branch} in: ", color = discord.Color.random())
        for num, name in enumerate(midclg, 1):
            midemb.add_field(name=f"{num}. {name.split('Clos')[0]}", value=f"Clos{name.split('Clos')[1]}")
        highemb = discord.Embed(title=f"High Chances for {branch} in: ", color = discord.Color.random())
        for num, name in enumerate(highclg, 1):
            highemb.add_field(name=f"{num}. {name.split('Clos')[0]}", value=f"Clos{name.split('Clos')[1]}")
        embs = [lowemb, midemb, highemb]

        await Paginator.Simple(timeout = 60, PageCounterStyle = discord.ButtonStyle.blurple).start(ctx, pages=embs)


async def setup(bot):
    await bot.add_cog(DASACommands(bot))
