import json
from loguru import logger
import requests
from requests.structures import CaseInsensitiveDict


baseurl = 'https://api.coingecko.com/api/v3'
headers = CaseInsensitiveDict()
headers['accept'] = 'application/json'


class CoingekoAPI:
    def getTokenPrice(chain_id: str, token_address: str, vs_currencies: str = 'usd'):
        try:
            url = f'{baseurl}/simple/token_price/{chain_id}?contract_addresses={token_address}&vs_currencies={vs_currencies}'
            resp = requests.get(url, headers=headers, timeout=1)
            if(resp.status_code == 200):
                jsonMessage = resp.json()
                return jsonMessage[token_address]['usd']
            else:
                logger.error(f'Cannot fetch balance{resp.status_code}')
        except:
            logger.error("Unable to reach Coingeko-API")
