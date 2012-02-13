'''
Created on Sep 23, 2011

@author: Ashwani Rao
'''
from numpy import *
from decimal import Decimal
from personalrecord import *
from scipy import stats
def getattributes(basestorage, age, sex, attrs):
    '''
    go over all the personal records and make an array of all value of the
    resuqested attributes at a particular age. for eg. if age is 2.6 and attributes is (sex, bmi)
    then result is as following at the age of 2.6
    [M,12
    M,13
    F, 14.6
    F, None]
    where each row represents a personal record
    '''
    
    result = array([], dtype = Decimal)
    if attrs is None or basestorage is None:
        return None
    for pr in basestorage:
        if (pr.getsex() == sex):
            tattrs = pr.gettimeattribute(age)
            temp = array([], dtype = Decimal, ndim = 1)
            if (tattrs in None):
                for attr in attrs:
                    temp = append(temp,[None])
            else:
                for attr in attrs:
                    temp = append(temp, tattrs.getattribute(attr))
            result = append(result, temp)
    result = reshape(result, ( result.size / len(attrs) ,len(attrs) ))
    return result



def getrecords(personalrecords, lowindex, highindex):
    result = list()
    for i in range(lowindex, highindex):
        result.append(personalrecords[i])
    return result

def getpersonalattribute(personalrec, attr):
    '''
    takes as input a personal record and single attribute name (this must be time based attribute)
    and returns an array for all the values of the given attribut
    '''
    result = array([])
    for timeattr in personalrec.getalltimeattribute():
        if (timeattr.getattribute(attr) is not None):
            result = append(result, float(timeattr.getage()))
            result = append(result, float(timeattr.getattribute(attr)))
    return reshape(result, (len(result)/2, 2))


def iterateoverrecords(listpr, sex, attr):
    result1 = array([],dtype=float)
    for pr in listpr:
        result = getpersonalattribute(pr, attr)
        if (result.size > 6):
            slp,inter,rval,pval,stderr =stats.linregress(result)
            if slp == slp or inter == inter:
                result1 = append(result1,slp)
                result1 = append(result1,inter)
                result1 = append(result1,rval)

    return reshape(result1, (len(result1)/3, 3))