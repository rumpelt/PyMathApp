'''
Created on Sep 19, 2011

@author: Ashwani Rao
'''

import xml.sax
import data.personalrecord as record
from xml.sax.saxutils import unescape
from decimal import Decimal
class _SaxParser(object):
    def __init__(self, filename, basestorage):
        self.__basestorage = basestorage
        self._filename = filename
        
    def parsexml(self):
        ifile = open(self._filename)
        xml.sax.parse(ifile, _SaxParser.PersonalRecordContentHandler(self.__basestorage))
         
    class PersonalRecordContentHandler(xml.sax.ContentHandler):
        '''
                Contenet handler for the personal record for following dtd
                dtd= "<?xml version=\"1.0\"?>" + "\n"+
               "<!DOCTYPE RECORDS [" + "\n"+
               "<!ELEMENT RECORDS  (PERSON+)>" + "\n"+
                "<!ELEMENT PERSON  (GENERICATTRIBUTE+,TIMEBASEDATTRIBUTE*)>" + "\n"+
                "<!ELEMENT GENERICATTRIBUTE  (ATTRIBUTES*)>" + "\n"+
                "<!ELEMENT TIMEBASEDATTRIBUTE  (TIMEATTRIBUTES*)>" + "\n"+
                "<!ELEMENT ATTRIBUTES  (#PCDATA)>" + "\n"+
                "<!ELEMENT TIMEATTRIBUTES  (#PCDATA)>" + "\n"+
                "<!ATTLIST  PERSON  uid ID #REQUIRED>" + "\n"+
                "<!ATTLIST  PERSON  lastname CDATA  #REQUIRED>" + "\n"+
                "<!ATTLIST  PERSON  givenname CDATA  #REQUIRED>" + "\n"+
                "<!ATTLIST  PERSON  middlename CDATA  #IMPLIED>" + "\n"+
                "<!ATTLIST  ATTRIBUTES name CDATA  #REQUIRED>" +"\n"+
                // following attribute give some information on the name above
                // for example dob (dateofbirth) attribute can be unix style or in regular date format.
                "<!ATTLIST  ATTRIBUTES type CDATA  #IMPLIED>" + "\n"+ 
                "<!ATTLIST  TIMEBASEDATTRIBUTE age CDATA  #REQUIRED>" +"\n"+
                "<!ATTLIST  TIMEBASEDATTRIBUTE agetype CDATA  #REQUIRED>"+"\n"+
                "<!ATTLIST  TIMEATTRIBUTES name CDATA  #REQUIRED>" +"\n"+
                // following attribute give some information on the name above
                "<!ATTLIST  TIMEATTRIBUTES type CDATA  #IMPLIED>"+ "\n"+
                "]>";
        '''
        
        
        def __init__(self, basestorage):
            xml.sax.ContentHandler.__init__(self)
            self.genericattrs = None
            self.timeattrs = None
            self.value = []
            self.attributetype = None
            self.attributename = None
            self.__basestorage = basestorage
    
        def startElement(self, name, attrs):
            '''
            start of element
            '''
            if  name == 'PERSON':
                self.personalrecord = self.__basestorage.getrecord(Decimal(attrs.getValue('MRN')))
                if self.personalrecord is None:
                    self.personalrecord = record.PersonalRecord()
                    self.personalrecord.addgenericattribute('MRN', attrs.getValue('MRN'))
                    self.personalrecord.addgenericattribute('LASTNAME', attrs.getValue('LASTNAME'))
                    self.personalrecord.addgenericattribute('GIVENNAME', attrs.getValue('GIVENNAME'))
            elif name ==  'TIMEBASEDATTRIBUTE':
                self.timeattrs = record._TimeAttribute(attrs.getValue('age'), attrs.getValue('agetype'))
            elif name ==  'GENERICATTRIBUTE':
                self.genericattrs = dict()
            elif name == 'ATTRIBUTES' or name == 'TIMEATTRIBUTES':
                self.attributename = attrs.getValue('name')
                if (not ( attrs.get('type') is None)):
                    self.attributetype = attrs.get('type')
            
        def endElement(self, name):
            if  name == 'PERSON':
                self.__basestorage(self.personalrecord)
                self.personalrecord = None
            elif name == 'TIMEBASEDATTRIBUTE':
                self.timeattrs = None
            elif name == 'GENERICATTRIBUTE':
                self.genericattrs = None
            elif name == 'ATTRIBUTES' or name == 'TIMEATTRIBUTES':
                if (not (self.timeattrs is None)):
                    self.personalrecord.addtimeattributewithnorder(self.timeattrs.getage(),self.timeattrs.getagetype()
                                                          , self.attributename, ''.join(self.value))
                else:
                    self.personalrecord.addgenericattribute(self.attributename, ''.join(self.value))
                self.attributename = None
                self.attributetype = None
                self.value = []
        
        def characters(self, content):
            content = str(content)
            content = content.strip()
            content = content.strip('\n\t')
            content = unescape(content)

            if (len(content) > 0):
                self.value.append(content)
             
    