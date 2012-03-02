'''
Created on Nov 2, 2011

@author: Ashwani Rao
'''
import csv
import nltk
from decimal import Decimal
from utility import decimalroutines as dd
class csvwriter():
    def __init__(self,filename, dlimter=',',  openmode = 'wb', quoting = csv.QUOTE_NONNUMERIC):
        self.filename = filename
        self.openmode = openmode
        self.filehandle = open(filename, self.openmode)
        self.writer = csv.writer(self.filehandle,dialect=csv.excel,quoting=quoting,delimiter =dlimter)
    
    def createwriter(self):
        return None
    
    def closewriter(self):
        self.filehandle.close()

    def writerow(self, row):
        self.writer.writerow(row)
        
    def writerows(self, rows):
        self.writer.writerows(rows)
    
    def createcsvdatafromkwargs(self, *args,**kwargs):
        '''
        a much improved version creating csv data on fly.
        *args is list of unique identifier for which we are getting the csv data.
        these identifiers represents each row.
        **kwargs: Represents variable number dictionaries of measurements indexed by
        the unique identifiers
        '''
        rows = list()
        headerrow= list()
        headerrow.append('ID')
        for key in kwargs:
            headerrow.append(str(key))
        rows.append(headerrow)
        uids = list()
        for uid in args:
            for ids in uid:
                uids.append(ids)
        for uid in uids:
            row = list()
            row.append(str(uid))
            for key in kwargs:
                if (kwargs[key]).get(uid) is not None:
                    row.append(kwargs[key].get(uid))
                else:
                    row.append('')
            rows.append(row)
        return rows    
    def createcsvdata(self, listpr,  attributes , lowage , upage):
        rows = list()
        for p in listpr:
            row = list()
            flag = True
            for att in attributes:
                gval  = p.getgenericattribute(att)                
                if p.getgenericattribute(att) is not None:
                    row.append(gval)
                elif p.getatributeinperiod(att,lowage,upage) is not None:
                    row.append(p.getatributeinperiod(att,lowage,upage))
                else:
                    flag = False
                    row.append('NA')
            if flag:
                rows.append(row)
        return rows
        
    def testwriter(self):
        freqdist = nltk.FreqDist()
        freqdist.inc(('eu' , 'tu'))
        freqdist.inc(('eu' , 'tu'))        
        freqdist.inc(('eu' , 'tu'))        
        freqdist.inc(('eu' , 'fu'))
        freqdist.inc(('gu' , 'tu'))
        freqdist.inc(('eu' , 'fu'))
        freqdist.inc(('eu' , 'fu'))
        freqdist.inc(('gu' , 'mu'))
        freqdist.inc(('gu' , 'mu'))
        dc = dd.decimalroutines()
        for item in freqdist:
            prob = freqdist.get(item) / freqdist.N()
            op = list()
            op.append(item)
            op.append(dc.getstring(prob, Decimal('.000000001')))
            self.writer.writerow(op)
        self.writer.closewriter()
    