from loguru import logger
import requests
from requests.structures import CaseInsensitiveDict

url = "https://api.mainnet-beta.solana.com"
headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/json"


class API:
    def getBalane(walletAddress: str):
        data = """{"jsonrpc":"2.0", "id":1, "method":"getBalance", "params": ["%s"]}"""%(walletAddress)
        resp = requests.post(url, headers=headers, data=data)
        
        if(resp.status_code == 200):
            jsonMessage = resp.json()
            balance = jsonMessage['result']['value'] /10e8
            return balance
        else:
            logger.error(f"Cannot fetch balance{resp.status_code}")

    def getTokenAccountBalance(walletAddress:str, tokenAddress:str):
        data = """  {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "getTokenAccountsByOwner",
                "params": [
                            "%s",
                            {
                                "mint": "%s"
                            },
                            {
                                "encoding": "jsonParsed"
                            }
                            ]
                    }
                """%(walletAddress, tokenAddress)

        resp = requests.post(url, headers=headers, data=data)
        
        if(resp.status_code == 200):
            jsonMessage = resp.json()
            try:
                balance = jsonMessage['result']['value'][0]['account']['data']['parsed']['info']['tokenAmount']['uiAmount'] #/10e8
                return balance
            except:
                logger.warning(f"Unable to fetch balance of {tokenAddress}")
                return 0
        else:
            logger.error(f"Cannot fetch balance{resp.status_code}")