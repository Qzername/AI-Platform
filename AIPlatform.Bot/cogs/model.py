from discord.ext import commands
import model_handler 

class Model(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def evaluate(self, ctx, *args):
        model_name = args[0]
        
        model = model_handler.model_collection[model_name]
        await model["handler"].handle(ctx, model)
        
    @commands.command()
    async def list(self, ctx):
        final_message = ""
        
        for k,v in model_handler.model_collection.items():
            final_message += "# " + k + "\nDescription: " + v["description"] + "\n"
            
            final_message += "\nversions:\n"

            for version in v["versions"]:
                final_message += "- " + version + "\n"

        await ctx.send(final_message)

    @commands.command()
    async def structure(self, ctx, *args):
        model_name = args[0]
        model_version = args[1]

        version = model_handler.model_collection[model_name]["versions"][model_version]

        await ctx.send(version["structure"])


async def setup(bot):
    await bot.add_cog(Model(bot))