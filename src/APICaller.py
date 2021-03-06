import requests
from loguru import logger
import loguru

def callSolscanAPI(url: str, headers, params):
    try:
        response = requests.get(url, headers=headers, params=params, timeout=1)
        if response.status_code == 200:
            return response
        else:
            logger.error('Solscan query error')
    except:
        logger.error(f'Unable to reach: {url}')
