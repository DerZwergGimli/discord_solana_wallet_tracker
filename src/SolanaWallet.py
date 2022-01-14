from loguru import logger
from src.SolscanAPI import SolscanAPI
from src.CoingeckoAPI import CoingeckoAPI
from src.file_helper import read_file_to_json, write_json_to_file
from src.Token import Token
from src.SplTransfer import SplTransfer
from src.SolanaAPI import API
"""
This is a Object that represents a SolanaWallet
"""

path_tokenlist = "./token-list.json"

class SolanaWallet:
    def __init__(self, walletaddress: str, walleturl: str = ''):
        self.walletaddress = walletaddress
        self.solbalance = None
        self.tokens : Token = []
        self.spl_transfers : SplTransfer = []
        j_tokenlist = read_file_to_json(path_tokenlist)
        self.walleturl = walleturl
        self.usd_value = 9.0
    
    def fetch(self):
        self.tokens = SolscanAPI.get_account_tokens(self.walletaddress)
        self.spl_transfers = SolscanAPI.get_splTransfers(self.walletaddress, 10)
        
        self.usd_value = 0.0
        for token in self.tokens:
            if token.coingecko:
                value = CoingeckoAPI.getTokenPrice('solana', token.address[0], 'usd')
                if value != None:
                    self.usd_value += value*token.amount

    def get_tokenBalance(self, tokenAddress:str, decimals:int = 0):
        for token in self.tokens:
            if token.address == tokenAddress:
                return round(token.amount, decimals)

    def printWallet(self):
        print('Wallet Info:')
        print(f'Address: {self.walletaddress}')
        print(f'SOL -> {self.solbalance}')
        
        token: Token
        for token in self.tokens:
            token.printToken()
    
        transfer: SplTransfer
        for transfer in self.spl_transfers:
            transfer.printTransfer()

    def saveTransferList(self):
        json_data = []
        for tx in self.spl_transfers:
            json_data.append(tx.signature)
        write_json_to_file('spl_list.json', json_data)
    
    def checkTransferList(self):
        json_data = read_file_to_json('spl_list.json')
        for tx in self.spl_transfers:
            for data in json_data:
                if tx.signature == data:
                    tx.isLogged = True