'''
Created on Oct 19, 2011

@author: 801155602
'''
import operator
import orange, orngTest, orngStat, orngTree  ,orngBayes
import orngLR
import random
import scipy
domain = None

def randomsamplewithreplacement(lstrecords, number):
    return random.sample(lstrecords, number)

def getAllObeseOrNonObese(lstrecords, flag , lowage, upage, agetype):
    '''
    flag : If true then we want to get all obese else
    non obese
    '''
    result = []
    for pr in lstrecords:
        if pr.getobese(lowage, upage, agetype) == 1 and flag:
            result.append(pr)
        elif pr.getobese(lowage, upage, agetype) == 0 and not flag:
            result.append(pr)
    return result

def getallfeatures(personalrecords, domain ,lowage , upage, agetype):
    '''
    list of personal records for which we want to prepare n_sample with 
    n_features.
    Skips the records for which any of its attribute is missing
    attlist is list of generic attributes.
    '''
    result = []
    numobese = 0;
    totalrecords = 0
    for pr in personalrecords:
        tempstorage = []
        for atts in domain.attributes:
            att = atts.name
            if pr.containsattribute(att, lowage, upage, agetype):
                if isinstance(pr.getattribute(att, lowage , upage, agetype),str) or isinstance(pr.getattribute(att, lowage , upage, agetype),unicode):
                    tempstorage.append(str (pr.getattribute(att, lowage , upage, agetype)))
                else:
                    tempstorage.append(float (pr.getattribute(att, lowage , upage, agetype)))
            else:
                tempstorage.append(None)
        if pr.getobese(lowage,upage,'MONTHS') == 1:
            tempstorage.append('1')
            result.append(tempstorage)
            numobese = numobese + 1
            totalrecords = totalrecords + 1
        elif pr.getobese(lowage,upage,'MONTHS') == 0:
            tempstorage.append('0')
            result.append(tempstorage)
            totalrecords = totalrecords + 1
        
    print 'Number of obese: ', numobese, ' non obese: ', totalrecords - numobese
    #print result
    return result

def countNumberOfObese(personalrecord, lowage, upage, agetype):
    numNone = 0
    obese = 0
    nonObese = 0
    for pr in personalrecord:
        if pr.getobese(lowage,upage,agetype) == 1:
            obese = obese + 1
        elif pr.getobese(lowage,upage,agetype) == 0:
            nonObese = nonObese + 1
        else:
            numNone = numNone + 1
    print 'Obese and Non obese count from' , lowage ,' till ', upage , ' months of age'
    print ' Number of obese :' , obese , ' Number of non obese :',   nonObese , ' Number of babies with no information :', numNone 
    
def createAttributes():
    #attlist = ['PREGNANCYWEIGHT','WEIGHTATDELIVERY','GESTATIONALDIABETES','PREGNANCYWEIGHTGAIN'
    #           ,'SMOKINGLOW', 'SMOKINGHIGH']
    
    
    
    #for keys,value in attlist.item():
     #   if valu
      #  classAttributes.append(keys)
    motherbmi = orange.FloatVariable('MOTHERBMI')
    gestWtGain = orange.FloatVariable('NETGESTATIONWEIGHTGAIN')
    prepregweight= orange.FloatVariable('PREPREGNANCYWEIGHT')
    ethinicity = orange.EnumVariable('ETHINICITY',values = ['WH','BL','HI','AS', 'UN', 'AI'])
    feed = orange.EnumVariable('FEEDINGMETHOD',values = ['Bottle','Breast','Breast and Bottle'])
    motherheight = orange.FloatVariable('MOTHERHEIGHT')
    diabetes =  orange.FloatVariable('DIABETES')
    gestdiabetes =  orange.FloatVariable('GESTATIONDIABETES')
    nicu =  orange.FloatVariable('NICU')
    nullip =  orange.FloatVariable('NULLIP')
    gestationweek =  orange.FloatVariable('GESTATIONWEEKS')
    
    w_delivery= orange.FloatVariable('WEIGHTATDELIVERY')
    gestdiab= orange.FloatVariable('GESTATIONALDIABETES')
    preg_wt_gain= orange.FloatVariable('PREGNANCYWEIGHTGAIN')
    lowsmoke= orange.FloatVariable('SMOKINGLOW')
    highsmoke= orange.FloatVariable('SMOKINGHIGH')
    
    obesity = orange.EnumVariable('OBESITY',values = ['1','0'])
    classAttributes = [motherbmi,gestWtGain, prepregweight, ethinicity, feed
                       , motherheight, diabetes, gestdiabetes, nicu, nullip, gestationweek]
    domain = orange.Domain(classAttributes, obesity)

    return domain

def getsample(lstrecords, lowage, upage, agetype):
    
    obese = getAllObeseOrNonObese(lstrecords,True, lowage, upage, agetype)
    nonobese = randomsamplewithreplacement(getAllObeseOrNonObese(lstrecords,False, lowage, upage, agetype), len(obese))
   
        #print len(result), ' ' , len(result[i])
    return obese + nonobese
def classiferProbabilites(experimentResults, numClasifierType , numCrossfold, data , attlist , responseVariable):
    result = dict()
    for i in range(numCrossfold):
        for j in range(numClasifierType):
            classifier = experimentResults.classifiers[i][j]
            for dt in data:
                for k in range(len(attlist)):
                    if not (dt[k] == None):
                    
                        prob = classifier.conditionalDistributions[k].p_class(dt[k], responseVariable)
                        t = (attlist[i], prob)
                        if result.get(attlist[i]) is None:
                            result[attlist[i]] = [t]
                        else:
                            result[attlist[i]] = result.get(attlist[i]).append(t)
                    else:
                        prob = 0
    return result

                    
def classifier(personalrecords, lowage, upage , agetype, numcrossfolds, estimation):
    domain = createAttributes()
    data = orange.ExampleTable(domain, getallfeatures(personalrecords,domain,
                                                                         lowage, upage, 'MONTHS'))
    
    bayes = orange.BayesLearner()
    bayesMEst = orange.BayesLearner()
    bayesMEst.estimatorConstructor = orange.ProbabilityEstimatorConstructor_m(m=estimation)

    tree = orngTree.TreeLearner(mForPruning=2)
    bayes.name = "bayes"
    bayesMEst.name = 'bayesWithMEstimation'
    tree.name = "tree"
    learners = [ bayesMEst]
    #learners = [tree]
    #print numcrossfolds , ' fold cross validattion', 'for' , learners
    results = orngTest.crossValidation(learners, data, folds=numcrossfolds, storeClassifiers = 1)
    # output the results
    #print "Learner  CA     IS     Brier    AUC" 
    #for i in range(len(learners)):
     #   print "%-8s %5.3f  %5.3f  %5.3f  %5.3f" % (learners[i].name, \
      #                                             orngStat.CA(results)[i], orngStat.IS(results)[i],
      #                                             orngStat.BrierScore(results)[i], orngStat.AUC(results)[i])
    
    #orngTree.printDot(tree, fileName='c:\\tree10.dot', internalNodeShape="ellipse", leafShape="box")
    #orngTree.printDot(bayes, fileName='c:\\bayes10.dot', internalNodeShape="ellipse", leafShape="box")
    TP = []
    FP = []
    TN = []
    FN = []
    for i in range(numcrossfolds):
        for j in range(len(learners)):
            classifier = (results.classifiers[i])[j]
            tp = 0
            fn = 0
            tn = 0
            fp = 0
            for dt  in data:
                if dt.getclass() == '1':
                    p = str(classifier(dt))
                    if p == '1':
                        tp = tp + 1
                    else:
                        fn  = fn +1
                if dt.getclass() == '0':
                    p = classifier(dt)
                    if p == '0':
                        tn = tn + 1
                    else:
                        fp  = fp +1
            #print 'Results for Learner :', learnersname[j], " for corssfold number ", i
            #print 'True positive: ', tp ,'False positive: ', fp, 'True Negative: ', tn, 'False Negative: ', fn
            TP.append(tp)
            FP.append(fp)
            TN.append(tn)
            FN.append(fn)
                #learners[j].dumpTree()
                #orngTree.printDot(learners[j], fileName=filename, internalNodeShape="ellipse", leafShape="box")
    #classiferProbabilites(results, len(learners) , numcrossfolds, data , attlist[:1] , '1')     
    return (results , TP ,FP , TN, FN)

def runexperiments(lstrecords, lowage,upage, agetype, numtimes ,numcrossfolds, mestimation):
    #print len(samplerecords)
    TPR = []
    FPR = []
    for i in range(numtimes):
        samplerecords = getsample(lstrecords, lowage, upage, agetype , 1)
        
        for records in samplerecords:
            #print len(records )
            results , TP ,FP , TN, FN = classifier(records, lowage, upage ,agetype, numcrossfolds, mestimation)
            #print scipy.mean(TP) ,' ', scipy.mean(FP) , ' ', scipy.mean(TN) , scipy.mean(FN)
            tpr = scipy.mean(TP) / (scipy.mean(TP) + scipy.mean(FN))
            fpr = scipy.mean(FP) / (scipy.mean(FP) + scipy.mean(TN))
            TPR.append(tpr)
            FPR.append(fpr) 
    return (TPR,FPR)

def getconditionalprob(lstrecords, lowage, upage, agetype, numcrossfolds , mestimation):
    samplerecords = getsample(lstrecords, lowage, upage, agetype , 1)
    domain = createAttributes()
    
    result = None
    for records in samplerecords:
        print len(records)
        data = orange.ExampleTable(domain, getallfeatures(records,domain,
                                                                         lowage, upage, 'MONTHS'))
    
        results , TP ,FP , TN, FN = classifier(records, lowage, upage ,agetype, numcrossfolds, mestimation)
        prob = classiferProbabilites(results,1,numcrossfolds, data, ['MOTHERBMI'],'1')
        result = sorted(prob, key=operator.itemgetter(0))
    return result

def countvariousattributes(examples):
    results = dict()
    domain = examples.domain
    for ex in examples:
        for i in range(len(ex)):
            if not ex[i].isSpecial():
                if results.get(domain.variables[i].name) is not None:
                    results[domain.variables[i].name] = results.get(domain.variables[i].name) + 1
                else:
                    results[domain.variables[i].name] = 1
    print results
            
def logisticregression(samplerecords, lowage, upage,agetype ):
    lstrecords = getsample(samplerecords, lowage, upage, agetype )
    prewt = orange.FloatVariable('PREPREGNANCYWEIGHT')
    motherbmi = orange.FloatVariable('MOTHERPREPREGNANCYBMI')
    #gestWtGain = orange.FloatVariable('NETGESTATIONWEIGHTGAIN')
    gestWtGainRate = orange.FloatVariable('GESTATIONWEIGHTGAINRATE')
    wtdelivery = orange.FloatVariable('WEIGHTATDELIVERY')
    bweight = orange.FloatVariable('BIRTHWEIGHT')
    ethinicity = orange.EnumVariable('MOTHERETHINICITY',values = ['BL','WH', 'AS', 'HI', 'AI','UN'])
    obesity = orange.EnumVariable('OBESITY',values = ['1','0'])
    classAttributes = [prewt,motherbmi, gestWtGainRate,wtdelivery, bweight,ethinicity]
    domain = orange.Domain(classAttributes, obesity)
    ft = getallfeatures(lstrecords,domain,lowage, upage,agetype)
    data = orange.ExampleTable(domain, ft)
    countvariousattributes(data)
    lr = orngLR.LogRegLearner(data, removeSingular=1)
    TP = TN = FP = FN = 0
    for ex in data:
        
        if ex.getclass() == '1':
            if lr(ex) == '1':
                TP = TP +1
            else:
                FN = FN + 1
        elif ex.getclass() == '0':
            if lr(ex) == '0':
                TN = TN +1
            else:
                FP = FP + 1
    countNumberOfObese(lstrecords, lowage,upage, agetype)
    orngLR.printOUT(lr)
    print TP, ' ', FP , ' ', TN , ' ', FN

def callsamples(numtimes, samplerecords, lowage, upage,agetype):
    for i in range(numtimes):
        lstrecords = getsample(samplerecords, lowage, upage, agetype )
        logisticregression(lstrecords, lowage, upage, agetype )
        
def std(lstrecords, attr):
    deviations = []
    ages =[]
    val = []

    for record  in lstrecords:
        if record.getAttributeAtEachAgePoint(attr) is not None:
            sorted_x = sorted(record.getAttributeAtEachAgePoint(attr).iteritems(), key=operator.itemgetter(0))
            for key , values in sorted_x:
                if values is not None:
                    val.append(float(values))
                    ages.append(float(key)) 
     
    return (ages , val)

