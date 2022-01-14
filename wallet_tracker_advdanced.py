import os
from loguru import logger
from dotenv import load_dotenv
import asyncio
import discord
from discord.ext import commands
from discord.ext import tasks

from src.SolanaWallet import SolanaWallet

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
BOT_NAME = os.getenv('DISCORD_BOT_NAME')
WALLET_ADDRESS = os.getenv('DISCORD_WALLET_ADDRESS')
WALLET_URL = os.getenv('DISCORD_WALLET_URL')

# logger.add("file_{time}.log", format="{time} {level} {message}", level="INFO")

bot = commands.Bot(command_prefix='$')
wallet = SolanaWallet(walletaddress=WALLET_ADDRESS, walleturl=WALLET_URL)

wallet.fetch()
wallet.printWallet()


#@tasks.loop(seconds=10)
@tasks.loop()
async def updateWallet_Task():
    await asyncio.sleep(10)
    wallet.fetch()
    logger.debug("Updated wallet!")


@tasks.loop()
async def updateStatus_Task():
    round = 0
    while True:
        #wallet.fetch()
        try:
            await asyncio.sleep(3)
            try:
                print(wallet.usd_value)
                bot_name_text = f'💰 ${wallet.usd_value} 💰'
            except:
                logger.warning("...unable to read wallet balance...")
                bot_name_text="...checking..."
            for server in bot.get_all_members():
                try:
                    await server.edit(nick=bot_name_text)
                except:
                    logger.warning("unable to change bot name!")
            if round == 0:
                await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f" {wallet.get_tokenBalance('EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v',2)} 💵-USDC"))
            elif round == 1:
                await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{wallet.get_tokenBalance('ATLASXmbPQxBUYbxPsV97usA3fPQYEqzQBUHgiFCUsXx',2)} 💎-ATLAS"))
            else:
                await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{wallet.get_tokenBalance('poLisWXnNRwC6oBu1vHiuKQzFjGL4XDSu4g9qjz9qVk',2)} 💎-POLIS"))
                round = -1
            round += 1
        except:
            logger.error("UpdateBOT problem!")
            pass


@bot.event
async def on_ready():
    logger.info(f'Bot logged as {bot.user}')


@bot.command()
async def atlas(ctx):
    balance = wallet.get_tokenBalance(
        'ATLASXmbPQxBUYbxPsV97usA3fPQYEqzQBUHgiFCUsXx', 2)
    await ctx.send(f'💎 Total:\t{balance} $ATLAS')


@bot.command()
async def polis(ctx):
    balance = wallet.get_tokenBalance(
        'poLisWXnNRwC6oBu1vHiuKQzFjGL4XDSu4g9qjz9qVk', 2)
    await ctx.send(f'💎 Total:\t{balance} $POLIS')


@bot.command()
async def usdc(ctx):
    balance = wallet.get_tokenBalance(
        'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v', 2)
    await ctx.send(f'💎 Total:\t{balance} $USDC')


# bot.loop.create_task(monitor())


#bot.loop.create_task(updateStatus_Task())
#bot.loop.create_task(updateWallet_Task())

updateWallet_Task.start()
updateStatus_Task.start()
token = 'OTMxMzMzMTg5NTg5NDI2MjA3.YeC5nw.HPttVnHBJNppt_Dw0QEh4q34Xug'

logger.info("Stared!")
bot.run(token)
