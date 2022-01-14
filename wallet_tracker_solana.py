from email import message
import os
from random import randint
from loguru import logger
from dotenv import load_dotenv
import asyncio
import discord
from discord.ext import commands
from discord.ext import tasks

from src.SolanaWallet import SolanaWallet
from src.SplTransfer import SplTransfer
from wallet_botCommads import wallet_botCommads

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
BOT_NAME = os.getenv('DISCORD_BOT_NAME')
WALLET_ADDRESS = os.getenv('DISCORD_WALLET_ADDRESS')
WALLET_URL = os.getenv('DISCORD_WALLET_URL')

logger.add("file_{time}.log", format="{time} {level} {message}", level="INFO")
description = '''A Bot that will keep track of a wallet! '''
bot = commands.Bot(command_prefix='$', description=description, help_command=None)
wallet = SolanaWallet(walletaddress=WALLET_ADDRESS, walleturl=WALLET_URL)

wallet.fetch()
wallet.printWallet()

# @tasks.loop(seconds=10)
@tasks.loop(seconds=15)
async def updateWallet_Task():
    # await asyncio.sleep(20)
    try:
        wallet.fetch()
    except:
        logger.error("Bot could not fetch Wallet")
    logger.debug("Updated wallet!")

@tasks.loop(seconds=5)
async def updateStatus_Task():
    try:
        try:
            bot_name_text = f'💰 $~{wallet.get_usdValue(2)} 💰'
        except:
            logger.warning("...unable to read wallet balance...")
            bot_name_text = "...checking..."
        for server in bot.get_all_members():
            try:
                await server.edit(nick=bot_name_text)
            except:
                logger.warning("unable to change bot name!")
        random = randint(1,3)
        if random == 1:
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f" {wallet.get_tokenBalance('EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v',2)} 💵-USDC"))
        elif random == 2:
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{wallet.get_tokenBalance('ATLASXmbPQxBUYbxPsV97usA3fPQYEqzQBUHgiFCUsXx',2)} 💎-ATLAS"))
        else:
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{wallet.get_tokenBalance('poLisWXnNRwC6oBu1vHiuKQzFjGL4XDSu4g9qjz9qVk',2)} 💎-POLIS"))
        print(f'random:{random}')
        logger.debug("Updated BOT!")
    except:
        logger.error("UpdateBOT problem!")
        pass

@tasks.loop(seconds=10)
async def updateTransactions_Task():
    ids = os.getenv('DISCORD_CHANNEL_TO_POST_TX').split(',')

    wallet.checkTransferList()
    txs = wallet.spl_transfers
    tx : SplTransfer
    for tx in txs:
        if tx.isLogged == False:
            for id in ids:
                channel = bot.get_channel(int(id))
                try:
                    embedVar = discord.Embed(title='ℹ️ TX Notification ℹ️', description='A SPL-Transaction was found!', color=0xffd700)
                    if(tx.changeType == 'inc'):
                        name = f"+{tx.get_transferAmountFormated()} {tx.tokenSymbol}"
                        value = 'have entered the wallet!'
                    if(tx.changeType == 'dec'):
                        name = f"{tx.get_transferAmountFormated()} {tx.tokenSymbol}"
                        value = 'have left the wallet!'
                    embedVar.add_field(name=name, value=value, inline=False)
                    embedVar.add_field(name="TX-Signature", value=f'{tx.signature[0]}')
                    await channel.send(embed=embedVar)
                except:
                    logger.error("Unable to write TX into a channel!")
    wallet.saveTransferList()
    logger.debug('Updated TXs!')


@bot.event
async def on_ready():
    logger.info(f'Bot logged as {bot.user}')
    updateWallet_Task.start()
    updateStatus_Task.start()
    updateTransactions_Task.start()

wallet_botCommads(bot, wallet)

logger.info("Stared!")
bot.run(TOKEN)
