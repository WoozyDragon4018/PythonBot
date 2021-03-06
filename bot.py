import discord
from discord.ext import commands, tasks
import os
import random
import json
from discord.utils import get
from itertools import cycle

extension_file = "extensions.json"
with open(extension_file) as file:
    extensions = json.load(file)["extensions"]


def get_prefix(bot, msg):
    prefixes = ['?']

    return commands.when_mentioned_or(*prefixes)(bot, msg)

bot=commands.Bot(case_insensitive=True,command_prefix=get_prefix)
bot.remove_command('help')

status = cycle(['PyBot v1.0!', 'with WoozyDragon', 'Age of Empire', 'Corn Hub', 'At your service!', '?help | \'send help plz\''])

@bot.listen()
async def on_ready():
    change_status.start()
    print("Bot is ready for action")

@tasks.loop(seconds=12)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))

@bot.listen()
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name='Members')
    await member.add_roles(role)
    channel = discord.utils.get(member.guild.channels, name='new-members')
    embed = discord.Embed(color=0xFFFF)
    embed.set_author(name='Welcome to the Server!')
    embed.add_field(name=f'New member!', value=f'{member} has joined this server!', inline=False)
    await channel.send(embed=embed)

@bot.command()
async def help(ctx):
    embed=discord.Embed(color=0xFFFF)
    embed.set_author(name='PyBot Help')
    embed.add_field(name='?modhelp', value='Help for Moderator Commands', inline=False)
    embed.add_field(name='?calchelp', value='Help for Calculator Commands', inline=False)
    embed.add_field(name='?pms', value='PyBot Messaging Service (PMS) [?pms @<user.mention> <your_message_here>]', inline=False)
    embed.add_field(name='?coinflip', value='Flips a coin for you', inline=False)
    embed.add_field(name='?diceroll', value='Rolls a dice', inline=False)
    embed.add_field(name='?suggest', value='Suggest for the server [?suggest <suggestion>]', inline=False)
    embed.set_footer(text='PyBot v1')
    await ctx.send(embed=embed)

@bot.command()
async def calchelp(ctx):
    embed=discord.Embed(color=0x00ff00)
    embed.set_author(name='PyBot Calculator Help')
    embed.add_field(name='?a', value='Addition [?a 11 12]', inline=False)
    embed.add_field(name='?s', value='Subtraction [?s 15 13]', inline=False)
    embed.add_field(name='?m', value='Multiplication [?m 15 13]', inline=False)
    embed.add_field(name='?d', value='Division [?d 15 13]', inline=False)
    await ctx.send(embed=embed)

@commands.has_role("Staff")
@bot.command()
async def modhelp(ctx):
    embed=discord.Embed(color=0x0000ff)
    embed.set_author(name='PyBot Moderation Help')
    embed.add_field(name='?purge', value='Mass deletes messages [?purge 11]', inline=False)
    embed.add_field(name='?warn', value='Warns the mentioned user [?warn @<user> <reason>]', inline=False)
    embed.add_field(name='?kick', value='Kicks the mentioned user [?kick @<user> <reason>]', inline=False)
    embed.add_field(name='?ban', value='Bans the mentioned user [?ban @<user> <reason>]', inline=False)
    await ctx.send(embed=embed)

#Calculator!
#Addition...
@bot.command()
async def a(ctx, numi, numii):
    sum_value = int(numi) + int(numii)
    await ctx.send(str(numi) + ' + ' + str(numii) + ' = ' + str(sum_value))

#Multiplication
@bot.command()
async def m(ctx, numi, numii):
    sum_value = int(numi) * int(numii)
    await ctx.send(str(numi) + ' x ' + str(numii) + ' = ' + str(sum_value))

#Subtraction
@bot.command()
async def s(ctx, numi, numii):
    sum_value = int(numi) - int(numii)
    await ctx.send(str(numi) + ' - ' + str(numii) + ' = ' + str(sum_value))

#Division
@bot.command()
async def d(ctx, numi, numii):
    sum_value = int(numi) / int(numii)
    await ctx.send(str(numi) + ' / ' + str(numii) + ' = ' + str(sum_value))

@commands.has_role("Staff")
@bot.command()
async def clear(ctx,amount:int=0):
    if ctx.author.guild_permissions.manage_messages:
        await ctx.channel.purge(limit=amount+1)
        await ctx.send(f"{amount} message has been deleted."if(int(amount)is 1)else(f"{amount} messages have been deleted."),delete_after=5)
        channel = bot.get_channel(652152328144551965)
        embed = discord.Embed(color=0xFFFFFF)
        embed.set_author(name='Mod Command Used!')
        embed.add_field(name='Clear Command used', value=f'{ctx.author.mention} has used `purge` command.')
        await channel.send(embed=embed)

@bot.command()
async def coinflip(ctx):
    flip = [
        'You got **heads**',
        'You got **tails**'
    ]

    await ctx.send(random.choice(flip))

@bot.command()
async def diceroll(ctx):
    roll = [
        '1','2','3','4','5','6'
    ]

    await ctx.send(random.choice(roll))

@commands.has_role("Staff")
@bot.command()
async def warn(ctx, user: discord.User, *, reason=None):
    await ctx.channel.purge(limit=1)
    embeda = discord.Embed(color=0xFFFF)
    embeda.set_author(name=f'Warning')
    embeda.add_field(name='You were warned in The kingdom for :', value=reason, inline=False)
    await user.send(embed=embeda)
    await ctx.send(str(user) + ' has succesfully been warned for ' + reason)
    channel = bot.get_channel(652152328144551965)
    embed = discord.Embed(color=0xFFFFFF)
    embed.set_author(name='Mod Command Used!')
    embed.add_field(name='Warn Command used', value=f'{ctx.author} has warned ' + str(user), inline=False)
    embed.add_field(name='Reason : ', value=reason, inline=False)
    await channel.send(embed=embed)

@bot.command()
async def pms(ctx, user: discord.User, *, message=None):
    embed = discord.Embed(color=0xffc0cb)
    embed.set_author(name='You got Mail!')
    embed.add_field(name='Message contents :-', value=message, inline=False)
    embed.add_field(name='Sender :-', value=f'{ctx.author.mention}', inline=False)
    embed.set_footer(text='PyBot Messaging Service (PMS)')
    await user.send(embed=embed)
    await ctx.send(f'{ctx.author.mention}, Succesfully sent your message to ' + str(user) + ' which says : ' + str(message))

@bot.command(pass_context = True)
async def suggest(ctx, *, suggest=None):
    await ctx.channel.purge(limit=1)
    channel = bot.get_channel(652146474037149706)
    embed = discord.Embed(color=0xffff00)
    embed.set_author(name=f'{ctx.author}')
    embed.add_field(name='Suggestion:', value=suggest, inline=False)
    embed.set_footer(text='PyBot Suggestions')
    await channel.send(embed=embed)

@commands.has_role("Staff")
@bot.command()
async def kick(ctx, user:discord.Member, *, reason=None):
    embeda = discord.Embed(color=0xFFFF)
    embeda.set_author(name='Kicked!')
    embeda.add_field(name='You were kicked from The kingdom for :', value=reason, inline=False)
    await user.send(embed=embeda)
    await user.kick(reason=reason)
    await ctx.send(str(user) + ' has succesfully been kicked for : ' + reason)
    channel = bot.get_channel(652152328144551965)
    embed = discord.Embed(color=0xFFFFFF)
    embed.set_author(name='Mod Command Used!')
    embed.add_field(name='Kick Command used', value=f'{ctx.author} has kicked ' + str(user), inline=False)
    embed.add_field(name='Reason : ', value=reason, inline=False)
    await channel.send(embed=embed)

@commands.has_role("Staff")
@bot.command()
async def ban(ctx, user:discord.Member, *, reason=None):
    embeda = discord.Embed(color=0xFFFF)
    embeda.set_author(name='Banned!')
    embeda.add_field(name='You were Banned from The kingdom for :', value=reason, inline=False)
    await user.send(embed=embeda)
    await user.ban(reason=reason)
    await ctx.send(str(user) + ' has succesfully been banned for : ' + reason)
    channel = bot.get_channel(652152328144551965)
    embed = discord.Embed(color=0xFFFFFF)
    embed.set_author(name='Mod Command Used!')
    embed.add_field(name='Ban Command used', value=f'{ctx.author} has banned ' + str(user), inline=False)
    embed.add_field(name='Reason : ', value=reason, inline=False)
    await channel.send(embed=embed)

@bot.listen()
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(color=0xff0000)
        embed.set_author(name='Error!')
        embed.add_field(name='Command Not Found!', value='The command you requested for was not found in the code, please refer to `?help` for my commands!', inline=False)
        await ctx.send(embed=embed)

    if isinstance(error, commands.CheckFailure):
        embed = discord.Embed(color=0xff0000)
        embed.set_author(name='Error!')
        embed.add_field(name='Permissions', value='You don\'t have the permissions to run this command!', inline=False)
        await ctx.send(embed=embed)



if len(extensions) > 0:
    for ext in extensions:
        try:
            bot.load_extension(ext)
            print(f"Extension {ext} loaded successfully")
        except Exception:
            print(f"Extension {ext} failed to load")

bot.run(os.getenv('token'))
