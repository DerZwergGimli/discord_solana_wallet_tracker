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
            #json_response = response.json()
            tokens: Token = []
            for json_token in response.json():
                try:
                    if json_token['tokenSymbol']:
                        tokenSymbol = json_token['tokenSymbol']
                except:
                    pass
                tokens.append(
                    Token(
                        address=str(json_token['tokenAddress']),
                        amount=float(
                            json_token['tokenAmount']['uiAmountString']),
                        short_name=str(tokenSymbol)
                    ))
                print(type(tokens[0].address))
            return tokens

    def get_splTransfers(walletAddress: str):
        solscan_url = base_url + 'account/splTransfers'
        params = {
            'account': walletAddress,
            'offset': 0,
            'limit': 2,
        }
        response = callSolscanAPI(
            url=solscan_url, headers=solscan_headers, params=params)

        if response != -1:
            splTransfers: SplTransfer = []
            j_respsonse = response.json()
            t: dict = j_respsonse['data']
            for json_transfer in t:
                splTransfers.append(SplTransfer('dsds', "s", "sds"))
            return splTransfers
