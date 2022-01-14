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

    def printTransfer(self):
        if self.decimalsAmount == 6:
            print(f'{self.isLogged}\t{self.signature}\t {self.changeType}{float(self.changeAmount)/1e6} {self.tokenSymbol}\t[{datetime.datetime.fromtimestamp(self.blockTime).isoformat()}]')
        else:
            print(f'{self.isLogged}\t{self.signature}\t {self.changeType}{float(self.changeAmount)} {self.tokenSymbol}\t[{datetime.datetime.fromtimestamp(self.blockTime).isoformat()}]')

    def set_coingekoPrice(self, cg_price: float):
        self.cg_price = cg_price

#  def getAmount(self):
#    return self.amount
