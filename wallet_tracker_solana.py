# wallet_tracker_solana.py
import asyncio

import os
from discord import guild
import requests

import discord
from discord import message
from discord.ext import tasks, commands
from dotenv import load_dotenv
from asyncio import sleep

from src.Wallet import Wallet



description = '''A Bot that will keep track of you wallet! '''

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
BOT_NAME = os.getenv('DISCORD_BOT_NAME')
WALLET_ADDRESS = os.getenv('DISCORD_WALLET_ADDRESS')

#client = discord.Client()

intents = discord.Intents.default()
intents.members = False

bot = commands.Bot(command_prefix='$', description=description, help_command=None, intents=intents)

mywallet = Wallet(WALLET_ADDRESS)

#def botUsername():
sleeptime = 5    

# Update Task
async def update_data_task():
    round = 0
    while True:
        mywallet.fetchAll()
        for member in bot.get_all_members():
            text = f'💰 {mywallet.getTotalBalanceValueUSD(2)}$ 💰'
            await member.edit(nick=text)
            print(f"CHANNEL{member}")
        if round == 0:
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f" {mywallet.getTotalBalanceValueName('USDC', 2)} 💵-USDC"))    
        elif round == 1:
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{mywallet.getTotalBalanceValueName('ATLAS',2)} 💎-ATLAS"))    
        else:
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{mywallet.getTotalBalanceValueName('POLIS',2)} 💎-POLIS")) 
            round = -1
        round +=1
        await asyncio.sleep(sleeptime)


#Intial 
@bot.event
async def on_ready():
    await bot.user.edit(username=BOT_NAME)
    print('[LOGS] Connecting to discord!')
    print(f'[LOGS] Logged in as {bot.user} [ID: {bot.user.id}]')
    bot.loop.create_task(update_data_task())
   

@bot.command()
async def usd(ctx):
    balance = mywallet.getTotalBalanceValueUSD()
    await ctx.send(f'We have:\t {balance} 💵-USD')


@bot.command()
async def atlas(ctx):
    balance = mywallet.getTotalBalanceValueName('ATLAS')
    await ctx.send(f'I found:\t {balance} 💎-ATLAS')


@bot.command()
async def polis(ctx):
    balance = mywallet.getTotalBalanceValueName('POLIS')
    await ctx.send(f'I found:\t {balance} 💎-Polis')


@bot.command()
async def report(ctx):
    embedVar = discord.Embed(title='🏴‍☠️ Treasry Report 🏴‍☠️', description='After watching closely i could find the following balances in the Guild-Wallet', color=0x00ff00)
    embedVar.add_field(name='💵  USDC', value=f'\t {mywallet.getTotalBalanceValueName("USDC", 1)}', inline=True)
    embedVar.add_field(name='💎 POLIS', value=f'{mywallet.getTotalBalanceValueName("POLIS", 1)}', inline=True)
    embedVar.add_field(name='💎 ATLAS', value=f'{mywallet.getTotalBalanceValueName("ATLAS",1) }', inline=True)
    embedVar.add_field(name='💰 TOTAL[USD]', value=f'{mywallet.getTotalBalanceValueUSD()}', inline=True)
    await ctx.channel.send(embed=embedVar)


@bot.command()
async def wallet(ctx):
    await ctx.channel.send(f"🔗 https://app.step.finance/#/watch/{mywallet.getWalletAddress()} 🔗")


@bot.command()
async def address(ctx):
    await ctx.channel.send(f"{mywallet.getWalletAddress()}")


@bot.command()
async def help(ctx):
    await ctx.channel.send("""
    Help-Commands:
    $usd     \t\t [show wallet total balance in $USD]
    $polis   \t\t [show wallet total $POLLIS]
    $atlas   \t\t [show wallet total $ATLAS]
    $report  \t    [creates a short balance report]
    $wallet  \t    [creates a step.finance handle]
    $address \t [show wallet solana-address-raw]""")


bot.run(TOKEN)