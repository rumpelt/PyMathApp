'''
Created on Feb 10, 2012

@author: 801155602
'''
import sys
class csvparser(object):
    
    def readfile(self,filename, numcols, header=False):
        fhandle = open(filename)
        result = list()
        for line in fhadle:
            