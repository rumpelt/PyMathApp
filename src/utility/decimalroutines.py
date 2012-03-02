'''
Created on Dec 8, 2011

@author: 801155602
'''
from decimal import Decimal
import decimal
class decimalroutines():
    
    def __init__(self, rounding=decimal.ROUND_HALF_UP ):
        self.rounding = rounding
        
  
    def getstring(self, value, scale):
        '''
        given a float value or a Decimal value. Return a string reprsentation of the
        float value with rounding 
        '''
        return str(Decimal(value).quantize(scale, self.rounding))
    def setscale(self, value, scale):
        '''
        given a float value or a Decimal value. Return a Decimal reprsentation of the
        float value with rounding 
        '''
        return Decimal(value).quantize(scale, self.rounding)

        