'''
Created on Feb 7, 2012

@author: Ashwani
TODO: Implement the weighted version of spline interpolation, look at the paper
LMS method for growth standard for heurisitc on calculation weight for each point.
Use some kind of heurisctic
'''
from scipy.interpolate import UnivariateSpline 
import numpy as np
from numpy import linspace

from utility import decimalroutines
from decimal import Decimal
class interp1d(object):
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
            func = UnivariateSpline(x , y , k = k)
            
            xnew = linspace(x[0],x[len(x) -1],x[len(x) -1] - x[0] )
            if len(xnew) <= 1:
                continue
            ynew = func(xnew)   
            
            
            if resetattribute:
                for  timeattr in p.getalltimeattribute():
                    timeattr.setattribute(attribute, None)
            
            count = 0
            for xn in xnew :
               # print dc.setscale(xn, Decimal('.01')), '  ', dc.setscale(ynew[count], Decimal('.01'))
                p.addtimeattributewithnorder(dc.setscale(xn, Decimal('.01')),agetype, attribute , dc.setscale(ynew[count], Decimal('.01')) )
                count = count + 1
            
    
    
    def setCentiles(self, listpr, attribute, lowerage, ageoffset):
        measurements = self.getpopulation(listpr, lowerage, ageoffset, attribute)
        L,M,S = self.returnLMS(measurements)
        for pr in listpr:
            if pr.getattributeinperiod(attribute, lowerage, ageoffset) is not None:
                val = pr.getattributeinperiod(attribute, lowerage, ageoffset)
                 
    def returnLMS(self, msr):
        '''
        This function returns the LMS parameter for given sample of mesurements.
        The following step is first step of Appendix A of LMS method for growth standards.
        '''
        mlogs = np.log(msr) # measurement of logs
        meanOfmlogs = np.mean(mlogs)
        sdOflmlogs = np.std(mlogs)
        gMean = np.exp(meanOfmlogs)
        gSD = sdOflmlogs
        
        '''
        Following is the second step of appendix A paper "LMS methods for growth standard".
        '''
        aMean = np.mean(msr)
        aSD = np.divide(np.std(msr), gMean)    
        
        '''
        following is third step of appendix A
        '''
        recmsr = np.reciprocal(msr)
        recMean = np.mean(recmsr)
        hMean  = np.reciprocal(recMean) # harmonic mean
        hSD = np.multiply(np.std(recmsr), gMean) # harmonic CV or harmonic SD
        
        '''
        following is forth step of the appendix A.
        '''
        print aSD, ' ' ,hSD, ' ', gSD
        A = np.log(np.divide(aSD, hSD))
        B = np.log(np.multiply(aSD, hSD) / np.power(gSD, 2))
        L  = np.multiply(-1 , np.divide(A , np.multiply(B,2)))
        errorL = np.divide(1, np.sqrt(np.multiply(len(msr), B)))
        print A , ' ', B
        '''
        following is the fifth step of the appendix A        
        '''
        S = np.multiply(gSD, np.exp(np.divide(np.multiply(A,L), 4)))    
        
        '''
        the sixth step of the appendix A of paper LMS method for growth 
        standards
        '''
        M = gMean + np.divide(np.multiply((aMean - hMean), L), 2) + \
            (((aMean - (2 * gMean) + hMean) * np.power(L,2))/ 2)            
        errorM = (M * S) / (np.sqrt(len(msr)))
        return (L,M,S)
            
                  