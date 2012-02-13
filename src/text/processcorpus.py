'''
Created on Nov 3, 2011

@author: ashwani
'''
import sys
import getopt
import parsing.xmlsaxparser as myparser2
from ngram import ngramsfreq
from documents import documents
#following class implement the processtext function
ngramfreq = ngramsfreq()
documents = documents()
def processInputXml(filename, objectHandler):
    myparser2._SaxParser(filename, objectHandler).parsexml()
    
class ProcessCorpus:
    def __init__(self, callerobject, basestorage):
        '''
        self.function to invoke for parsing text
        callerobject implements method processtext. Currently there are two
        classes which does that documents class and ngramfreq class
        '''
        self.__callerobject = callerobject
        self.__basestorage =  basestorage
    def __call__(self, personalrecord = None):
        self.__callerobject.processtext(personalrecord)
        
    def getrecord(self, key):
        if self.__basestorage is None:
            return None
        return self.__basestorage.getrecord(key)
def main(argv=None):
    i = 0
    if argv is None:
        print "none argument"
        argv = sys.argv
        i = 1
   
    print argv 
    opts, args = getopt.getopt(argv[i:], '', ["help","txml=","oxml="])
    print opts
    for o ,a in opts:
        if (o == '--txml'):
            print "procesing xmlfile"
            processInputXml(a ,ProcessCorpus(documents))
        else:
            print "could not identify"


if __name__ == "__main__":
    sys.exit(main())