'''
Created on Feb 7, 2012

@author: 801155602
'''
from scipy.interpolate import UnivariateSpline , LSQUnivariateSpline
from numpy import linspace
from utility import decimalroutines
from decimal import Decimal
class onedinterp(object):
    def __init__(self, records =None):
        '''
        One D interpolation
        '''
        self.__records = records
    
    def interpolatelocal(self, attribute, resetattribute=False , records = None):
        if records is not None:
            self.__records = records
        dc = decimalroutines.decimalroutines()
        for p in self.__records:
            x  = list()
            y = list ()
           
            agetype = None
            for  timeattr in p.getalltimeattribute():
                agetype = timeattr.getagetype()
                if timeattr.getattribute(attribute) is not None:
                    x.append(float(timeattr.getage()))
                    y.append(float(timeattr.getattribute(attribute)))
            
            k = 2
            if len(x) <= 1:
                continue
            if len(x) <= 2:
                k = 1
            
            #func = LSQUnivariateSpline(x , y ,t= t, k = k)
            func = UnivariateSpline(x , y , k = k, s=2)
            
            xnew = linspace(x[0],x[len(x) -1],x[len(x) -1] - x[0] )
            ynew = func(xnew)   
            
            
            if resetattribute:
                for p in self.__records:
                    for  timeattr in p.getalltimeattribute():
                        timeattr.setattribute(attribute, None)
            if len(xnew) == 1:
                ynew = [ynew]
            count = 0
            for xn in xnew :
             #  print dc.setscale(xn, Decimal('.01')), '  ', dc.setscale(ynew[count], Decimal('.01'))
                p.addtimeattributewithnorder(dc.setscale(xn, Decimal('.01')),agetype, attribute , dc.setscale(ynew[count], Decimal('.01')) )
                count = count + 1
            