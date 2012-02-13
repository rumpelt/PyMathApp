'''
Created on Feb 9, 2012

@author: 801155602
'''

import urllib
import decimal
from xml.dom.minidom import parseString

googleurl= 'http://maps.googleapis.com/maps/api/geocode/'
def getlatitudelongitude(address ,xml=True , sensor=False):
    if sensor:
        sense='true'
    else:
        sense='false'
    query=  dict(address=address ,sensor=sense)
    url= None
    
       
    if xml:
        url = googleurl+'xml?'
    else:
        url = googleurl+'json?'
    query = urllib.urlencode(query)
    url=url+query
    print url
    response = urllib.urlopen(url).read()
    #response = None
    lat = None
    longt = None
    if xml and response is not None:
        dom = parseString(response)
       # print address
       # print url
        locationlist = dom.getElementsByTagName('location')
        if  len(locationlist) > 0:
            latlist = locationlist[0].getElementsByTagName('lat')
            longlist = locationlist[0].getElementsByTagName('lng')
            
            if latlist is not None  and longlist is not None:
                latitude = latlist[0].toxml().replace('<lat>','')
                lat = decimal.Decimal(latitude.replace('</lat>',''))
                longt = decimal.Decimal(longlist[0].toxml().replace('<lng>','').replace('</lng>',''))
    if lat is not None:
        return (lat,longt)
    else:
        return None
       

def getaddressforrecord(p):
    add1 = p.getgenericattribute('ADDRESSLINE1')
    
    city = p.getgenericattribute('CITY')
    zipt = p.getgenericattribute('ZIPCODE')
    state = p.getgenericattribute('STATE')
    address = str(add1)+', '+str(city)+' '+str(zipt)+', '+str(state)
    res = getlatitudelongitude(address)
        
    if res is not None:
        lat,longt = res
        #p.addgenericattribute('LATITUDE', lat)
        #p.addgenericattribute('LONGITUDE', longt)
        print lat,'  ' ,longt
        
           
def populategeocode(listpr):
    for p in listpr:
        if p.getgenericattribute('LATITUDE') is not None:
            continue
        add1 = p.getgenericattribute('ADDRESSLINE1')
        add2=  p.getgenericattribute('ADDRESSLINE2')
        zipcode = p.getgenericattribute('ZIPCODE')
        city = p.getgenericattribute('CITY')
        state = p.getgenericattribute('STATE')
        if add2 is None:
            add2 = ''
        address = add1+', '+add2+', '+city+', '+str(zipcode)+', '+ state
        #print address
        #result = None
        
        result = getlatitudelongitude(address)
        if result is not None:
            latitude,longitude=result
            print latitude, ' ', longitude 
            p.addgenericattribute('LATITUDE',latitude)
            p.addgenericattribute('LONGITUDE',longitude)