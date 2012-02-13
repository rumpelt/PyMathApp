'''
Created on Sep 24, 2011

@author: ashwani
'''
import personalrecord.PersonalRecord 
import personalrecord._TimeAttribute
from numpy import *
def getattributes(population, age, agetype, attributes):
    result = array[len(attributes)]
    i = 0
    for pr in population:
        tattrs = pr.gettimeattribute(age, agetype)
        if (not (tattrs is None)):
            for attr in attributes:
                result[i] = tattrs.getattribute(attr)
                i = i + 1    