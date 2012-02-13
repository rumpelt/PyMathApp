'''
Created on Nov 1, 2011
A module representing a particular document and 
a base storage class containing all the documents.
@author: ashwani
'''
import re
import nltk
import math
from utility.decimalroutines import decimalroutines 

from decimal import Decimal
from writer import csvwriter
dc = decimalroutines()
fieldstoget = ['HISTORY:','Feeding:','Eating:', 'Sleeping:',  'Are you giving multivitamins?','Nightime feedings?',
               'Started solid foods yet?','Any juice, water, or cereal in the bottle?',
               'Sleeping position', 'Voiding:','Gestation Age:','Cesarean:','BIRTH Weight:','Comment:' , 'GENERAL:','CLAVICLES:','CHEST:' 
               ,'OBJECTIVE:','MUSCULOSKELETAL:','VASCULAR:' ,'HIPS:','Head:', 'Voiding pattern:','Stooling pattern:',
                         'Immunization status reviewed:','Immunization status:','Immunization reviewed:',
                          'Adverse reaction to previous vaccinations?', 'PHYSICAL EXAMINATION:',
                           'ABDOMEN:','GENERAL:', 'HEAD:','ROS:', 'Dental:','EYES:','ENT:','NECK:',
                           'RESP:','HEART:','ABD:','GU:','EXTREMITIES:','SKIN:','NEURO:', 
                           'GROWTH/DEVELOPMENT:','GROWTH:','DEVELOPMENT:','ASSESSMENT:', 'PLAN:', 
                           'No hospital prescriptions on file','No outpatient prescriptions on file','Counseling:' ,'Appetite:' ,
                           'Activity:','outpatient prescriptions as of', 'EXAM:', 'Growth parameters:',
                         'Current outpatient prescriptions','Other concerns:','Allergies:' ,'FUNDOSCOPY:',
                          'Current parental concerns:']


def createtopre(fields):
    result =''
    for field in fields:
        toks = field.split()
        #result =result + '^[[]*\s*'+toks[0]+'\s*[]]*$' +'|'
    
        if '?' in toks[0]:
            tomatch = toks[0].replace('?','[?]')
        else:
            tomatch = toks[0]
        result =result + '^[[]*.*'+tomatch+'\s*[]]*$' +'|'
    length = len(result)
    result  = result[:length -1]
    return str(result)

def separatefields(fields):
    result = list()
    for field in fields:
        toks = field.split()
        
        result.append(toks)
    return result

mainfieldmatch = createtopre(fieldstoget)
separatedfields = separatefields(fieldstoget)

def getfield(matchedfields):
    '''
    Regular expression might want to include the ignore case also
    Using separatedfields in here which is predefined in this script to
    fasten the process of tokenization
    '''
   
    for field in separatedfields:
       
        regexp = ''
        for tok in field:
            if '?' in tok:
                tomatch = tok.replace('?','[?]')
            else:
                tomatch = tok
            regexp = regexp+'^[[]*.*'+tomatch+'\s*[]]*$' +'|'
        regexp = regexp[:len(regexp) -1]
        found = True 
        for mf in matchedfields:
            if not re.match(regexp, mf):
                found = False
                break
        if found:
            return ' '.join(field)
    return None


def nextexpected( matchedtoks ):
    '''
    Using separatedfields in here which is predefined in this script to
    fasten the process of tokenization
    '''
    nextfield = []
    matchedTokLength = len(matchedtoks)
    for field in separatedfields:
        
        count = 0
        found =True
        for tok in field:
            if '?' in tok:
                tomatch = tok.replace('?','[?]')
            else:
                tomatch = tok
            if count >= matchedTokLength:
                break
            elif re.match('^[[]*\s*'+tomatch+'\s*[]]*$', matchedtoks[count]) is None:
                found = False
                break;
            count = count + 1
        if found and len(field) > count:
            nextfield.append(field[count])
    if len(nextfield) == 0:
        return None
    return nextfield

               
class documentid():
    '''
    A class representing how to identify the document.
    it represent a tuple of the unique id of the person
    and the age it was created
    id : the first element represent the unigue id of the
    person and the second is the age at which this was created
    '''
    
    def __init__(self, identifier):
        self.name ,self.age =  identifier
    
class ngramcontainer():
    def __init__(self , ngram , field ,agelower = None, ageupper= None):
        self.ngram = ngram
        self.freqdist = nltk.FreqDist()
        self.field = field
        self.agelower =agelower
        self.ageupper = ageupper
        self.probabilites = list()
    def populatefreqdist(self, tokens):
        grams = nltk.util.ingrams(tokens, self.ngram)
        for g in grams:
            if self.ngram == 1:                
                self.freqdist.inc(g[0])
            else:
                self.freqdist.inc(g)
    def calculateprobability(self, sample):
        if self.freqdist.freq(sample) is not None:
            return (float) (self.freqdist.freq(sample))/ self.freqdist.N()
        return None
class documents():
    '''
    A class representing the collection of all the documents we have so far.
    '''
    def __init__(self, basestorage=None , lowage=None, upage=None):
        # collection of type document
        self.collections = list()
        self.basestorage = basestorage
        # A dictionary of unigrams for fields like appetite , feeding , general etc , try to build
        # it for a range of age        
        self.unigrams = dict()
        # A dictionary of bigrams for fields like appetite , feeding , general etc
        self.bigrams = dict()
        # A dictionary of trigrams for fields like appetite , feeding , general etc
        self.trigrams = dict()
        self.count  = 0
        self.lowage = lowage
        self.upage = upage
    
    def populatengrams(self, listofkeys, agelower, ageupper):
        '''
        build the freq distribution of unigram , bigram or trigram.
        listofkeys: fields for which we want to build the ngram
        agelower: build only for personal records with age greater than agelower
        ageupper: build only for personal records with age lower than ageupper
        '''
        for field in listofkeys:
            self.unigrams[field] = ngramcontainer(1,field, agelower, ageupper)
            self.bigrams[field] = ngramcontainer(2,field, agelower, ageupper)
            self.trigrams[field] = ngramcontainer(3,field, agelower, ageupper)
            
        for doc in self.collections:
            if doc.documentid.age.compare(Decimal(agelower)) >= 0  and \
                doc.documentid.age.compare(Decimal(ageupper)) <= 0:
                for key in listofkeys:
                    if doc.text.get(key) is not None:
                        self.unigrams.get(key).populatefreqdist(doc.text.get(key))
                        self.bigrams.get(key).populatefreqdist(doc.text.get(key))
                        self.trigrams.get(key).populatefreqdist(doc.text.get(key))
    
    
    def printprobabilty(self, filename, key , ngram):
        writer = csvwriter.csvwriter(filename)
        freqdist = None
        if ngram == 1:
            freqdist = self.unigrams.get(key).freqdist
        elif ngram == 2:
            freqdist = self.bigrams.get(key).freqdist
        elif ngram == 3:
            freqdist = self.trigrams.get(key).freqdist
            
        samplesize = float (freqdist.N())
        print samplesize
        for item in freqdist:
            prob = freqdist.get(item) / samplesize
            op = list()
            op.append(' '.join(item))
            op.append(dc.getstring(prob, '.000000001'))
            writer.writerow(op)
        writer.closewriter()
    
    def utility(self , freqdist ,filename = None):
        '''
        function to print the freqdist
        '''
        if filename is not None:
            fhandle = open(filename,'w')
        for item in freqdist.iteritems():
            if filename is not None:
                fhandle.write(str(item))
                fhandle.write('\n')
            else:
                print item
        fhandle.close()
    def calculateEntropy(self , personalrecord, ngram , key , globalfreqdist ,agelower, ageupper):
        '''
        calculate enropy the values of field in the personal record. field here represents
        field of interest such as Feeding: , Eating, appetite etc.
        ngram : 1 for unigram , 2 for bigram , 3 for trigram
        field : field of interest as explained above
        globalfreqdist: The overall  freq distribution of the field in the corpus
        ''' 
        totalcounts = globalfreqdist.N()
        for timeattrs in personalrecord.getalltimeattribute():
            if timeattrs.getage().compare(Decimal(agelower)) >= 0 and \
                timeattrs.getage().compare(Decimal(ageupper)) <= 0 and \
                timeattrs.getattribute('DOC') is not None:
                doc = timeattrs.getattribute('DOC')
                if doc.text.get(key) is not None:
                    textvalue = doc.text.get(key) 
                    grams = nltk.util.ingrams(textvalue, ngram)
                    entropy = 0.0
                    cnt = 0
                    for gram in grams:
                        cnt = cnt + 1
                        if ngram == 1:
                            gram = gram[0]
                        count = globalfreqdist[gram]
                        probability =  float(count) / totalcounts
                        #  print count , ' ',  totalcounts , ' ' , probability 
                        entropy = entropy - (probability * math.log(probability , 2))
                    if cnt != 0:
                        timeattrs.setattribute(key+':ENTROPY:'+str(ngram), entropy / cnt)
                    #print entropy , ' ' , ngram
        return personalrecord
    
    def jointprobability(self , personalrecord, ngram , key , globalfreqdist ,agelower, ageupper):
        '''
        calculate enropy the values of field in the personal record. field here represents
        field of interest such as Feeding: , Eating, appetite etc.
        ngram : 1 for unigram , 2 for bigram , 3 for trigram
        field : field of interest as explained above
        globalfreqdist: The overall  freq distribution of the field in the corpus
        ''' 
        totalcounts = globalfreqdist.N()
        for timeattrs in personalrecord.getalltimeattribute():
            if timeattrs.getage().compare(Decimal(agelower)) >= 0 and \
                timeattrs.getage().compare(Decimal(ageupper)) <= 0 and \
                timeattrs.getattribute('DOC') is not None:
                doc = timeattrs.getattribute('DOC')
                if doc.text.get(key) is not None:
                    textvalue = doc.text.get(key) 
                    grams = nltk.util.ingrams(textvalue, ngram)
                    jporb = 1.0
                    cnt = 0.0
                    for gram in grams:
                        cnt = cnt + 1
                    grams = nltk.util.ingrams(textvalue, ngram)
                    for gram in grams:
                        if ngram == 1:
                            gram = gram[0]
                        count = globalfreqdist[gram]
                        probability =  float(count) / totalcounts
                    #    print count , ' ',  math.log(probability) 
                        jporb = jporb *  (probability)
                    if cnt != 0 and Decimal(jporb).compare(Decimal('0.000000000000000')) > 0:
                        timeattrs.setattribute(key+':JOINTPROB:'+str(ngram),  math.log(jporb) )
                        #print math.log(jporb) 
        return personalrecord
    
    def printentropy(self, filename , listpr , key , ngram ,agelower ,ageupper):
        fhandle = open(filename , 'w')
        writer = csvwriter.csvwriter(filename)
        for pr in listpr:
            data = False
            if pr.getobese(24, 55 ,'MONTHS') == 1:
                for timeattrs in pr.getalltimeattribute():
                    if timeattrs.getattribute(key+':JOINTPROB:'+str(ngram)) is not None \
                    and timeattrs.getage().compare(Decimal(agelower)) >= 0 and \
                timeattrs.getage().compare(Decimal(ageupper)) <= 0 :
                        fhandle.write(str(timeattrs.getage()) + ': ')
                        fhandle.write(dc.getstring(self, timeattrs.getattribute(key+':JOINTPROB:'+str(ngram)), \
                                                   '.0000001') + ' ')
                        data = True
            if data:
                fhandle.write('\n')            
        fhandle.close()    
        
    def caluculateEntropyForEachRecord(self ,listpr , agelower , ageupper , listofkeys):
        '''
        obsese: Flag to calculate for obese/ non-obese / or both. True means
        calucalete for just obese. False mean for false and None means for every 
        body.
        '''
        uni, bi , tri = self.utilityFunction(listpr, agelower, ageupper, listofkeys)
        for record in listpr:
            for key in listofkeys:
                ufreqdist = uni.get(key).freqdist
                bfreqdist = bi.get(key).freqdist
                tfreqdist = tri.get(key).freqdist
                self.calculateEntropy(record, 1, key, ufreqdist, agelower, ageupper)
                self.calculateEntropy(record, 2, key, bfreqdist, agelower, ageupper)
                self.calculateEntropy(record, 3, key, tfreqdist, agelower, ageupper)
    
    def caluculateJointProbForEachRecord(self ,listpr , agelower , ageupper , listofkeys):
        '''
        obsese: Flag to calculate for obese/ non-obese / or both. True means
        calucalete for just obese. False mean for false and None means for every 
        body.
        '''
        uni, bi , tri = self.utilityFunction(listpr, agelower, ageupper, listofkeys)
        for record in listpr:
            for key in listofkeys:
                ufreqdist = uni.get(key).freqdist
                bfreqdist = bi.get(key).freqdist
                tfreqdist = tri.get(key).freqdist
                self.jointprobability(record, 1, key, ufreqdist, agelower, ageupper)
                self.jointprobability(record, 2, key, bfreqdist, agelower, ageupper)
                self.jointprobability(record, 3, key, tfreqdist, agelower, ageupper)            
    def utilityFunction(self, listrecords , agelower, ageupper, listofkeys):
        '''
        Utility Function to study the freq dist of some of the fields 
        kids
        '''
        listpr = listrecords
        for field in listofkeys:
            self.unigrams[field] = ngramcontainer(1,field, agelower, ageupper)
            self.bigrams[field] = ngramcontainer(2,field, agelower, ageupper)
            self.trigrams[field] = ngramcontainer(3,field, agelower, ageupper)
        for personalrecord in listpr:
            for timeattrs in personalrecord.getalltimeattribute():
                if  timeattrs.getage().compare(Decimal(agelower)) >= 0 and \
                timeattrs.getage().compare(Decimal(ageupper)) <= 0:
                    if timeattrs.getattribute('DOC') is not None:
                        print 'doc'
                    else:
                        print 'no doc' 
            for timeattrs in personalrecord.getalltimeattribute():
                if  timeattrs.getage().compare(Decimal(agelower)) >= 0 and \
                timeattrs.getage().compare(Decimal(ageupper)) <= 0 \
                and timeattrs.getattribute('DOC') is not None:
                    doc = timeattrs.getattrissbute('DOC')
                    for key in listofkeys:
                        if doc.text.get(key) is not None:
                    
                            self.unigrams.get(key).populatefreqdist(doc.text.get(key))
                            self.bigrams.get(key).populatefreqdist(doc.text.get(key))
                            self.trigrams.get(key).populatefreqdist(doc.text.get(key))
            
        return (self.unigrams, self.bigrams, self.trigrams)
     
    def adddocument(self, doc):
        self.collections.append(doc)
        
    def processtext(self, personalrecord=None):
        if personalrecord is not None:
            mrn = personalrecord.getgenericattribute('MRN')
            prn = self.basestorage.getrecord(mrn)
            for timeattrs in prn.getalltimeattribute():
                age = timeattrs.getage()
                if self.lowage is not None and age.compare(Decimal(self.lowage)) >= 0 and age.compare(Decimal(self.upage)) <= 0:
                    docid = documentid((mrn, age))
                    doc = document(docid, fieldstoget)
                    text = timeattrs.getattribute('NOTES')
                    timeattrs.setattribute('NOTES', None)
                    if text is not None:
                        doc.parsetext(text)
                        if prn is not None and len(doc.text.keys()) > 0:
                            prn.addtimeattributewithnorder(age, 'MONTHS', 'DOC', doc)
                            #    print prn.getmrn()
                        else:
                            self.collections.append(doc)
                            print 'adding to collections'
                    
                     
            
 
    def printdoctexts(self, listofkeys, filename=None):
        fhandle = None
        if filename is not None:
            fhandle = open(filename, 'w')
            
        for doc in self.collections:
            if fhandle is None:
                print '\n\n'
                print 'information for ',' ', doc.documentid.name , ' at age ', doc.documentid.age
            else:
                fhandle.write('\n\n')    
                fhandle.write('information for '+' '+ str(doc.documentid.name) +' at age '+ str(doc.documentid.age))
                fhandle.write('\n')
            for key in listofkeys:
                if doc.text.get(key) is not None:
                    strng = '[' + key + ']'+'\n'
                    if fhandle is None:
                        print strng
                        print doc.text.get(key)
                    else:
                        fhandle.write('\n')
                        fhandle.write(strng)
                        fhandle.write('\n')
                        for val in doc.text.get(key):
                            fhandle.write(str(val))
                            fhandle.write('  ')
                        fhandle.write('\n')
                            
        if filename is not None:
            fhandle.close()

class field:
    '''
    A class representing a text and the type of text.
    For example we can have a name field and the value it will have
    id the name of person. Name also represents the identifiable field in
    text which want to filter out.
    '''
    def __init_(self, name, text):
        self.name = name
        self.text = text
        
class document():
    '''
    Build a document object from the text.
    text: The text which will be parsed to  populate various fields.
    fieldlist: Name of fields which we are interested to filter out.
    dcid: It is a tuple with first element as the unique id and
    the second element is the age at which this was created
    '''
    def __init__(self, docid , fields):
        self.documentid = docid
        # following field repesents the field we are interested to get from text
        self.fields = fields
        '''
        a dictionary of fields and its content
        '''
        self.text = dict()
    
    def parsetext(self, text):
        rawtokens = text.split()
        nextexpectedmatch = None
        matchedposition = 0
        prevfield = None
        currentfield = None
        fullvalue = list()
        matchedToks = []
        matchobj = None
                     
        for tok in rawtokens:
            if nextexpectedmatch is None:
                matchobj = re.match(mainfieldmatch, tok)
                if matchobj:
                    matchedToks.append(tok)
                    nextexpectedmatch = nextexpected(matchedToks)
                    if nextexpectedmatch is None:
                        matchedposition = 0;
                        currentfield = getfield(matchedToks )
                        matchedToks = []
                        if prevfield is None:
                            prevfield = currentfield
                    else:
                        matchedposition = 1
                if  not matchobj   and currentfield != prevfield  and nextexpectedmatch is None:
                    self.text[prevfield] = fullvalue
                    fullvalue = list()
                    stem = nltk.PorterStemmer().stem(tok).lower()
                    fullvalue.append(stem)
                    prevfield = currentfield
                elif not matchobj:
                    stem = nltk.PorterStemmer().stem(tok).lower()
                    fullvalue.append(stem)               
            else:
                for expectedmatch in nextexpectedmatch:
                    if '?' in expectedmatch:
                        tomatch = expectedmatch.replace('?','[?]')
                    else:
                        tomatch = expectedmatch
                    matchobj = re.match('^[[]*\s*'+tomatch+'\s*[]]*$', tok)
                    if matchobj:
                        break
                if matchobj:
                    matchedToks.append(tok)
                    nextexpectedmatch = nextexpected(matchedToks)
                    if nextexpectedmatch is None:
                        matchedposition = 0;
                        currentfield = getfield(matchedToks )
                        matchedToks = []
                        if prevfield is None:
                            prevfield = currentfield
                    else:
                        matchedposition = matchedposition  + 1
                else:      
                    for token in matchedToks:                        
                        fullvalue.append(nltk.PorterStemmer().stem(token).lower())

                    stem = nltk.PorterStemmer().stem(tok).lower()
                    fullvalue.append(stem)
                    matchedToks = []
                    currentfield = prevfield
                    nextexpectedmatch = None
                    
        