from loguru import logger
import os
from dotenv import load_dotenv
from src.SplTransfer import SplTransfer
from src.SolanaWallet import SolanaWallet
from src.SolscanAPI import SolscanAPI
from src.Wallet import Wallet


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
BOT_NAME = os.getenv('DISCORD_BOT_NAME')
WALLET_ADDRESS = os.getenv('DISCORD_WALLET_ADDRESS')
WALLET_URL = os.getenv('DISCORD_WALLET_URL')


#logger.add("file_{time}.log", format="{time} {level} {message}", level="INFO")

#wallet = Wallet(walletaddress=WALLET_ADDRESS, walleturl=WALLET_URL)
wallet = SolanaWallet(walletaddress=WALLET_ADDRESS, walleturl=WALLET_URL)
wallet.fetch()
wallet.printWallet()


print("----")
spl = SplTransfer("111", "222", "333")
spl.printTransfer()


#wallet.fetchAll()
#wallet.printWallet()

#SolscanAPI.get_lastSPLtransfer(wallet.getWalletAddress())
#tokens = SolscanAPI.get_account_tokens(wallet.getWalletAddress())
#for t in tokens:
#    print(f'{t.address}\t {t.short_name} \t {t.amount}')