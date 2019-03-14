# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 08:58:44 2019

@author: Rajesh
"""

import urllib.request
from bs4 import BeautifulSoup
import csv
import pandas as pd

recipe = "https://www.tarladalal.com/RecipeAtoZ.aspx?pageindex=8"
page1 = urllib.request.urlopen(recipe)
soup = BeautifulSoup(page1,features="lxml")

links = soup.find_all('span', {"class": "rcc_recipename"})

for link in links:
    print('https://www.tarladalal.com/' + link.find('a').get('href')) 
    r = 'https://www.tarladalal.com/' + link.find('a').get('href')
    page1 = urllib.request.urlopen(r)
    soup = BeautifulSoup(page1,features="lxml")
    recipe_id = 1
#print(soup.prettify())


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
        print("Prep time is", prep_time.text)
    except:
        pass
    
    try:
        cooking_time = soup.find("time", {"itemprop": "cookTime"})
        print("Cooking time is", cooking_time.text)
    except:
        pass
    
    try:
        total_time =  soup.find("time", {"itemprop": "totalTime"})
        print("total time is", total_time.text)
    except:
        pass
    

    try:
        csv_file = csv.reader(open('recipes.csv', "r"), delimiter=",")
        recipe_id = len(list(csv_file)) - 1    
    except:
        recipe_id += 1
        pass
    
    try:
        fields = [recipe_id+1, recipe_name.text, desc.text,prep_time.text,cooking_time.text,total_time.text] 
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
            if(ing_name==row[1]):  # checking the ingrident name with the name already present 
                qty_table.append([recipe_id+1, row[0], i.select("span")[0].text])
                flag = 1
                
                #print(ing_name, " status = ", flag, "count = ", count)
        if(not flag):
            fields = [count, ing_name]
            qty_table.append([recipe_id+1, count, i.select("span")[0].text])
            with open(r'ingredients.csv','a', newline='')as f:
                writer = csv.writer(f)
                writer.writerow(fields)  # converting dataframe to csv
                        
    print(qty_table)
    with open(r'ingredient_quantities.csv','a', newline='')as f:
        for fields in qty_table:
            writer = csv.writer(f)
            writer.writerow(fields)
                                
    method_table = []
# Get recepie instructions list
    try:
        recInstructions = soup.find("ol", {"itemprop": "recipeInstructions"})
        method = recInstructions.find_all("li", {"itemprop": "itemListElement"})
        c= 0
        for i in method:
            c+=1
            method_table.append([recipe_id+1, c ,i.select("span")[0].text])

        with open(r'steps.csv','a', newline='')as f:
            for fields in method_table:
                writer = csv.writer(f)    # converting dataframe to csv
                writer.writerow(fields)
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
            
        with open(r'howToProceed_table.csv','a', newline='')as f:
            for fields in howToProceed_table:
                writer = csv.writer(f)    # converting dataframe to csv
                writer.writerow(fields)
    except:
        pass


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
            nutrients_table.append([recipe_id+1,nutrition1_df[0][0].iloc[i]['Nutrients'],nutrition1_df[0][0].iloc[i]['Values']])
            
        with open(r'nutrition_values.csv','a', newline='')as f:
            for fields in nutrients_table:
                writer = csv.writer(f)    # converting dataframe to csv
                writer.writerow(fields)
    except:
        pass
#recipe = "https://www.tarladalal.com/Achar-Dip-Achari-Dip-22718r" #reading the url of the recipe



