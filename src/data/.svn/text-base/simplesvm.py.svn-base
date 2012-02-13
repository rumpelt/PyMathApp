'''
Created on Oct 6, 2011

@author: Ashwani Rao
'''
from sklearn import svm
from sklearn.linear_model import SGDClassifier
from sklearn import linear_model
from numpy import *
from decimal import Decimal

def getallfeatures(personalrecords, attlist , attdeaultvalue , atttocheck,lowage , upage, agetype):
    '''
    list of personal records for which we want to prepare n_sample with 
    n_features.
    Skips the records for which any of its attribute is missing
    attlist is list of generic attributes.
    '''
    processedlist = None
    for pr in personalrecords:
        if pr.containsattribute(atttocheck, lowage, upage, agetype):
            if processedlist is None:
                processedlist = [pr]
            else:
                processedlist.append(pr)
    result = array([],dtype=float)
    missing = 0
    for pr in processedlist:
        tempstorage = array([],dtype=float)
        full = True
        for att in attlist:
            if pr.containsattribute(att, lowage, upage, agetype):
                tempstorage = append(tempstorage, float (pr.getattribute(att, lowage , upage, agetype)))
            else:
                #tempstorage = append(tempstorage, attdeaultvalue.get(att))
                #tempstorage = append(tempstorage, float(0.0))
                full = False
                break
        if full:
            result = append(result, tempstorage)
        else:
            missing = missing + 1
    print 'missing'
    print missing
    if len(attlist) == 1:
        return result
    return reshape(result, (len(result) / len(attlist) , len(attlist) ))

def gettrainingrecords(personalrecords, lowrange, highrange):
    trainingrecords = list()
    for i in range(lowrange, highrange):
        trainingrecords.append(personalrecords[i])
    return trainingrecords

def getobsesitytarget(personalrecords ,attlist):
    result = array([],dtype=float)
    for pr in personalrecords:
        result = append(result, pr.getobese(Decimal(30.0), 'MONTHS'))
    return result
 
def gettestingrecords(personalrecords, lowrange, highrange):
    testingrecords = list()
    for i in range(lowrange, highrange):
        testingrecords.append(personalrecords[i])

def getdefualtvalues(attlist, personalrecords):
    result = dict()
    for att in attlist:
        temp =  array([],dtype=float)
        for p in personalrecords:
            if p.getgenericattribute(att) is not None:
                temp = append(temp, float(p.getgenericattribute(att)))
        result[att] = median(temp)
    return result
def testbayesianridge(personalrecords, sex, lowrange, highrange):
    clf = linear_model.BayesianRidge()
    training = gettrainingrecords(personalrecords, lowrange, highrange)
    testing = gettrainingrecords(personalrecords, highrange, len(personalrecords))
   # attlist = ['GESTATIONWEEKS','PREGNANCYWEIGHT','WEIGHTATDELIVERY','GESTATIONALDIABETES','PREGNANCYWEIGHTGAIN'
    #           ,'SMOKINGHIGH','SMOKINGLOW']
    attlist = ['PREGNANCYWEIGHT','WEIGHTATDELIVERY','GESTATIONALDIABETES','PREGNANCYWEIGHTGAIN'
               ,'SMOKINGHIGH','SMOKINGLOW']
   # attlist = ['PREGNANCYWEIGHTGAIN']
    
    attdefaultvalue = getdefualtvalues(attlist, personalrecords)
    attdefaultvalue['SMOKINGHIGH'] = float(0.0)
    attdefaultvalue['SMOKINGLOW'] = float(0.0)
    
    features = getallfeatures(training, attlist , attdefaultvalue)
    targets = getobsesitytarget(training,attlist)
    testinfeatures = getallfeatures(testing, attlist , attdefaultvalue)
    testingtarget = getobsesitytarget(testing,attlist)
    
    count = 0
    for val in targets:
        if val == 1:
            count = count + 1
    print count
    print 'fitting model'
    clf.fit(features, targets)
    print 'fitted model'
    count = 0
    for ft in testinfeatures:
        resul = clf.predict(ft)
      #  print resul
        count = count + 1
    return clf

def testSGD(personalrecords, sex, lowrange, highrange):
    clf = SGDClassifier(loss='hinge',penalty='l2')
    training = gettrainingrecords(personalrecords, lowrange, highrange)
    testing = gettrainingrecords(personalrecords, highrange, len(personalrecords))
   # attlist = ['GESTATIONWEEKS','PREGNANCYWEIGHT','WEIGHTATDELIVERY','GESTATIONALDIABETES','PREGNANCYWEIGHTGAIN'
    #           ,'SMOKINGHIGH','SMOKINGLOW']
    attlist = ['PREGNANCYWEIGHT','WEIGHTATDELIVERY','GESTATIONALDIABETES','PREGNANCYWEIGHTGAIN','SMOKINGHIGH','SMOKINGLOW']
    #attlist = ['PREGNANCYWEIGHTGAIN','GESTATIONALDIABETES']
    
    attdefaultvalue = getdefualtvalues(attlist, personalrecords)
    attdefaultvalue['SMOKINGHIGH'] = float(0.0)
    attdefaultvalue['SMOKINGLOW'] = float(0.0)
    
    features = getallfeatures(training, attlist , attdefaultvalue, 'OBESITY', 30.0, 60.0, 'MONTHS')
    targets = getallfeatures(training, ['OBESITY'] , attdefaultvalue, 'OBESITY', 30.0, 60.0, 'MONTHS')
    testinfeatures = getallfeatures(testing, attlist , attdefaultvalue , 'OBESITY', 30.0, 60.0, 'MONTHS')
    testingtarget = getallfeatures(testing, ['OBESITY'] , attdefaultvalue, 'OBESITY', 30.0, 60.0, 'MONTHS')
    
    count = 0
    for val in targets:
        if val == 1:
            count = count + 1
    print count
    count = 0
    for val in testingtarget:
        if val == 1:
            count = count + 1
    print count
    print 'fitting model'
    print features.shape 
    print features.ndim
    print targets.shape 
    print targets.ndim
    clf.fit(features, targets)
    print 'fitted model'
    count = 0
    for ft in testinfeatures:
        resul = clf.predict(ft)
        if resul == 1 and testingtarget[count] == resul:
            print resul
        count = count + 1
    return clf

def testsvm(personalrecords, sex, lowrange, highrange):
    clf = svm.SVC()
    training = gettrainingrecords(personalrecords, lowrange, highrange)
    testing = gettrainingrecords(personalrecords, highrange, len(personalrecords))
    
   # attlist = ['GESTATIONWEEKS','PREGNANCYWEIGHT','WEIGHTATDELIVERY','GESTATIONALDIABETES','PREGNANCYWEIGHTGAIN'
    #           ,'SMOKINGHIGH','SMOKINGLOW']
   # attlist = ['PREGNANCYWEIGHT','WEIGHTATDELIVERY','GESTATIONALDIABETES','PREGNANCYWEIGHTGAIN'
    #           ,'SMOKINGHIGH','SMOKINGLOW']
    attlist = ['PREGNANCYWEIGHTGAIN','GESTATIONALDIABETES']
    
    attdefaultvalue = getdefualtvalues(attlist, personalrecords)
    attdefaultvalue['SMOKINGHIGH'] = float(0.0)
    attdefaultvalue['SMOKINGLOW'] = float(0.0)
    
    features = getallfeatures(training, attlist , attdefaultvalue, 'OBESITY', 30.0, 60.0, 'MONTHS')
    targets = getallfeatures(training, ['OBESITY'] , attdefaultvalue, 'OBESITY', 30.0, 60.0, 'MONTHS')
    testinfeatures = getallfeatures(testing, attlist , attdefaultvalue , 'OBESITY', 30.0, 60.0, 'MONTHS')
    testingtarget = getallfeatures(testing, ['OBESITY'] , attdefaultvalue, 'OBESITY', 30.0, 60.0, 'MONTHS')
    
    count = 0
    for val in targets:
        if val == 1:
            count = count + 1
    print count
    count = 0
    for val in testingtarget:
        if val == 1:
            count = count + 1
    print count
    print 'fitting model'
    print features.shape 
    print features.ndim
    print targets.shape 
    print targets.ndim
    clf.fit(features, targets)
    print 'fitted model'
    count = 0
    for ft in testinfeatures:
        resul = clf.predict(ft)
        if resul[0] == 1. and resul[0] == testingtarget[count] :
            print resul
        count = count + 1
    return clf