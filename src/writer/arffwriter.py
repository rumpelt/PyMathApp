'''
Created on Jan 25, 2012

@author: Ashwani Rao
'''

class arffwriter(object):
    '''
    classdocs
    arff writer for weka analysis
    '''


    def __init__(self, filename=None):
        '''
        Constructor
        '''
        self.filename = filename
    
    def getattribute(self, pr , att):
        val = pr.getgenericattribute(att)
        if  val is not  None:
            return val
        return '?'
    
    def writegeneric(self, pr , fhandle):
        fhandle.write(str(self.getattribute(pr, 'SEX')))            
        fhandle.write(',')
        fhandle.write(str(self.getattribute(pr, 'MOTHERETHINICITY')))            
        fhandle.write(',')
        fhandle.write(str(self.getattribute(pr, 'SMOKINGLOW')))
        fhandle.write(',')
        fhandle.write(str(self.getattribute(pr, 'SMOKINGHIGH')))            
        fhandle.write(',')
        if self.getattribute(pr, 'DELIVERYMETHOD') != '?':
            fhandle.write(str('\''+self.getattribute(pr, 'DELIVERYMETHOD') +'\''))
        else:
            fhandle.write('?')            
        fhandle.write(',')
        fhandle.write(str(self.getattribute(pr, 'GRAVIDA')))            
        fhandle.write(',')
        fhandle.write(str(self.getattribute(pr, 'MOTHERPREPREGNANCYBMI')))            
        fhandle.write(',')
        fhandle.write(str(self.getattribute(pr, 'LOS')))            
        fhandle.write(',')
        fhandle.write(str(self.getattribute(pr, 'PARA')))            
        fhandle.write(',')
        fhandle.write(str(self.getattribute(pr, 'GESTATIONALDIABETES')))            
        fhandle.write(',')
        fhandle.write(str(self.getattribute(pr, 'BIRTHWEIGHT')))            
        fhandle.write(',')
        if self.getattribute(pr, 'PATIENTTYPE') != '?':
            fhandle.write(str('\''+self.getattribute(pr, 'PATIENTTYPE') +'\''))
        else:
            fhandle.write('?')
        fhandle.write(',')
        fhandle.write(str(self.getattribute(pr, 'GESTATIONWEEKS')))            
        fhandle.write(',')
        fhandle.write(str(self.getattribute(pr, 'DIABETES')))            
        fhandle.write(',')
        fhandle.write(str(self.getattribute(pr, 'REGULARDIABETES')))            
        fhandle.write(',')
        fhandle.write(str(self.getattribute(pr, 'PREPREGNANCYWEIGHT')))            
        fhandle.write(',')
        fhandle.write(str(self.getattribute(pr, 'NICU')))            
        fhandle.write(',')
        fhandle.write(str(self.getattribute(pr, 'MOTHERHEIGHT')))            
        fhandle.write(',')
        fhandle.write(str(self.getattribute(pr, 'WEIGHTATDELIVERY')))            
        fhandle.write(',')            
        if self.getattribute(pr, 'DELIVERYTYPE') != '?':
            fhandle.write(str('\''+self.getattribute(pr, 'DELIVERYTYPE') +'\''))
        else:
            fhandle.write('?')
        fhandle.write(',')                     
        fhandle.write(str(self.getattribute(pr, 'INDUCED')))            
        fhandle.write(',')
        if self.getattribute(pr, 'LABORSTATUS') != '?':
            fhandle.write(str('\''+self.getattribute(pr, 'LABORSTATUS') +'\''))
        else:
            fhandle.write('?')
        fhandle.write(',')
        fhandle.write(str(self.getattribute(pr, 'LENGTHOFLABOR')))            
        fhandle.write(',')
        if self.getattribute(pr, 'FEEDING') != '?':
            fhandle.write(str('\''+self.getattribute(pr, 'FEEDING') +'\''))
        else:
            fhandle.write('?')
        fhandle.write(',')
    
    def write(self,  listpr , filename=None ):
        if (filename is not None):
            self.filename = filename
        fhandle = open(self.filename, 'w')
        header = '@RELATION Babies\n' \
        + '@ATTRIBUTE uid STRING \n' \
        + '@ATTRIBUTE age NUMERIC \n' \
        + '@ATTRIBUTE sex {M,F} \n' \
        + '@ATTRIBUTE ethinicity {BL,WH,HI,AI,UN,AS} \n' \
        + '@ATTRIBUTE smokinglow {0 , 1} \n' \
        + '@ATTRIBUTE smokinghigh {0 , 1} \n' \
        + '@ATTRIBUTE deliverymethod {\'Spontaneous\' , \'Vacuum Extraction\' ,\'Forceps\',\'Forceps Outlet\'} \n' \
        + '@ATTRIBUTE gravida NUMERIC \n' \
        + '@ATTRIBUTE motherprepregnancybmi NUMERIC \n' \
        + '@ATTRIBUTE los  NUMERIC \n' \
        + '@ATTRIBUTE para  NUMERIC \n' \
        + '@ATTRIBUTE gestationaldiabetes  {0, 1} \n' \
        + '@ATTRIBUTE birthweight  NUMERIC \n' \
        + '@ATTRIBUTE patienttype  {\'Private\', \'Service\'} \n' \
        + '@ATTRIBUTE gestationweeks  NUMERIC \n' \
        + '@ATTRIBUTE diabetes  {0, 1 , 2}\n' \
        + '@ATTRIBUTE regulardiabetes  {0 ,1 } \n' \
        + '@ATTRIBUTE prepregnancyweight  NUMERIC \n' \
        + '@ATTRIBUTE nicu  {0 , 1} \n' \
        + '@ATTRIBUTE motherheight  NUMERIC \n' \
        + '@ATTRIBUTE weightatdelivery  NUMERIC \n' \
        + '@ATTRIBUTE deliverytype  {\'Vaginal\' , \'Primary Csection\'  , \'Rpt C/S Elective\' ,\'VBAC\' ,\'Rpt C/S Fail VBAC (N/E)\'} \n'\
        + '@ATTRIBUTE induced  {0, 1} \n' \
        + '@ATTRIBUTE laborstatus  {\'Spontaneous Labor\', \'Premature Labor\',\'Induction of Labor\' , \'No Labor\'} \n' \
        + '@ATTRIBUTE lenghtoflabor   NUMERIC \n' \
        + '@ATTRIBUTE feeding {\'Breast\' , \'Bottle\' ,\'Breast and Bottle\'  }\n' \
        + '@ATTRIBUTE headcrf NUMERIC \n'  \
        + '@ATTRIBUTE height NUMERIC \n' \
        + '@ATTRIBUTE heightzscore NUMERIC \n'\
        + '@ATTRIBUTE heightpercentile NUMERIC \n'\
        + '@ATTRIBUTE weight NUMERIC \n' \
        + '@ATTRIBUTE weightzscore NUMERIC \n' \
        + '@ATTRIBUTE weightpercentile NUMERIC \n' \
        + '@ATTRIBUTE weightlengthzscore NUMERIC \n'\
        + '@ATTRIBUTE weightlengthpercentile NUMERIC \n' \
        + '@ATTRIBUTE bmi NUMERIC \n' \
        + '@ATTRIBUTE bmizscore NUMERIC \n' \
        + '@ATTRIBUTE bmipercentile NUMERIC \n' \
        + '@ATTRIBUTE obesityrank {1 , 2, 3 , 4} \n' \
        + '@ATTRIBUTE obesity {0 , 1} \n'  
                
        fhandle.write(header)
        fhandle.write('@DATA\n')
        
        for pr in listpr:
            for timeattrs in pr.getalltimeattribute():
                
                fhandle.write(str(pr.getgenericattribute('UID')))
                fhandle.write(',')
                fhandle.write(str(timeattrs.getage()))
                fhandle.write(',')
                self.writegeneric(pr, fhandle)
                headcrf = timeattrs.getattribute('HEADCRF')
                height = timeattrs.getattribute('HEIGHT')
                heightzscore = timeattrs.getattribute('HEIGHTZSCORE')
                heightpercentile = timeattrs.getattribute('HEIGHTPERCENTILE')
                weight = timeattrs.getattribute('WEIGHT')
                weightzscore = timeattrs.getattribute('WEIGHTZSCORE')
                weightpercentile = timeattrs.getattribute('WEIGHTPERCENTILE')
                weightlengthzscore = timeattrs.getattribute('WEIGHTLENGTHZSCORE')
                weightlengthpercentile = timeattrs.getattribute('WEIGHTLENGTHPERCENTILE')
                bmi = timeattrs.getattribute('BMI')
                bmizscore = timeattrs.getattribute('BMIZSCORE')
                bmipercentile = timeattrs.getattribute('BMIPERCENTILE')                
                obesityrank = timeattrs.getattribute('OBESITYRANK')
                obesity = timeattrs.getattribute('OBESITY')
                if headcrf is None:
                    fhandle.write('?,')
                else:
                    fhandle.write(str(headcrf)+',')
                if height is None:                    
                    fhandle.write('?,')
                else:
                    fhandle.write(str(height)+',')
                if heightzscore is None:
                    fhandle.write('?,')
                else:
                    fhandle.write(str(heightzscore)+',')
                if heightpercentile is None:
                    fhandle.write('?,')
                else:
                    fhandle.write(str(heightpercentile)+',')
                if weight is None:
                    fhandle.write('?,')
                else:
                    fhandle.write(str(weight)+',')
                if weightzscore is None:
                    fhandle.write('?,')
                else:
                    fhandle.write(str(weightzscore)+',')
                if weightpercentile is None:
                    fhandle.write('?,')
                else:
                    fhandle.write(str(weightpercentile)+',')
                if weightlengthzscore is None:
                    fhandle.write('?,')
                else:
                    fhandle.write(str(weightlengthzscore)+',')
                if weightlengthpercentile is None:
                    fhandle.write('?,')
                else:
                    fhandle.write(str(weightlengthpercentile)+',')
                if bmi is None:
                    fhandle.write('?,')
                else:
                    fhandle.write(str(bmi)+',')
                if bmizscore is None:
                    fhandle.write('?,')
                else:
                    fhandle.write(str(bmizscore) +',')
                if bmipercentile is None:
                    fhandle.write('?,')
                else:
                    fhandle.write(str(bmipercentile)+',')
                if obesityrank is None:
                    fhandle.write('?,')
                else:
                    fhandle.write(str(obesityrank)+',')
                if obesity is None:
                    fhandle.write('?')
                else:
                    fhandle.write(str(obesity))
                fhandle.write('\n')    
        fhandle.close()