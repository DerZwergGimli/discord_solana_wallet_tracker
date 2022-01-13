"""
This is a Object that represents a SPL-Transfer
"""


class SplTransfer:
    def __init__(self, tid:str, 
                        address: str, 
                        signature: str):
        self.tid:str = tid,
        self.address:str = address,
        self.signature:str = signature,
        
    def printTransfer(self):
        #print(f'\t{self.tid}\t {self.address} {self.symbol} {self.signature}\t {self.changeType} {self.changeAmount}')
        print(str(self.tid))

    def set_coingekoPrice(self, cg_price: float):
        self.cg_price = cg_price
