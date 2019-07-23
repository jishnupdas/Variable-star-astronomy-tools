#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 12:24:16 2019

@author: jishnu
"""

#%%
import sys
import pandas as pd

#%%
files = sys.argv[1:]

#%%
class WDformat:
    
    def __init__(self,file=None,df=None,light=None,magmn=None,phase=None,
                 mag=None):
        '''initialize variables'''
        
        self.file  = file
        self.df    = df
        self.phase = phase
        self.mag   = mag
        self.light = light
        self.magmn = magmn
    

    def convert_mag2light(self,file):
        '''
        convert mag to flux/light
        
        and write a file with 3 columns
        phase,light,error
        
        '''
        self.file    = file
        self.df      = pd.read_csv(self.file,sep='\t')
        self.phase   = self.df[self.df.columns[0]]
        self.mag     = self.df[self.df.columns[1]]
        
        self.magmn   = self.df[self.df.columns[1]].min()
        self.df['e'] = ['{:.2f}'.format(1.00) for i in range(len(self.mag))]
        
        self.light   = ['{:.5f}'.format(10**(-0.4*(m-self.magmn))) 
                        for m in self.mag]
        
        with open(file+'_light','w+') as outfile:
            for phase,ligt,err in zip(self.phase,self.light,self.df['e']):
                outfile.write('{:.5f}'.format(phase)+' '+ligt+' '+err+'\n')
    
    
    def format_to_columns(self):
        
        col_len      = len(self.mag)//3
        rmdr         = len(self.mag)%3
        
        len1,len2    = col_len,(col_len*2)+1
        
        #adjusting column heights according to length
        if   rmdr == 0:
            pass
        elif rmdr == 1:
            len1+=1
        elif rmdr == 2:
            len1+=1
            len2+=1
        else:
            print('Unexpected error!!')
            
        col1 = ['   0000'+'{:.5f}'.format(p)+'  '+l+'  '+e
                for p,l,e 
                in zip(self.phase[:len1],
                       self.light[:len1],
                       self.df['e'][:len1])]
        
        col2 = ['   0000'+'{:.5f}'.format(p)+'  '+l+'  '+e 
                for p,l,e 
                in zip(self.phase[len1:len2],
                       self.light[len1:len2],
                       self.df['e'][len1:len2])]
        
        col3 = ['   0000'+'{:.5f}'.format(p)+'  '+l+'  '+e 
                for p,l,e 
                in zip(self.phase[len2:],
                       self.light[len2:],
                       self.df['e'][len2:])]
        
        
        #making all columns equal length
        
        if   rmdr == 1:
            col2.append('')
            col3.append('')
        elif rmdr == 2:
            col3.append('')
        else:
            pass 
        
        with open(self.file+'.active','a+') as activefile:
            for c1,c2,c3 in zip(col1,col2,col3):
                activefile.write(c1+c2+c3+'\n')
        
#        return (col1,col2,col3),(len1,len2,len3)
                
#%%
for f in files:
    obj = WDformat()
    obj.convert_mag2light(f)
    obj.format_to_columns() 
    
#%%
'For testing'
#obj = WDformat()
#obj.convert_mag2light('953ligt')
#obj.format_to_columns()