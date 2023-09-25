import crawl_functions as cf
import requests
from bs4 import BeautifulSoup
import json
import re
import pandas as pd
import numpy as np
from time import sleep
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
import urllib.parse
import csv
from time import sleep
import math
from persiantools.jdatetime import JalaliDate


#read urls from csv
csv_file = 'book_url.csv'
with open(csv_file, 'r') as file:
    csv_reader = csv.reader(file)
    links = list()
    for row in csv_reader:
        links.append(row[0])

links = list(set(links[1:5]))

#header of each request
headers = {"Accept-Language": "en-US,en;q=0.5",
           "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}

#==============================================================================================================
#creating lists and dataframes

#group-description
df_group = pd.DataFrame(columns=['group_id', 'description'])
#person_description
df_person_description = pd.DataFrame(columns=['id', 'name' , 'description'])
#category_description
df_category = pd.DataFrame(columns=['id', 'name', 'description'])
#all detais
df_iraniketab = pd.DataFrame(columns=['title_persian','title_english','price','discount','grade','code','shabak',
                                'count_page','realese_year_sh','release_year_mi','exist_bolean','earliest_access',
                                'print_serie', 'publisher_name','category','ghate','cover', 'writer',
                                'translator','book_id','writer_id','translator_id','category_id','publisher_id'])


#=================================================================================================================
#Getting each page details
#getting description
def get_detail(link):
    global df_iraniketab, df_group, df_category, df_person_description
    response = requests.get(link, headers=headers, timeout=timeout)
    soup = BeautifulSoup(response.content, "html.parser")    


    #run functions
    # df_hashtags, df_book1, df_person_book = cf.get_description(link, soup)
    # #inserting data into dataframes 
    # #inserting data into group_description df
    # df_group = pd.concat([df_group_description, df_book1])
    # df_group.drop_duplicates(inplace=True)
    # #inserting data into person df
    # df_person_description = pd.concat([df_person_description, df_person_book])
    # df_person_description.drop_duplicates(inplace=True)
    # #inserting data into category df
    # df_category = pd.concat([df_category, df_hashtags])
    # df_category.drop_duplicates(inplace=True) 

    main_df = cf.mge_jnge(link, soup)
    df_iraniketab = pd.concat([df_iraniketab, main_df])
    return response



#========================================================================================
#request manager
count_of_request = 1000
#requests in each pulse
workers = 100
sleep_time = 1
timeout = 30
max_count = math.ceil((len(links)*1.5) / count_of_request)

count = 0
out = list()
while (len(links)) and (count < max_count):
    sleep(sleep_time)
    if len(links) > count_of_request:
        req_list = links[:count_of_request].copy()
    else:
        req_list = links.copy()

    with ThreadPoolExecutor(max_workers=workers) as executer:
        future_to_url = (executer.submit(get_detail, link) for link in req_list)
        for future in as_completed(future_to_url):
            try:
                data = future.result()
                out.append(data)
            except Exception as exc:
                continue

    for result in out:
        if result.status_code == 200:
            url = result.url.lower()
            if url in links:
                links.remove(url)
    count += 1



#=======================================================================================
#lists
title_persian_list = list()
title_english_list = list()
price_list = list()
discount_list = list()
grade_list = list()
shabak_list = list()
page_count_list = list()
release_year_sh_list = list()
release_year_mi_list = list()
exist_list = list()
earliest_access_list = list()
print_series_list = list()
publisher_name_list = list()
publisher_id_list =list()
category_list = list()
category_id_list = list()
ghate_list = list()
cover_list = list()
group_id_list = list()
person_name_list = list()
person_id_list = list()
group_id_list = list()
book_code_list = list()
#------------------------------------------------------------------------------------------------------------
#inserting into dataframes
#book
df_iraniketab.rename(columns={'exist_bolean': 'exist', 'count_page': 'page_count', 'print_serie': 'print_series', 'realese_year_sh': 'release_year_sh'}, inplace=True)
df_iraniketab.reset_index(drop=False, inplace=True)
df_book = df_iraniketab[['code', 'title_persian','title_english','price','discount','grade','code','shabak',
                                'page_count','release_year_sh','release_year_mi','exist','earliest_access',
                                'print_series', 'ghate', 'cover']]
df_book.drop_duplicates(inplace=True)


df_crew = pd.DataFrame(columns=['book_code', 'person_id', 'role'])
df_group_book = pd.DataFrame({'group_id': df_iraniketab['book_id'].values.tolist(),
                              'book_code': df_iraniketab['code'].values.tolist()})


#group_category
df_group_category = pd.DataFrame(columns=['group_id', 'category_id'])

for index in range(len(df_iraniketab.index)):
    publisher_name_list.append(df_iraniketab.loc[index, 'publisher_name'])
    publisher_id_list.append(df_iraniketab.loc[index, 'publisher_id'][0])
    for category in df_iraniketab.loc[index, 'category']:
        category_list.append(category)
    for category_id in df_iraniketab.loc[index, 'category_id']:
        new_dict = {'group_id': df_iraniketab.loc[index, 'book_id'],
                    'category_id': category_id}
        category_id_list.append(category_id) 

    #person
    for writer in df_iraniketab.loc[index, 'writer']:
        person_name_list.append(writer)

    for writer_id in df_iraniketab.loc[index, 'writer_id']:
        person_id_list.append(writer_id)
    
    for translator in df_iraniketab.loc[index, 'translator']:
        person_name_list.append(translator)

    for translator_id in df_iraniketab.loc[index, 'translator_id']:
        person_id_list.append(translator_id)

print(len(person_id_list), len(person_name_list))
#publisher_df
df_publisher = pd.DataFrame({'id': publisher_id_list, 'name': publisher_name_list})

#person_df
df_person = pd.DataFrame({'person_id': person_id_list, 'name': person_name_list})
df_person = pd.merge(df_person, df_person_description, how='left', on='id')
df_person.drop_duplicates(inplace=True)
df_person['counter'] = np.arange(0, len(df_person['name'].values.tolist()))


#crew 
df_crew = pd.DataFrame(columns=['book_code', 'person_counter', 'role'])
for index in range(len(df_iraniketab.index)):
    for writer_name in df_iraniketab.loc[index, 'writer']:
        new_dict = {'book_code': df_iraniketab.loc[index, 'code'],
                    'person_counter': df_person.loc[df_person['name'] == writer_name]['name'].values.tolist()[0],
                    'role': 'writer'}
        df_crew = df_crew._append(new_dict, ignore_index=True)
    for translator_name in df_iraniketab.loc[index, 'translator']:
        new_dict = {'book_code': df_iraniketab.loc[index, 'code'],
                    'person_counter': df_person.loc[df_person['name'] == translator_name]['name'].values.tolist()[0],
                    'role': 'translator'}
        df_crew = df_crew._append(new_dict, ignore_index=True)
df_crew.drop_duplicates(inplace=True)


#=======================================================================================
#make csv
# df_group.to_csv('group_description.csv', index=False, encoding='utf-8-sig')
# df_person_description.to_csv('person.csv', index=False, encoding='utf-8-sig')
# df_category.to_csv('category.csv', index=False, encoding='utf-8-sig')
df_iraniketab.to_csv('iraniketab.csv', index=False, encoding='utf-8-sig')
#df_book.to_csv('book.csv', index=False, encoding='utf-8-sig')
# df_group_book.to_csv('group_book.csv', index=False, encoding='utf-8-sig')
df_person.to_csv('person.csv', index=False, encoding='utf-8-sig')
df_crew.to_csv('crew.csv', index=False, encoding='utf-8-sig')
df_publisher.to_csv('publisher.csv', index=False, encoding='utf-8-sig')
df_group_category.to_csv('group_category.csv', index=False, encoding='utf-8-sig')

print("Done!")
