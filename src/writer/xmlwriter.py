'''
Created on Sep 23, 2011

@author: Ashwani Rao
'''


dtd = "<?xml version=\"1.1\" encoding=\"utf-8\"?>" + "\n" \
"<!DOCTYPE RECORDS [" + "\n" \
"<!ELEMENT RECORDS  (PERSON+)>" + "\n" \
"<!ELEMENT PERSON  (GENERICATTRIBUTE+,TIMEBASEDATTRIBUTE*)>" + "\n" \
"<!ELEMENT GENERICATTRIBUTE  (ATTRIBUTES*)>" + "\n" \
"<!ELEMENT TIMEBASEDATTRIBUTE  (TIMEATTRIBUTES*)>" + "\n" \
"<!ELEMENT ATTRIBUTES  (#PCDATA)>" + "\n" \
"<!ELEMENT TIMEATTRIBUTES  (#PCDATA)>" + "\n" \
"<!ATTLIST  PERSON  uid ID #REQUIRED>" + "\n" \
"<!ATTLIST  PERSON  lastname CDATA  #REQUIRED>" + "\n" \
"<!ATTLIST  PERSON  givenname CDATA  #REQUIRED>" + "\n" \
"<!ATTLIST  PERSON  middlename CDATA  #IMPLIED>" + "\n" \
"<!ATTLIST  ATTRIBUTES name CDATA  #REQUIRED>" +"\n" \
                # following attribute give some information on the name above
                # for example dob (dateofbirth) attribute can be unix style or in regular date format.
"<!ATTLIST  ATTRIBUTES type CDATA  #IMPLIED>" + "\n" \
"<!ATTLIST  TIMEBASEDATTRIBUTE age CDATA  #REQUIRED>" +"\n" \
"<!ATTLIST  TIMEBASEDATTRIBUTE agetype CDATA  #REQUIRED>"+"\n" \
"<!ATTLIST  TIMEATTRIBUTES name CDATA  #REQUIRED>" +"\n" \
# following attribute give some information on the name above
"<!ATTLIST  TIMEATTRIBUTES type CDATA  #IMPLIED>"+ "\n"\
"]>"

class recordxmlwriter():
    def __init__(self, filename , datadefinition = dtd):
        self.filehandle = open(filename,"w")
        self.dtd = datadefinition
    
    def writeoutput(self, records):
        self.filehandle.write(self.dtd)
        self.filehandle.write("<RECORDS>\n")
        
        for  p in records:
            mrn = p.getgenericattribute('MRN')
            lastname = p.getgenericattribute('LASTNAME')
            givenname = p.getgenericattribute('GIVENNAME')
            self.filehandle.write("<PERSON MRN=\""+str(mrn)+"\""+" LASTNAME=\""+lastname+"\"" \
                                  +" GIVENNAME=\""+givenname+"\""+">")
            self.filehandle.write("\n")
            self.filehandle.write("<GENERICATTRIBUTE>")            
            for key, value in p.getgenericattributeiterator():
                self.filehandle.write("<ATTRIBUTES name=\""+key+"\" >")
                self.filehandle.write(str(value))
                self.filehandle.write("</ATTRIBUTES>\n")
                
            self.filehandle.write("</GENERICATTRIBUTE>\n")
            for timeattr in p.getalltimeattribute():
                self.filehandle.write("<TIMEBASEDATTRIBUTE age=\""+str(timeattr.getage())+"\""+ \
                            " agetype=\""+timeattr.getagetype()+"\""+">"+"\n")
                for key, value in timeattr.getallnumericattributes().items():
                    self.filehandle.write("<TIMEATTRIBUTES name=\""+key+"\""+">")
                    self.filehandle.write(str(value))
                    self.filehandle.write("</TIMEATTRIBUTES>"+"\n")
                for key, value in timeattr.getallstringattributes().items():
                    self.filehandle.write("<TIMEATTRIBUTES name=\""+key+"\""+">")
                    self.filehandle.write(value)
                    self.filehandle.write("</TIMEATTRIBUTES>"+"\n")                       
                self.filehandle.write("</TIMEBASEDATTRIBUTE>"+"\n")
            self.filehandle.write("</PERSON>"+"\n")
            
        self.filehandle.write("</RECORDS>"+"\n")
        self.filehandle.close()

    