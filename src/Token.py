"""
This is a Object that represents a Token
"""


class Token:
    def __init__(self, address: str, amount: float, short_name: str, coingecko:bool):
        self.address = address
        self.amount = amount
        self.short_name = short_name
        self.coingecko = False

    def enableCoingeko(self):
        self.coingecko = True

    def printToken(self):
        print(f'\t{self.address}\t {self.short_name}\t {self.amount}')

    def set_coingekoPrice(self, cg_price: float):
        self.cg_price = cg_price
#  def getAmount(self):
#    return self.amount
