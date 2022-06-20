# package imports
import discord
from discord.ext import commands,tasks
from discord.commands import Option, permissions
from dotenv import load_dotenv, find_dotenv
from os import getenv

# file imports
from other_files import logging, helpfile, c_upscale


# load dotenv and logging
load_dotenv(find_dotenv())

# version and constants
__version__ = '0.2.0a'
__changelog__ = f"""
**{__version__} Changelog**
----------------
- Reworked entire API
"""
BACKUP_CHANNEL_ID = 972541376375975996

# connect to client and bot
intents = discord.Intents.default()
bot = commands.Bot(debug_guilds=[739630717159473192],command_prefix='.', intents=intents, help_command=None)


# on bot ready
@bot.event
async def on_ready():
    print("Logged in as {0.user}".format(bot))
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(f"UB_DevB V{__version__}"))
    #TODO: Fix Loggin
    logging.log(f"Logged in as {bot.user}")

#task loop comes here
@tasks.loop(hours=24.0) #this task will upload the database as a backup every 24 hours
async def upload_db():
    global bot
    id = bot.get_channel(BACKUP_CHANNEL_ID) # 972541376375975996 is the channel id of #db-backups in the Ska's bots server
    await id.send(file=discord.File('db.json'))
    await id.send(file=discord.File('log.txt'))
@upload_db.before_loop
async def before_upload_db():
    global bot
    await bot.wait_until_ready()


# info command
@bot.slash_command()
async def ping(ctx):
    """Get bot ping and basic info"""
    await ctx.respond(f"UpscaleBot V{__version__}: ({round((bot.latency * 1000))}ms)\n{__changelog__}")
    logging.log(f"{ctx.author} used ping command")
    
# help command
@bot.slash_command()
async def help(ctx):
    """Get help with commands"""
    #TODO: Remake help command
    await helpfile.help(ctx,__version__)
    logging.log(f"{ctx.author} used help command")


# upscale command
@bot.slash_command()
async def upscale(ctx,
    image: Option(  # this is the attachment option, aka where you have to add your image
        discord.Attachment,
        "The image you want to upscale",
        required=True), 
    amount: Option(  # this is the amount option, aka the amount of times you want to upscale
        str,
        "The amount of times you want to upscale",
        choices=['2x','4x'], #! ,'8x','16x' are temporarily disabled
        required=False),
    noise_reduction: Option(  # this is the Noise_reduction option, aka the amount of noise to remove
        str,
        "How much noise reduction the upscale should have",
        choices=['None','Low','Medium','High','Highest'], #! Warning; 'None' (type=str) is No noise whilst None (type=NoneType) is no option entered
        required=False),
    model: Option(  # this is the model option, aka which upscaling model to use
        str,
        "The model that should be used, art for drawings/anime, photo for irl images",
        choices=['Art','Photo'],
        required=False),
    ):
    """Upscale your images"""
    #TODO: Complete upscaling rework
    await c_upscale.upscale(ctx=ctx, image=image, x2=amount, noise=noise_reduction, model=model)

# * This command is temporarily disabled
# ban command
@bot.slash_command(guild_ids=[739630717159473192]) #! Do not remove the guild_ids!
async def ban_user(ctx,
    user: Option( # this is image option, aka which image is infringing
        str,  
        "The image that infringes the ToS",
        required=True),
    time: Option(  # this is the time option, aka the time you want to ban the user for
        str,
        "The time you want to ban the user for",
        choices=['1 week','1 month','3 months','1 year','Permanent'],
        required=True),
    reason: Option(  # this is the reason option, aka the reason you want to ban the user)
        str,
        "The reason you want to ban the user",
        required=False)):
    """Ban a user"""
    #TODO: Completely rework ban system
    #await command_ban.permanent(ctx, user,time,reason)
    await ctx.respond(f"This command is temporarily disabled")

#! Remove in main build
#test command
@bot.slash_command()
async def test(ctx):
    """Test command"""
    await ctx.respond("Test command")


#start the tasks
upload_db.start()

# get bot token and run bot
#TODO: Fix token
token = getenv('bot_token')
bot.run(token)