"""
This is a Object that represents a SPL-Transaction
"""
import datetime
        

class SplTransfer:
    def __init__(self, tid: str, address: str, signature: str, changeType:str, changeAmount:int, decimals:int, tokenAddress:str, tokenSymbol:str, blockTime:int):
        self.tid = tid
        self.address = address
        self.signature = signature
        self.changeType = changeType
        self.changeAmount = changeAmount
        self.decimalsAmount = decimals
        self.tokenAddress = tokenAddress
        self.tokenSymbol = tokenSymbol
        self.blockTime = blockTime
        self.isLogged = False

    def get_transferAmountFormated(self):
        if self.decimalsAmount != 0:
            tmp = self.decimalsAmount
            devisor = 1
            while(tmp):
                devisor *= 10
                tmp -= 1
            return float(self.changeAmount)/devisor
        else:
            return float(self.changeAmount)

    def printTransfer(self):
        print(f'{self.isLogged}\t{self.signature}\t {self.changeType}{self.get_transferAmountFormated()} {self.tokenSymbol}\t[{datetime.datetime.fromtimestamp(self.blockTime).isoformat()}]')
       
    def set_coingeckoPrice(self, cg_price: float):
        self.cg_price = cg_price
