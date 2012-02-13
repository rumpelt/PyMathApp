'''
Created on Dec 8, 2011

@author: 801155602
'''
from data import  personalrecord
from decimal import Decimal
import re
from writer import csvwriter
import nltk

def resetvariable(listpr, attributetoreset, generictype=False):
    for p in listpr:
        if generictype:
            p.setgenericattribute(attributetoreset, None)
        else:
            for timeattr in p.getalltimeattribute():
                timeattr.setattribute(attributetoreset, None)

def resetalltimeattribute(listpr):
    for p in listpr:
        p.__timeattributes = list()
def getrecordswithvaluegreaterthan(listpr, agelower , ageupper, threshold ,attribute ):
    '''
    return the personal records with value greater than or equal to threshold value for
    the given attribute
    '''
    result = list()
    for personalrecord in listpr:
        
        for timeattrs in personalrecord.getalltimeattribute():
            if timeattrs.getage().compare(Decimal(agelower)) >= 0 and \
            timeattrs.getage().compare(Decimal(ageupper)) <= 0:
                bmip = timeattrs.getattribute(attribute)
                if bmip is not None and bmip.compare(Decimal(threshold)) >= 0:
                    result.append(personalrecord)
                    break
    return result

def getrecordswithvaluelessthan(listpr, agelower , ageupper, threshold ,attribute ):
    '''
    return the personal records with value less than the threshold value for
    the given attribute
    '''
    result = list()
    for personalrecord in listpr:
        for timeattrs in personalrecord.getalltimeattribute():
            if timeattrs.getage().compare(Decimal(agelower)) >= 0 and \
            timeattrs.getage().compare(Decimal(ageupper)) <= 0:
                bmip = timeattrs.getattribute(attribute)
                if bmip is not None and bmip.compare(Decimal(threshold)) < 0:
                    result.append(personalrecord)
                    break
    return result


def returnfeedtype(tokens):
    if tokens is None:
        return None
    bottle = False
    breast = False

    for tok in tokens:
        if not bottle and re.match('^bottl|^bf|formula|^enfa|^lipil|^iron|^isomil|^enf|^lacto|^similac|^prosobe', tok):
            bottle = True
        elif not breast and re.match('^breast' , tok):
            breast = True
    if bottle and breast:
        return "Breast and Bottle"
    elif bottle:
        return "Bottle"
    elif breast:
        return "Breast"
    else:
        return None
def changed(values):
    temp = values[0]
    changed = None
    for val in values:
        if temp != val:
            return val
        temp = val
    return changed 

def highestfreq(values):
    freqcount = nltk.FreqDist()
    for val in values:
        freqcount.inc(val)
    freqc = freqcount.max()
    if freqcount.Nr(freqcount[freqc]) > 1:
        return 'equal'
    else:
        return freqc 

def clearfeedingvalue(listpr):
    for pr in listpr:
        pr.removegenricattribute('FEEDING')
def populatefeedingvalue(listpr,  lowage, upage):
    for pr in listpr:
        feedtype = list()
        agetype = list()    
        for timeattrs in pr.getalltimeattribute():
            age = timeattrs.getage()
            doc = timeattrs.getattribute('DOC')
            value = None
            if doc is not None and age.compare(Decimal(lowage)) >= 0 \
            and age.compare(Decimal(upage)) < 0:
                value = returnfeedtype(doc.text.get('Feeding:'))
                if value is None:
                    value = returnfeedtype(doc.text.get('Feeding:'))
                if value is None:
                    value = returnfeedtype(doc.text.get('Appetite:'))               
                if value is not None:                    
                    #timeattrs.addattribute(age, 'FEEDING', value)
                    print value
                    feedtype.append(value)
                    agetype.append(age) 
            
        if len(feedtype) > 0:
            if changed(feedtype) is  None:
                pr.addgenericattribute('FEEDING',feedtype[0])
        #        row.append('NOTPURE')
        #        row.append(changed(feedtype))
        #    else:
        #        row.append('PURE')
        #       row.append(feedtype[0])
def test(listpr, lowage, upage):
    for p in listpr:
        for timeattrs in p.getalltimeattribute():
            age = timeattrs.getage()
            doc = timeattrs.getattribute('DOC')
            if doc is not None and age.compare(Decimal(lowage)) >= 0 \
            and age.compare(Decimal(upage)) < 0:
                if len(doc.text.values()) > 0:
                    print 'doc', ' ', doc.text.keys()
def writefeedingvalue(filename, listpr,  lowage, upage):
    writer = csvwriter.csvwriter(filename)
    rows = list()
        
    for pr in listpr:
        agetype = list()
        feedlist = list()
        missingVisit = list()
        for i in range(int(upage - lowage)):
            feedlist.append('')
            missingVisit.append(True)
        for timeattrs in pr.getalltimeattribute():
            age = timeattrs.getage()
            doc = timeattrs.getattribute('DOC')
            value = None
            if doc is not None and age.compare(Decimal(lowage)) >= 0 \
            and age.compare(Decimal(upage)) < 0:
                value = returnfeedtype(doc.text.get('Feeding:'))
                if value is None:
                    value = returnfeedtype(doc.text.get('Appetite:'))
                if value is None:
                    value = returnfeedtype(doc.text.get('Eating:'))               
                if value is not None:
                    print value
                    if int(age) == len(feedlist):
                        feedlist[int(age) - 1] = value
                    else:
                        feedlist[int(age)] = value                    
                    agetype.append(age)                    
                    
                missingVisit.insert(int(age), False)
               
            #if age.compare(Decimal(lowage)) >= 0 and age.compare(Decimal(upage)) < 0 and value is not None:
             #   row = list()                
             #   row.append(str(pr.getgenericattribute('MRN')))                
             #   row.append(str(pr.getgenericattribute('UID')))
             #   row.append(str(age))
             #   row.append(value)
                #print row
             #   rows.append(row)
             #   break
        #if len(feedtype) > 0:
        #    row = list()
        #    row.append(str(pr.getgenericattribute('MRN')))                
        #    row.append(str(pr.getgenericattribute('UID')))
        #    row.append(str(agetype[0]))
        #    row.append(feedtype[0])
        #    if changed(feedtype) is not None:
        #        row.append('NOTPURE')
        #        row.append(changed(feedtype))
        #    else:
        #        row.append('PURE')
        #       row.append(feedtype[0])
        #    row.append(highestfreq(feedtype))
        #    rows.append(row)
        prevfeed = None
        i = 0    
       # print feedlist
        for feed in feedlist:
            if feed == '' and prevfeed == 'Bottle':
                feedlist[i] = 'Bottle'  
            else:
                prevfeed = feed
            i = i+1
        feedlist.reverse()
        i = 0
       # print 'after ', feedlist
        prevfeed = None
        for feed in feedlist:
            if feed == '' and prevfeed == 'Breast':
                feedlist[i] = 'Breast'
            else:
                prevfeed = feed
            i = i+1
       # print 'after 2', feedlist
        feedlist.reverse()
        row = list()
        row.append(str(pr.getgenericattribute('MRN')))                
        row.append(str(pr.getgenericattribute('UID')))
        count = 0
        for feed in feedlist:
            row.append(feed)
            if feed == '':
                row.append(str(missingVisit[count]))
            else:
                row.append('')
            count = count + 1
        if len(row) > 0:
            rows.append(row)
    writer.writerows(rows)                    
    writer.closewriter()                    