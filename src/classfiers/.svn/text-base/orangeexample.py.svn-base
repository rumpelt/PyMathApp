'''
Created on Oct 18, 2011

@author: 801155602
'''
import orange, orngTest, orngStat, orngTree ,orngBayes

import data.personalrecord 
domain = None

def getallfeatures(personalrecords, attlist ,lowage , upage, agetype):
    '''
    list of personal records for which we want to prepare n_sample with 
    n_features.
    Skips the records for which any of its attribute is missing
    attlist is list of generic attributes.
    '''
    result = []
    for pr in personalrecords:
        tempstorage = []
        for att in attlist:
            if pr.containsattribute(att, lowage, upage, agetype):
                tempstorage.append(float (pr.getattribute(att, lowage , upage, agetype)))
            else:
                tempstorage.append(None)
        if pr.getobese(lowage,upage,'MONTHS') == 1:
                tempstorage.append('1')
        elif pr.getobese(lowage,upage,'MONTHS') == 0:
            tempstorage.append('0')
        else:
            tempstorage.append('None')
        result.append(tempstorage)
    return result

def createAttributes(attlist):
    attlist = ['PREGNANCYWEIGHT','WEIGHTATDELIVERY','GESTATIONALDIABETES','PREGNANCYWEIGHTGAIN'
               ,'SMOKINGLOW', 'SMOKINGHIGH']
    pregweight= orange.FloatVariable('PREGNANCYWEIGHT')
    w_delivery= orange.FloatVariable('WEIGHTATDELIVERY')
    gestdiab= orange.FloatVariable('GESTATIONALDIABETES')
    preg_wt_gain= orange.FloatVariable('PREGNANCYWEIGHTGAIN')
    lowsmoke= orange.FloatVariable('SMOKINGLOW')
    highsmoke= orange.FloatVariable('SMOKINGHIGH')
    obesity = orange.EnumVariable('OBESITY',values = ['1','0','None'])
    classAttributes = [pregweight,w_delivery, gestdiab, preg_wt_gain, lowsmoke
                       , highsmoke]
    domain = orange.Domain(classAttributes, obesity)

    return domain
def classifier(personalrecords, features , attlist ,lowage, upage ,estimation):
    data = orange.ExampleTable(createAttributes(attlist), getallfeatures(personalrecords,attlist,
                                                                         lowage, upage, 'MONTHS'))
    bayes = orange.BayesLearner()
    bayesWithEstimation = orange.BayesLearner(m=estimation)
    tree = orngTree.TreeLearner(mForPruning=2)
    bayes.name = "bayes"
    bayesWithEstimation.name = "bayesWithEstimation"
    tree.name = "tree"
    learners = [bayes, bayesWithEstimation]
    print '10 fold cross validattion'
    results = orngTest.crossValidation(learners, data, folds=10)
    # output the results
    print "Learner  CA     IS     Brier    AUC"
    for i in range(len(learners)):
        print "%-8s %5.3f  %5.3f  %5.3f  %5.3f" % (learners[i].name, \
                                                   orngStat.CA(results)[i], orngStat.IS(results)[i],
                                                   orngStat.BrierScore(results)[i], orngStat.AUC(results)[i])
        if learners[i].name == 'bayes' or learners[i].name == 'bayesWithEstimation':
            
    orngTree.printDot(tree, fileName='c:\\tree10.dot', internalNodeShape="ellipse", leafShape="box")
    
    orngTree.printDot(bayes, fileName='c:\\bayes10.dot', internalNodeShape="ellipse", leafShape="box")
