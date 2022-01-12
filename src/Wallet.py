from loguru import logger
from src.CoingekoAPI import CoingekoAPI
from src.file_helper import read_file_to_json
from src.Token import Token
from src.SolanaAPI import API
"""
This is a Object that represents a SolanaWallet
"""

path_tokenlist = "./token-list.json"

class Wallet:
    def __init__(self, walletaddress: str, walleturl: str = ''):
        self.walletaddress = walletaddress
        self.solbalance = None
        self.tokens = []
        j_tokenlist = read_file_to_json(path_tokenlist)
        for token in j_tokenlist['tokens']:
            self.tokens.append(
                Token(token['address'],
                        -1,
                        token['short_name'],
                        token['cg_price']))
        self.walleturl = walleturl

    def fetchAll(self):
        self.fetchBalance()
        self.fetchTokenBalance()
        self.fetchTokenPrices()

    def fetchBalance(self):
        logger.info('Fetching Wallet-Balance...')
        self.solbalance = API.getBalane(self.walletaddress)

    def fetchTokenBalance(self):
        logger.info('Fetching Token-Balance...')
        for token in self.tokens:
            token.amount = API.getTokenAccountBalance(self.walletaddress, token.address)

    def fetchTokenPrices(self):
        logger.info('Fetching Token-Pirces...')
        for token in self.tokens:
            if(token.cg_price):
                try:
                    token.value_in_usd = token.amount * CoingekoAPI.getTokenPrice('solana', token.address, 'usd')
                except:
                    logger.error('Unable to fetch usd value')
            else: 
                token.value_in_usd = token.amount

    
    def sumWalletInUSDC(self):
        sum = 0
        for token in self.tokens:
            sum += token.value_in_usd
        print(f'Sum Wallet in usdc = {sum}')

    # Public
    def printWallet(self):
        print('Wallet Info:')
        print(f'Address: {self.walletaddress}')
        print(f'SOL -> {self.solbalance}')

        for token in self.tokens:
            print(f'-{token.short_name} \t -> {token.amount} \t usd={token.value_in_usd}')
    
    def getWalletAddress(self):
        return self.walletaddress

    def getWalletURL(self):
        return self.walleturl
    
    def getTotalBalanceValueUSD(self, ndigits:int = 2):
        sum = 0
        for token in self.tokens:
            sum += token.value_in_usd
        return round(sum, ndigits)

    def getTotalBalanceValueName(self, short_name:str, ndigits:int = 2):
        amount = 0
        for token in self.tokens:
            if(token.short_name == short_name):
                amount = token.amount
        return round(amount, ndigits)
    
    