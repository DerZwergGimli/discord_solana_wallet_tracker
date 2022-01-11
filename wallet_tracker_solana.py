# wallet_tracker_solana.py
import asyncio

import os
from discord import guild
from loguru import logger
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


logger.add("file_{time}.log", format="{time} {level} {message}", filter="my_module", level="INFO")


intents = discord.Intents.default()
intents.members = False

bot = commands.Bot(command_prefix='$', description=description, help_command=None, intents=intents)

wallet = Wallet(WALLET_ADDRESS)


#def botUsername():
sleeptime = 10    

# Update Task
async def update_data_task():
    round = 0
    while True:
        wallet.fetchAll()
        for member in bot.get_all_members():
            text = f'💰 ${wallet.getTotalBalanceValueUSD(2)} 💰'
            await member.edit(nick=text)
        if round == 0:
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f" {wallet.getTotalBalanceValueName('USDC', 2)} 💵-USDC"))    
        elif round == 1:
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{wallet.getTotalBalanceValueName('ATLAS',2)} 💎-ATLAS"))    
        else:
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{wallet.getTotalBalanceValueName('POLIS',2)} 💎-POLIS")) 
            round = -1
        round +=1
        await asyncio.sleep(sleeptime)


#Intial 
@bot.event
async def on_ready():
    await bot.user.edit(username=BOT_NAME)
    logger.info('Connecting to discord!')
    logger.info(f'Logged in as {bot.user} [ID: {bot.user.id}]')
    bot.loop.create_task(update_data_task())
   

@bot.command()
async def usd(ctx):
    balance = wallet.getTotalBalanceValueUSD()
    await ctx.send(f'We have:\t {balance} 💵-USD')


@bot.command()
async def atlas(ctx):
    balance = wallet.getTotalBalanceValueName('ATLAS')
    await ctx.send(f'I found:\t {balance} 💎-ATLAS')


@bot.command()
async def polis(ctx):
    balance = wallet.getTotalBalanceValueName('POLIS')
    await ctx.send(f'I found:\t {balance} 💎-Polis')


@bot.command()
async def usdc(ctx):
    balance = wallet.getTotalBalanceValueName('USDC')
    await ctx.send(f'I found:\t {balance} 💎-USDC')


@bot.command()
async def report(ctx):
    embedVar = discord.Embed(title='🏴‍☠️ Treasury Report 🏴‍☠️', description='After watching closely i could find the following balances in the Guild-Wallet', color=0x00ff00)
    embedVar.add_field(name='💵 USDC-amount', value=f'\t {wallet.getTotalBalanceValueName("USDC", 1)}', inline=True)
    embedVar.add_field(name='💎 POLIS-amount', value=f'{wallet.getTotalBalanceValueName("POLIS", 1)}', inline=True)
    embedVar.add_field(name='💎 ATLAS-amount', value=f'{wallet.getTotalBalanceValueName("ATLAS",1) }', inline=True)
    embedVar.add_field(name='💰 TOTAL[USD]', value=f'{wallet.getTotalBalanceValueUSD()}', inline=True)
    await ctx.channel.send(embed=embedVar)


@bot.command()
async def step(ctx):
    await ctx.channel.send(f"🔗 https://app.step.finance/#/watch/{wallet.getWalletAddress()} 🔗")


@bot.command()
async def solanabeach(ctx):
    await ctx.channel.send(f"🔗 https://solanabeach.io/address/{wallet.getWalletAddress()} 🔗")


@bot.command()
async def address(ctx):
    await ctx.channel.send(f"{wallet.getWalletAddress()}")


@bot.command()
async def url(ctx):
    await ctx.channel.send(f"{wallet.getWalletURL()}")


@bot.command()
async def help(ctx):
    await ctx.channel.send("""
    Help-Commands:
    $usd     \t\t [show wallet total-balance in $USD live price Coingeko]
    $usdc   \t\t [show wallet amount $USDC]
    $polis   \t\t [show wallet amount $POLIS]
    $atlas   \t\t [show wallet amount $ATLAS]
    $report  \t    [creates a short balance report]
    $step  \t    [creates a step.finance handle]
    $solanabeach \t [creates a solanabeach handle]
    $address \t [show wallet solana-address-raw]
    $url \t [show wallet solana-address-url]""")


bot.run(TOKEN)