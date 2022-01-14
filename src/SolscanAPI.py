from cmath import log
from email import header
from email.mime import base
from lib2to3.pgen2 import token
from ossaudiodev import AFMT_MPEG
from urllib import request, response
from loguru import logger
import requests
from requests.structures import CaseInsensitiveDict
from src.APICaller import callSolscanAPI
from src.Token import Token
from src.SplTransfer import SplTransfer
import json

url = "https://api.mainnet-beta.solana.com"
base_url = "https://public-api.solscan.io/"
solscan_headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
    'Accept': 'application/json'
}


class SolscanAPI:
    def get_account_tokens(walletAddress: str):
        solscan_url = base_url + 'account/tokens'
        params = {
            'account': walletAddress
        }
        response = callSolscanAPI(
            url=solscan_url, headers=solscan_headers, params=params)

        if response != -1:
            tokens: Token = []
            for json_token in response.json():
                try:
                    if json_token['tokenSymbol']:
                        tokenSymbol = json_token['tokenSymbol']
                except:
                    tokenSymbol = "?"
                    pass
                tokens.append(
                    Token(
                        address=str(json_token['tokenAddress']),
                        amount=float(
                        json_token['tokenAmount']['uiAmountString']),
                        short_name=str(tokenSymbol),
                        coingecko=False
                    ))
            return tokens

    def get_splTransfers(walletAddress: str, limit:int = 1):
        solscan_url = base_url + 'account/splTransfers'
        params = {
            'account': walletAddress,
            'offset': 0,
            'limit': limit,
        }
        response = callSolscanAPI(
            url=solscan_url, headers=solscan_headers, params=params)

        if response != -1:
            splTransfers: SplTransfer = []
            for data in response.json()['data']:
                try:
                    if data['symbol']:
                        tokenSymbol = data['symbol']
                except:
                    tokenSymbol = "?"
                    pass
                splTransfers.append(SplTransfer(
                    tid=data['_id'], 
                    address=data['address'], 
                    signature=data['signature'],
                    changeType=data['changeType'],
                    changeAmount=data['changeAmount'],
                    decimals=data['decimals'],
                    tokenAddress=data['tokenAddress'],
                    tokenSymbol=str(tokenSymbol),
                    blockTime=data["blockTime"]
                    ))
            return splTransfers
