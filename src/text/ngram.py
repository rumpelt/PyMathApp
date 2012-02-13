'''
Created on Nov 3, 2011
routines on the ngrams found
@author: ashwani
'''
from  nltk.probability import FreqDist
from  nltk.collocations import *
from nltk import *
import nltk

class ngramsfreq:
    '''
     A class consisting of all the ngrams individual freq distribution of various words. 
    '''
    def __init__(self):
        self.words_fd = FreqDist()
        self.ngrams_fd = FreqDist()
        self.corpus = list()
  
        
    def collocationfinder(self, numresults):
        bigram_measures = nltk.collocations.BigramAssocMeasures()
        finder = BigramCollocationFinder.from_words(self.corpus)
        return finder.nbest(bigram_measures.pmi, numresults)  

    def processtext(self, personalrecord=None):
        if personalrecord is not None:
            for timeattrs in personalrecord.getalltimeattribute():
                text = timeattrs.getattribute('NOTES')
                words = text.split()
                for wd in words:
                    self.corpus.append(wd)
        