'''
Created on Dec 8, 2011

@author: 801155602
'''
from data import  personalrecord
from decimal import Decimal
from decimal import Context
import re
from writer import csvwriter
import nltk
import csv
import random
def getpopulation( listpr, agelower , offset, attribute ,genericattribute=False):
        '''
        get a list of the measurement for attribute.
        Primarly to be used in csv files
        '''
        result = list()
        for pr in listpr:
            if genericattribute:
                if pr.getgenericattribute(attribute) is not None:
                    result.append(str(pr.getgenericattribute(attribute)))
                continue             
            val = pr.getatributeinperiod(attribute, agelower, agelower+offset)
            if val is not None:
                result.append(float(val))
        return result


def getSetOfAttribute( listpr, agelower , offset, attlist):
        '''
         returns an M * N array of  values of attributes for each records
         M: number of records
         N: number of attributes to fetch
        '''
        result = []
        for pr in listpr:
            rlist = []
            rlist.append(str(pr.getgenericattribute('MRN')))
            for attribute in attlist:
                val = pr.getatributeinperiod(attribute, agelower, agelower+offset)                
                if val is not None:
                    rlist.append(float(val))
                else:
                    rlist.append('NA')
            result.append(rlist)    
        return result
        
def getpopulationasdict( listpr, agelower , offset, attribute ):
        '''
        get dictionary of measurement of attribute indexed by the UID
        '''
        result = dict()
        for pr in listpr:
            val = pr.getatributeinperiod(attribute, agelower, agelower+offset)
            if val is not None:
                result[str(pr.getgenericattribute('UID'))] = float(val)
        return result

def resetExceptHeightAndWeight(listpr,generictype=False):
    resetvariable(listpr,'HEADCRF',generictype)
    resetvariable(listpr,'VISITTYPE',generictype)
    resetvariable(listpr,'HEIGHTPERCENTILE',generictype)
    resetvariable(listpr,'HEIGHTZSCORE',generictype)
    resetvariable(listpr,'WEIGHTZSCORE',generictype)
    resetvariable(listpr,'WEIGHTPERCENTILE',generictype)
    resetvariable(listpr,'WEIGHTLENGTHZSCORE',generictype)
    resetvariable(listpr,'WEIGHTLENGTHPERCENTILE',generictype)
    resetvariable(listpr,'WEIGHTSTATUREPERCENTILE',generictype)
    resetvariable(listpr,'WEIGHTSTATUREZSCORE',generictype)
    resetvariable(listpr,'BMI',generictype)
    resetvariable(listpr,'BMIZSCORE',generictype)
    resetvariable(listpr,'BMIPERCENTILE',generictype)
    resetvariable(listpr,'OBESITY',generictype)
    resetvariable(listpr,'OBESITYRANK',generictype)
    resetvariable(listpr,'PONDREALINDEX',generictype)
    resetvariable(listpr,'SYSTOLICBP',generictype)
    resetvariable(listpr,'DIASTOLICBP',generictype)
    
       
def resetvariable(listpr, attributetoreset, generictype=False):
    '''
    Reset a generic type attribute. For a generic type attribute the 
    argumnet generictype should be set to True
    If it is time based attribute then this reset in all the time attributes
    '''
    for p in listpr:
        if generictype:
            p.setgenericattribute(attributetoreset, None)
        else:
            for timeattr in p.getalltimeattribute():
                timeattr.setattribute(attributetoreset, None)



def resetalltimeattribute(listpr):
    '''
    flushes the timebasedattribite structure for all records in list pr
    '''
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
        feedlist = list()
        visit = list()
        for i in range(int(upage - lowage)):
            feedlist.append('')
            visit.append(False)
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
                    if int(age) == len(feedlist):
                        feedlist[int(age) - 1] = value
                    else:
                        feedlist[int(age)] = value                 
                if int(age) == len(feedlist):    
                    visit[int(age) - 1] = True
                else:
                    visit[int(age)] = True
               
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
            row.append(str(visit[count]))
            count = count + 1
        if len(row) > 0:
            rows.append(row)
    writer.writerows(rows)                    
    writer.closewriter()       
    

def calculatebmi(listpr):
    c = Context()
    for p in listpr:
        for timeattr in p.getalltimeattribute():
            if timeattr.getattribute('HEIGHT') is not None  and timeattr.getattribute('WEIGHT') is not None:
                bmi = c.divide(timeattr.getattribute('HEIGHT') , c.power(timeattr.getattribute('WEIGHT'), Decimal("2")))
                timeattr.setattribute('BMI',bmi)  
                                                                                                                                                                                         
def removetimeattributes(listpr):
    for p in listpr:
        newtimeattr = list()
        for timeattr in p.getalltimeattribute():
            if timeattr.getnumnumericattributes() > 0 or \
            timeattr.getnumstringattributes() > 0:
                newtimeattr.append(timeattr)
        p.cleartimeattributes()
        p.getalltimeattribute().extend(newtimeattr)
        
def csvreader(filename ,lowage, upage, 
              seednum, numelements, skipheader):
    reader = csv.reader(open(filename,'r'),delimiter=',')
    ids=[]
    random.seed(seednum)
    if skipheader:
        reader.next()
    for row in reader:
        if float(row[1]) >= lowage and float(row[1]) <= upage: 
            ids.append(row[0])
    print random.sample(ids, numelements)

def csvappender(files, filetodump, skiheader):
    '''
    appends two csv files
    '''
    writer = csvwriter.csvwriter(filetodump)
    rows = list()
    for fi in files:
        reader = csv.reader(open(fi,'r'),delimiter=',')
        if skiheader:
            reader.next()
        for row in reader:
            rows.append(row)
    writer.writerows(rows)
    writer.closewriter()
            
def yetanotherscript(fileToRead, filetodump):
    '''
    operates on csv file to recorde the variable to string representation
    '''
    reader = csv.reader(open(fileToRead,'r'),delimiter=',')
    writer = csvwriter.csvwriter(filetodump)
    rows = list();
    for row in reader:
        thisrow = list()
        thisrow.append(row[0])
        if row[1] == '0.0':
            thisrow.append('0') 
        elif row[1] == '1.0':
            thisrow.append('1')
        else:
            thisrow.append('NA')
        if row[2] == '4.0' or row[2] == '3.0':
            thisrow.append('1')
        elif row[2] == '1.0' or row[2] == '2.0':
            thisrow.append('0')
        else:
            thisrow.append('NA')
        rows.append(thisrow)
    writer.writerows(rows)
    writer.closewriter()
      
def yetanotherscript2(fileToRead, filetodump, skipheader):
    '''
    Merges two columns of a csv file to produce a new column
    '''
    reader = csv.reader(open(fileToRead,'r'),delimiter=',')
    writer = csvwriter.csvwriter(filetodump)
    rows = list();
    if skipheader:
        rows.append(reader.next())
    for row in reader:
        thisrow = list(row)
        if row[4] != '':
            thisrow.append(row[4])
        elif row[5] != '':
            thisrow.append(row[5])
        rows.append(thisrow)
    writer.writerows(rows)
    writer.closewriter()

def yetanotherscript3(obesityfile, catfile, filetodump):
    '''
    Merges two columns of a csv file to produce a new column
    '''
    oreader = csv.reader(open(obesityfile,'r'),delimiter=',')
    creader = csv.reader(open(catfile,'r'),delimiter=',')
    writer = csvwriter.csvwriter(filetodump)
    rows = list()
    odict = dict()
    owdict = dict()
    for row  in oreader:
        odict[row[0]] = row[1]
        owdict[row[0]] = row[2]
    
    for row in creader:
        thisrow = list()
        thisrow.append(row[0])
        thisrow.append(row[1])
        thisrow.append(row[2])
        thisrow.append(odict.get(row[0]))
        thisrow.append(owdict.get(row[0]))
        rows.append(thisrow)
    
    writer.writerows(rows)
    writer.closewriter()