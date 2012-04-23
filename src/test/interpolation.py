'''
Created on Feb 7, 2012

@author: 801155602
'''
import math
from scipy import integrate
x = [0.5 , 2.1 , 4.1 , 6.7 , 9.6 , 13.1 , 16.5 ,   19.1 , 25.2 , 36.5, 37.2 , 44.1 , 49.6 , 51.5 , 60.2 , 60.7  ]
y = [.53340, 0.57 , 0.64, 0.70 , 0.72 , 0.77, 0.81, 0.83 , 0.88 , 0.95, 0.96  , 1.004062 , 1.04 , 1.06 , 1.12 , 1.12 ]
z = [.53340, 0.57 , 0.64, 0.70 , 0.72 , 0.77, 0.81, 0.83 , 0.88 , 0.95, 0.96  , 1.004062 , 1.04 , 1.06]


def gaussianfunc(x, stddev, mean):
    power = -1 * (math.pow(x - mean, 2) / (2 * math.pow(stddev,2)))
    exponent = math.exp(power)
    return exponent / (stddev * math.sqrt(2 * math.pi))

def inversegaussian(area, stddev , mean):
    area = area * (stddev * math.sqrt(2* math.pi))
    lnarea = (math.log(area) * -1) * 2 * (math.pow(stddev, 2))
    lnarea = math.sqrt(lnarea)
    return lnarea + mean

def areaundercurve(func, a , b , funcarguments):
    return integrate.quad(func, a , b ,args = funcarguments )



    
    