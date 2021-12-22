"""
This is a Object that represents a Token
"""

class Token:
  def __init__(self, address:str, amount:float, short_name:str, gc_price:str, value_in_usd:float = 0):
    self.address = address
    self.amount = amount
    self.short_name = short_name
    self.value_in_usd = value_in_usd
    self.cg_price = gc_price #coingeko

#  def getAmount(self):
#    return self.amount
 