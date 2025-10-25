from discord.ext import commands

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
        
    @commands.command()
    async def help(self, ctx):
        print("yep")
        await ctx.send("""
$aip evaluate [model name] - depending on model, result can be diffrent
$aip list - lists all models implemented into bot
$aip structure [model name] [version name] - gives advanced description about model structure
                       """)
        
async def setup(bot):
    await bot.add_cog(General(bot))