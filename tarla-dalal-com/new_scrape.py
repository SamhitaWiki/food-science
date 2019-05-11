# -*- coding: utf-8 -*-
"""
Created on Wed May  8 15:24:25 2019

@author: Rajesh
"""

from bs4 import BeautifulSoup
import requests
import re
import csv
import pandas as pd

page = requests.get('https://www.tarladalal.com/latest_recipes.aspx?pageindex=1')
soup=BeautifulSoup(page.text,'lxml')
tag=soup('a',{'class':"respglink"})
    
for t in tag:
   s=str(t)
   s1=re.search('([0-9]+)',s)
   k=int(s1.group(0))
   
for i in range(k):
    page = requests.get('https://www.tarladalal.com/latest_recipes.aspx?pageindex=%d'%(i))
    soup=BeautifulSoup(page.text,'lxml')
    #tag=soup('a',{'class':"respglink"})
    date  = soup.find_all('span',{"style":"font-size:8pt;color:#636770;"})
    for a in date:
        print(a.text)
    
date   

new = soup.find('span',{"style":"font-size:8pt;color:#636770;"}) 
new.find('br')
print(new.text)