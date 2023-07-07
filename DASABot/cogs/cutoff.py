import connectRankDB

import discord
from discord.ext import commands

class Select (discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label = "option1", emoji= " ", description="yeaaa boi"),
            discord.SelectOption(label = "option2", emoji= " ", description="noooo boi"),
            discord.SelectOption(label = "option3", emoji= " ", description="maybe boi")
        ]
        super().__init__(placeholder="Choose an option", max_values=1, min_values=1, options=options)

        async def callback(self, interaction : discord.Interaction):
            user = interaction.user
            guild = interaction.guild

            if self.values[0] == "option1":
                print("option 1 chosen")
            if self.values[1] == "option2":
                print("option 2 chosen")
            if self.values[2] == "option3":
                print("user is a retard")


class SelectView(discord.ui.View):
    def __init__ (self, *, timeout=30):
        super().__init__(timeout=timeout)
        self.add_item(Select())


class cutoff(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.dbconnect = connectRankDB.connectDB()

    @commands.Cog.listener()
    async def on_ready(self):
        print("cutoff cog loaded")
    
    @commands.command()
    async def cutoff(self, ctx):
        print("cutoff yeahhhh")
        await ctx.send("Choose from the following:", view = SelectView(), delete_after=15)

async def setup(bot):
    await bot.add_cog(cutoff(bot))