# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 08:58:44 2019

@author: Rajesh
"""

import urllib.request
import pandas as pd
import csv

#import titlecase
from bs4 import BeautifulSoup
recipe = "https://www.tarladalal.com/Apple-Strawberry-Pur%C3%A9e-(-Baby-and-Toddler-Recipe)-3062r" #reading the url of the recipe
page1 = urllib.request.urlopen(recipe)
soup = BeautifulSoup(page1,features="lxml")

# Extracting the image url
try:
    img_link = soup.find('img', {"id":"ctl00_cntrightpanel_imgRecipe"})
    url = 'https://www.tarladalal.com/'+ img_link['src']
    print ('https://www.tarladalal.com/'+ img_link['src'])
except:
    pass

# Extracting the number of views 
try:    
    views = soup.find('span', {"id": "ctl00_cntrightpanel_lblViewCount"})
    abc = views.text.split()
    n = len(abc)
    view = abc[n-2] + ' ' +abc[n-1]
    print(abc[n-2] + ' ' +abc[n-1])
except:
    pass

recipe_id = 1
#finding the recipe name
recipe_name = soup.find("span",{"id": "ctl00_cntrightpanel_lblRecipeName"})
print("recipe name is ", recipe_name.text)


# Get the description of the recipe
sec = soup.find("div", {"id": "recipe_details_left"})
desc = sec.find('span', {"itemprop" : "description"})
print(desc.text)

#finding the Times
try:
    prep_time = soup.find("time", {"itemprop": "prepTime"})
    cook1 = prep_time.text.split()
    if (cook1[1] == 'hours') :
        pt = cook1[0]*60+cook1[2]
        print("Prep time in minutes is", cook1[0]*60+cook1[2])
    if (cook1[1] == 'hours.'):
        pt = cook1[0]*60
        print("Prep time in minutes is", cook1[0]*60)
    else:
        pt = cook1[0]
        print("Prep time in minutes is", cook1[0])
except:
    pass
    
try:
    cooking_time = soup.find("time", {"itemprop": "cookTime"})
    cook = cooking_time.text.split()
    if (cook[1] == 'hours') :
        ct = cook[0]*60+cook[2]
        print("Cooking time in minutes is", cook[0]*60+cook[2])
    if (cook[1] == 'hours.'):
        ct = cook[0]*60
        print("Cooking time in minutes is", cook[0]*60)
    else:
        ct = cook[0]
        print("Cooking time in minutes is", cook[0])
        
except:
    pass
    
try:
    total_time =  soup.find("time", {"itemprop": "totalTime"})
    cook2 = total_time.text.split()
    if (cook2[1] == 'hours') :
        tt =cook2[0]*60+cook2[2]
        print("total time in minutes is", cook2[0]*60+cook2[2])
    if (cook2[1] == 'hours.'):
        tt = cook2[0]*60
        print("total time in minutes is", cook2[0]*60)
    else:
        tt =cook2[0]
        print("total time in minutes is", cook2[0])
except:
    pass
    

try:
    csv_file = csv.reader(open('recipes.csv', "r"), delimiter=",")
    recipe_id = len(list(csv_file)) - 1    
except:
    pass
    
try:
    fields = [recipe_id+1, recipe_name.text, desc.text,pt,ct,tt,url,view] 
    with open(r'recipes.csv','a', newline='')as f:
        writer = csv.writer(f)    # converting dataframe to csv
        writer.writerow(fields) 
except:
    pass

############## Change This

# Get ingridients list
ingrident_table = []
quantity_table = []
#ingrident_table = pd.DataFrame(ingrident_table, columns = ['ingridents'])
#ingrident_table.loc[1:1 , 1:1] = 'abc'
#df.ix['','C']=10

ingridients = soup.find_all("span", {"itemprop": "recipeIngredient"})
qty_table =[]

print("recipe_id = ", recipe_id+1) 
for i in ingridients:
    csv_file = csv.reader(open('ingredients.csv', "r"), delimiter=",") # opening the existing csv file
    ing_name = i.select("span")[1].text.title()
    flag = 0
    count = 0
    #print("here count = ", count)
    for row in csv_file:
        
        count += 1
        #print("row = ", row, "count = ", count)
        if(len(row)==0):
            if(count==1):
                continue
            break
        if(ing_name==row[1]):
            s = i.select("span")[0].text.split()
            if (len(s)==0):
                qty_table.append([recipe_id+1, row[0][0], ' ', ' '])
                print(row[0])
            if (len(s)==1):
                qty_table.append([recipe_id+1, row[0], s[0], ' '])
                print(row[0])
         #   print(s.split()[1] )# checking the ingrident name with the name already present 
            if(len(s)==2):
                qty_table.append([recipe_id+1, row[0], s[0],s[1]])
            if(len(s)==3):
                if(s[1]=='to'):
                    qty_table.append([recipe_id+1, row[0], i.select("span")[0].text, ' '])
                else:
                    qty_table.append([recipe_id+1, row[0], s[0]+' '+s[1], s[2] ])
                
            flag = 1
    
    #print(ing_name, " status = ", flag, "count = ", count)
    if(not flag):
        fields = [count, ing_name]
       # s = i.select("span")[0].text
        s = i.select("span")[0].text.split()
        if (len(s)==0):
            qty_table.append([recipe_id+1, row[1], ' ', ' '])
            print(row[0])
            if (len(s)==1):
                qty_table.append([recipe_id+1, row[0], s[0], ' '])
         #   print(s.split()[1] )# checking the ingrident name with the name already present 
            if(len(s)==2):
                qty_table.append([recipe_id+1, row[0], s[0],s[1]])
            if(len(s)==3):
                if(s[1]=='to'):
                    qty_table.append([recipe_id+1, row[0], i.select("span")[0].text, ' '])
                else:
                    qty_table.append([recipe_id+1, row[0], s[0]+' '+s[1], s[2] ])
       # with open(r'ingredients.csv','a', newline='')as f:
        #    writer = csv.writer(f)
         #   writer.writerow(fields)  # converting dataframe to csv

print(qty_table)
#with open(r'ingredient_quantities.csv','a', newline='')as f:
 #           for fields in qty_table:
  #              writer = csv.writer(f)
   #             writer.writerow(fields)


method_table = []
# Get recepie instructions list
try:
    recInstructions = soup.find("ol", {"itemprop": "recipeInstructions"})
    method = recInstructions.find_all("li", {"itemprop": "itemListElement"})
    c= 0
    for i in method:
        c+=1
        method_table.append([recipe_id+1, c ,i.select("span")[0].text])

  #  with open(r'steps.csv','a', newline='')as f:
   #     for fields in method_table:
    #        writer = csv.writer(f)    # converting dataframe to csv
     #       writer.writerow(fields)
except:
    pass


howToProceed_table= []
# Get how to proceed list
try:
    recInstructions = soup.find_all("ol", {"itemprop": "recipeInstructions"})
    howToProceed = recInstructions[1].find_all("li", {"itemprop": "itemListElement"})
    c= 0
    for i in howToProceed:
        c+=1
        howToProceed_table.append([recipe_id+1, c ,i.select("span")[0].text])
        
 #   with open(r'howToProceed.csv','a', newline='')as f:
  #      for fields in howToProceed_table:
   #         writer = csv.writer(f)    # converting dataframe to csv
    #        writer.writerow(fields)
except:
    pass

#a = soup.find("span",{"class":"recipe_subheader"})
#a.text
# Get table data
nutrients_table = []
nutrition_df = []
nutrition = soup.find("table", {"id": "rcpnutrients"})
try:
    nutrition_df = pd.read_html(str(nutrition))
    print(nutrition_df)
    nutrition1_df= pd.DataFrame(nutrition_df)

    nutrition1_df[0][0].columns = ['Nutrients','Values']
    nutrition1_df[0][0]['Nutrients']
    n = len(nutrition1_df[0][0]['Nutrients'])
#nutrition1_df[0][0].iloc[0]['Nutrients']
    c = 0
    for i in range(0,n):
   # print(nutrition1_df[0][0].iloc[i]['Nutrients'])
        nutrients_table.append([recipe_id+1,nutrition1_df[0][0].iloc[i]['Nutrients'],nutrition1_df[0][0].iloc[i]['Values'].split()[0],nutrition1_df[0][0].iloc[i]['Values'].split()[1]])

   # with open(r'nutrition_values.csv','a', newline='')as f:
    #    for fields in nutrients_table:
     #       writer = csv.writer(f)    # converting dataframe to csv
      #      writer.writerow(fields)
except:
    pass
#nutrition_df.columns = ['Nutrients','Value']
#if len(nutrition_df)== 0:
    

        
#nutrition1_df[0][0].to_csv('nutrition.csv')
#print(nutrition_df)



