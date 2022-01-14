import discord
from discord.ext import commands
from src.SolanaWallet import SolanaWallet



def wallet_botCommads(bot, wallet:SolanaWallet):
    @bot.command()
    async def usd(ctx):
        balance = round(wallet.usd_value, 2)
        await ctx.send(f'We have:\t {balance} 💵-USD')

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
    
    @bot.command()
    async def report(ctx):
        embedVar = discord.Embed(title='🏴‍☠️ Treasury Report 🏴‍☠️', description='After watching closely i could find the following balances in the Guild-Wallet', color=0xffd700)
        embedVar.add_field(name='💵 USDC-amount', value=f'\t {wallet.get_tokenBalance("EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v", 2)}', inline=True)
        embedVar.add_field(name='💎 POLIS-amount', value=f'{wallet.get_tokenBalance("poLisWXnNRwC6oBu1vHiuKQzFjGL4XDSu4g9qjz9qVk", 2)}', inline=True)
        embedVar.add_field(name='💎 ATLAS-amount', value=f'{wallet.get_tokenBalance("ATLASXmbPQxBUYbxPsV97usA3fPQYEqzQBUHgiFCUsXx",2) }', inline=True)
        embedVar.add_field(name='💰 TOTAL[USD]', value=f'{round(wallet.usd_value, 2)}', inline=True)
        await ctx.channel.send(embed=embedVar)


    @bot.command()
    async def step(ctx):
        await ctx.channel.send(f"🔗 https://app.step.finance/#/watch/{wallet.walletaddress} 🔗")


    @bot.command()
    async def explorer(ctx):
        await ctx.channel.send(f"🔗 https://solanabeach.io/address/{wallet.walletaddress} 🔗")


    @bot.command()
    async def address(ctx):
        await ctx.channel.send(f"{wallet.walletaddress}")


    @bot.command()
    async def url(ctx):
        await ctx.channel.send(f"{wallet.walleturl}")
    
    @bot.command()
    async def spl(ctx, str_amount):
        try:
            amount = int(str_amount)
            count = 0
            while(amount):
                txs = wallet.spl_transfers
                await ctx.channel.send(f'{txs[count].signature}\t {txs[count].get_transferAmountFormated()} {txs[count].tokenSymbol}')
                amount -= 1
                count += 1
        except:
            await ctx.channel.send("Please use the format: '$spl <n>'")
    
    @bot.command()
    async def help(ctx):
        description_text = """```$usd \t\t\t[show wallet total-balance in $USD]
$usdc            [show wallet amount $USDC]
$polis           [show wallet amount $POLIS]
$atlas           [show wallet amount $ATLAS]
$report          [creates a short balance report]
$step            [creates a step.finance handle]
$explorer        [creates a solanabeach handle]
$address         [show wallet solana-address-raw]
$url             [show wallet solana-address-url]
$spl <n>         [pint n last spl-transactions]```
        """
        embedVar = discord.Embed(title="Help-Commands:", description=description_text, color=0xffd700)
        await ctx.send(embed=embedVar)