# bot.py
import os
import random
import discord.member
import tinydb
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions, CheckFailure, BadArgument
import os.path

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
bot = commands.Bot(command_prefix='yo ')


@bot.event
async def on_ready():
    print("up and running")


@bot.command(name='dev', help="your developer")
async def dev(ctx):
    await ctx.send('EY_Sviper#4342')


@bot.command(name='setup')
async def setup(ctx, type):
    newpath = r'./database/'+ctx.message.guild.name
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    if type == "welcome":
        await ctx.send("Type out the welcome message you want to be displayed: (btw the welcome message will show in "
                       "this channel. If you dont want it displayed gere, go to the channel you desire.")
        msg = await bot.wait_for('message', timeout=30, check=lambda message: message.author == ctx.author)
        db = tinydb.TinyDB("./database/"+ctx.message.guild.name+"/settings.json")
        argument = tinydb.Query()
        if db.contains(argument.type == "welcome"):
            db.update({"message":str(msg.content), "channel":msg.channel.id}, argument.type=="welcome")
            await ctx.send("updated message")
        else:
            db.insert({"type":"welcome", "channel":int(msg.channel.id), "message":str(msg.content)})
            await ctx.send("updated message")


@bot.command(name='warn', help='warns a user')
@has_permissions(administrator=True)
async def warn(ctx, user: str, arg: str):
    print("init")
    newpath = r'./database/'+ctx.message.guild.name
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    db = tinydb.TinyDB("./database/"+ctx.message.guild.name+"/warnings.json")
    db.insert({"username": user, "reason":arg})
    response = user + " has been warned for " + arg + " Don't be a bad boi."
    await ctx.send(response)


@bot.command(name='clear', help='clears channel, requires argument number')
@has_permissions(administrator=True)
async def clear(ctx, amount: int):
    response = str(amount) + " messages cleared"
    await ctx.channel.purge(limit=amount)
    await ctx.send(response)


@warn.error
async def warn_error(error, ctx):
    if isinstance(error, MissingPermissions):
        await ctx.send("no perms boi")


@bot.command(name='warnings', help="show all warnings a user has")
async def warn(ctx, usr: str):
    db = tinydb.TinyDB(ctx.message.guild.name)
    user = tinydb.Query()
    warnings = db.search(user.username == usr)
    number = len(warnings)
    response = str(usr) + " has " + str(number)+ " warnings till date."
    await ctx.send(response)


@bot.command(name='kick')
@commands.has_permissions(kick_members=True)
async def kick(ctx, kicked: discord.Member, *, reason=None):
    print(kicked)
    await kicked.kick(reason=reason)
    response = kicked + "has been kicked"
    await ctx.send(response)

bot.run(TOKEN)
