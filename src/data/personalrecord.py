'''
Created on Sep 16, 2011

@author: Ashwani Rao
'''
from decimal import Decimal

def isnumeric(val):
    try:
        Decimal(val)
        return True
    except:
        return False

class AllRecords(object):
    
    def __call__(self, personalrecord = None):
        '''
        Call method to directly add a personal recods instance
        '''
        if personalrecord is not None:
            self.addrecord(personalrecord)
    def __init__(self, key = 'MRN'):
        self.__allrecords = dict()
        self.__key = key
    
    
    def addrecord(self, pr):
        if self.__allrecords.get(pr.getgenericattribute(self.__key)) is None:
            self.__allrecords[pr.getgenericattribute(self.__key)] = pr
            
    def getmalerecords(self):
        males = list();
        for record in self.__allrecords.values():
            if record.getgenericattribute('SEX') == 'M' and \
            record.getgenericattribute('MOTHERMRN').compare(Decimal("-1")) != 0:
                males.append(record)            
        return males
    def getfemalerecords(self):
        females = list();
        for record in self.__allrecords.values():
            if record.getgenericattribute('SEX') == 'F' and \
            record.getgenericattribute('MOTHERMRN').compare(Decimal("-1")) != 0:
                females.append(record)            
        return females
        
    def getmotherrecords(self):
        females = list();
        for record in self.__allrecords.values():
            if record.getgenericattribute('SEX') == 'F' and record.getgenericattribute('MOTHERMRN') is  None:
                females.append(record)            
        return females
            
    def getallrecords(self):
        return self.__allrecords.values()
    
    def getallobese(self ,agelower ,ageupper ,sex):
        if sex == 'M':
            listpr = self.getmalerecords()
        elif sex == 'F':
            listpr = self.getfemalerecords()
        elif sex == 'B':
            listpr = self.getallbabies()
        result = list()
        for pr in listpr:
            if pr.getobese(agelower ,ageupper ,'MONTHS') == 1:
                result.append(pr);
    def getallnonobese(self ,agelower ,ageupper ,sex):
        listpr = self.getallbabies()
        result = list()
        for pr in listpr:
            if pr.getobese(agelower ,ageupper ,'MONTHS') == 0:
                result.append(pr);
                
  
                
    def getallbabies(self):
        result = list()
        result.extend(self.getmalerecords())
        result.extend(self.getfemalerecords())
        return result
    
    def getrecord(self,   mrn):
        return self.__allrecords.get(mrn)
   
                    
class _TimeAttribute(object):
    '''
         Attributes of the personal record which are collected at a particular
         age: This parameter specify the 
        agetype : This parameter represent the age is in months or years or days.      
    '''
    def __init__(self, age, agetype='MONTHS'):
        self.__agetype  = agetype
        self.__age = Decimal(age)
        self.__atributes = dict()
        self.__stringAtributes= dict()
        
    def getagetype(self):
        return self.__agetype
    
    def getage(self):
        return self.__age
    def getallnumericattributes(self):
        return self.__atributes
    
    def getallstringattributes(self):
        return self.__stringAtributes
    
    def getnumnumericattributes(self):
        return len(self.__atributes.items())
    
    def getnumstringattributes(self):
        return len(self.__stringAtributes.items())
    def addattribute(self, age, key, value):
        '''
        Adds an attribute and corresponding values.
        Returns true if addition is successful else false.
        Will Raise an error if the age is not equal to age of this class
        '''
        if (self.__age.compare(age) == 0):
            if (key and value):
                if isnumeric(value):
                    self.__atributes[key] = Decimal(value)
                else:
                    self.__stringAtributes[key] = value
                return True
            else:
                return False
        else:
            raise("problem with age " + self.__age + " adding for age "+ age)
    
    def setattribute(self, key, value):
        '''
        set a key to particular value. Used to reset an already present key.
        Can be used other wise also i.e. to set to a particular key.
        '''
        if value is None:
            if key in self.__atributes.keys():
                self.__atributes.pop(key)
            elif key in self.__stringAtributes.keys():
                self.__stringAtributes.pop(key)
        elif isnumeric(value):
            self.__atributes[key] = Decimal(value)
        else:
            self.__stringAtributes[key] = value
            
    def getattribute(self, key):
        '''
        Gets the value of attribute associate with a key
        '''
        if self.__atributes.get(key) is None:
            return self.__stringAtributes.get(key)
        return self.__atributes.get(key)
        
    
class PersonalRecord(object):
    '''
    classdocs: Class representing the a personal record having attributes
    generic and time based. For example record number , age, sex, ethinicity
    are generic attributes.
    '''


    def __init__(self):
        '''
        Constructor
        self.__genericAttribute : contains single value or list of values if there is more than one value 
        possible for a key
        '''
        self.__genericAttribute = dict()
        self.__timeattributes =  list()
        
  
    def cleartimeattributes(self):
        self.__timeattributes =  list()
    def cleargenericattributes(self):
        self.__genericAttribute =  list()
    def getmrn(self):
        '''
        gets the medical record number
        '''
        return self.getgenericattribute('MRN')
      
    def setsex(self, sex):
        '''
        set the sex of the person.
        '''
        
        self.__sex = sex
        
    def setuid(self, uid):
        '''
        set a unique generated identifier for this record
        '''
        self.__uid = uid
    
    def getuid(self):
        '''
        sets the unique identifier generated by me
        '''
        return self.getgenericattribute('UID')
            
    def  setdob(self, uid):
        '''
        set the date of birth of this person
        '''
        self.__dob = uid
    def removegenricattribute(self, key):
        self.__genericAttribute.pop(key)
        
    def setgenericattribute(self, key, value):
        if value is None:
            if self.__genericAttribute.get(key) is not None:
                self.__genericAttribute.pop(key)
        else:
            if isnumeric(value):
                val = Decimal(value)
            else:
                val = value
            self.__genericAttribute[key] = val 
    def addgenericattribute(self, key, value):
        if (len(key)> 0 and len(value) > 0):
            if isnumeric(value):
                val = Decimal(value)
            else:
                val = value
            self.__genericAttribute[key] = val
            
    def appendgenericattribute(self, key, value):
        '''
        Adds a generic attribute to the record. For example 
        ethinicity, dob, sex, etc
        '''
        if (len(key)> 0 and len(value) > 0):
            if isnumeric(value):
                val = Decimal(value)
            else:
                val = value
            if (not (self.__genericAttribute.get(key) is None)):
                if (hasattr(self.__genericAttribute.get(key), '__iter__')):
                    self.__genericAttribute.get(key).append(val)
                else:
                    newlist = list()
                    newlist.append(self.__genericAttribute.get(key))
                    newlist.append(val)
                    self.__genericAttribute[key] = newlist
            else:
                self.__genericAttribute[key] = val
            return True
        else:
            return False
        
        
    def getgenericattributeiterator(self):
        return self.__genericAttribute.iteritems()           
    def getgenericattribute(self, key):
        return self.__genericAttribute.get(key)
        
    def gettimeattribute(self, age, agetype='MONTHS'):
        '''
        '''
        
        for val in self.__timeattributes:
            if (agetype == val.getagetype() and 
                Decimal(age).compare(val.getage()) == 0 ):
                return val
        return None                
    
    def getAttributeAtEachAgePoint(self, attribute):
        result = dict()
        for attr in self.__timeattributes:
            if attr.getattribute(attribute) is not None:
                result[attr.getage()] = attr.getattribute(attribute)
        if len(result.keys()) > 1:
            return result 
        return None
            
    def getattribute(self, key, lowage, upage, agetype='MONTHS'):
        if self.__genericAttribute.get(key) is not None:
            return self.__genericAttribute.get(key)
        for attr in self.__timeattributes:
            if  attr.getagetype() == agetype and (attr.getage().compare(Decimal(lowage)) < 0  or attr.getage().compare(Decimal(upage)) > 0 ):
                continue
            if attr.getattribute(key) is not None:
                return attr.getattribute(key)
        return None
    def getalltimeattribute(self):
        '''
        returns the collection self.__timeattributes which consists of
        _TimeAttribute objects
        '''
        
        return self.__timeattributes
    
    def getatributeinperiod(self, key,  lowage , upage,agetype='MONTHS'):
        '''
        look for a attribute denoted by key in the period from lowage
        till upage. lowage is inclusive and upage is exclusive
        '''
        
        for tattr in self.__timeattributes:
            if (agetype == tattr.getagetype() and 
                Decimal(lowage).compare(tattr.getage()) <= 0 and 
                Decimal(upage).compare(tattr.getage()) > 0):
                if tattr.getattribute(key ) is not None:
                    return tattr.getattribute(key)
        return None
    
    def containsattribute(self, attribute , lowage , upage, agetype):
        if self.__genericAttribute.get(attribute) is not None:
            return True
        for attr in self.__timeattributes:
            if attr.getage().compare(Decimal(lowage)) < 0  and attr.getage().compare(Decimal(upage)) > 0 and attr.getagetype() == agetype:
                continue
            if attr.getattribute(attribute) is not None:
                return True
        return False
    def getobese(self, lowage, upage, agetype):
        '''
        check if a person is obese in any time in a given period from lowage 
        to upage
        '''
        result = None
        for attr in self.__timeattributes:
            if attr.getagetype() == agetype and (attr.getage().compare(lowage) < 0  or attr.getage().compare(upage) > 0):
                continue
            if  attr.getattribute('OBESITY') is not None and attr.getattribute('OBESITY').compare(Decimal('1')) == 0:
                return 1
            if  attr.getattribute('OBESITY') is not None and attr.getattribute('OBESITY').compare(Decimal('0')) == 0:
                result = 0
        return result
    def comparatorfunction(self, timeatt1, timeatt2):
        '''
        comparator function for two _TimeAttribute
        '''
        if (timeatt1.getage().compare(timeatt2.getage()) > 0):
            return 1
        elif (timeatt1.getage().compare(timeatt2.getage()) < 0):
            return -1
        else:
            return 0
    def sorttimeattributes(self):
        self.__timeattributes = sorted(self.__timeattributes,cmp=self.comparatorfunction)
                 
    def addtimeattribute(self, age, agetype, key, value):
        '''
        adds an attibute at a particular age
        '''
        timeattribute = self.gettimeattribute(age, agetype)
        if (timeattribute is None):
            timeattribute = _TimeAttribute(age, agetype)
            timeattribute.addattribute(age, key, value)
            self.__timeattributes.append(timeattribute)
            sorted(self.__timeattributes,cmp=self.comparatorfunction)
        else:
            timeattribute.addattribute(age, key, value)
    
    def addtimeattributewithnorder(self, age, agetype, key, value):
        '''
        adds an attibute at a particular age without caring for sorting
        of the timeattributes 
        '''
        timeattribute = self.gettimeattribute(age, agetype)
        if (timeattribute is None):
            timeattribute = _TimeAttribute(age, agetype)
            timeattribute.addattribute(age, key, value)
            self.__timeattributes.append(timeattribute)
        else:
            timeattribute.addattribute(age, key, value)
    
    