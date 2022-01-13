from loguru import logger
from src.SolscanAPI import SolscanAPI
from src.CoingekoAPI import CoingekoAPI
from src.file_helper import read_file_to_json
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
    
    def fetch(self):
        self.tokens = SolscanAPI.get_account_tokens(self.walletaddress)
        self.spl_transfers = SolscanAPI.get_splTransfers(self.walletaddress)
    
    def printWallet(self):
        print('Wallet Info:')
        print(f'Address: {self.walletaddress}')
        print(f'SOL -> {self.solbalance}')
        
        token: Token
        for token in self.tokens:
            token.printToken()
    
        transfer: SplTransfer
        for transfer in self.spl_transfers:
            print(transfer.address)
            transfer.printTransfer()
            #print(f'\t{transfer.tid}\t {transfer.address} {transfer.symbol} {transfer.signature}\t {transfer.changeType} {transfer.changeAmount}')
            #
