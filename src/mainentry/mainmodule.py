'''
Created on Sep 19, 2011
@author: Ashwani Rao
'''
import sys
import getopt
import parsing.xmlsaxparser as myparser
import data.personalrecord as records
from text import processcorpus as pc
from text import documents




class Usage(Exception):
    def __init__(self, msg):
        self.message = msg

def outputToXml(filename):
    return

def processInputXml(filename , objectHandler):
    myparser._SaxParser(filename, objectHandler).parsexml()
    
def main(argv=None):
    '''
    argv got to be a list else it will be problem when you execute this from the 
    python idle
    '''
    lowage = None
    upage = None    
    i = 0
    
    if argv is None:
        print "none argument"
        argv = sys.argv
        i = 1
    else:
        print argv 
    basestorage = None
    alldocuments = None
    opts, args = getopt.getopt(argv[i:], '', ["help","ixml=","txml=","oxml=", "lowage=", "upage="])
    for o ,a in opts:
        if (o == '--ixml'):
            print "procesing xmlfile"
            
            if basestorage is None:
                basestorage = records.AllRecords()
            processInputXml(a , basestorage)
        elif (o == '--lowage'):
            lowage = a 
        elif (o == '--upage'):
            upage = a
        elif (o == '--txml'):
            print "procesing text xmlfile"
           
            if alldocuments is None:
                alldocuments = documents.documents(basestorage, lowage , upage)
            processInputXml(a , pc.ProcessCorpus(alldocuments , basestorage))
        elif (o == '--oxml'):
            outputToXml(a)
        elif (o == '--test'):
            outputToXml(a)
        else:
            print "could not identify"
    return basestorage
   

if __name__ == "__main__":
    sys.exit(main())

    