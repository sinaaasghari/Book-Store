import crawl_functions as cf
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from time import sleep
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
import csv
from time import sleep
import math


#read urls from csv
csv_file = 'book_url.csv'
with open(csv_file, 'r') as file:
    csv_reader = csv.reader(file)
    links = list()
    for row in csv_reader:
        links.append(row[0])

links = list(set(links[1:]))

#header of each request
headers = {"Accept-Language": "en-US,en;q=0.5"}

#==============================================================================================================
#creating lists and dataframes

#group
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
#person
df_person = pd.DataFrame(columns=['id', 'name'])
#crew
df_crew = pd.DataFrame(columns=['book_code', 'name', 'role'])

#group_category
df_group_category = pd.DataFrame(columns=['group_id', 'category_id'])

#publisher_df
df_publisher = pd.DataFrame(columns=['id', 'name'])

#book_publisher
df_book_publisher = pd.DataFrame(columns=['publisher_id'])

person_urls_list = list()
category_urls_list = list()
#=================================================================================================================
#Getting each page details
#getting description
i = 1
def get_detail(link):
    global df_iraniketab, df_group, df_category, df_person_description, person_urls_list, category_urls_list, i, df_person, df_group_category, df_crew, df_publisher, df_book_publisher
    print(i)
    response = requests.get(link, headers=headers, timeout=timeout)
    soup = BeautifulSoup(response.content, "html.parser")    
    if response.status_code  == 200:
        #run functions
        df_hashtags, df_book1, df_person_book, book_person_urls_list, book_category_urls_list = cf.get_description(link, soup, person_urls_list, category_urls_list)
        person_urls_list.append(book_person_urls_list)
        category_urls_list.append(book_category_urls_list)
        #inserting data into dataframes 
        #inserting data into group df
        df_group = pd.concat([df_group, df_book1])
        df_group.drop_duplicates(inplace=True)
        #inserting data into person df
        df_person_description = pd.concat([df_person_description, df_person_book])
        df_person_description.drop_duplicates(inplace=True)
        #inserting data into category df
        df_category = pd.concat([df_category, df_hashtags])
        df_category.drop_duplicates(inplace=True) 
        main_df = cf.mge_jnge(link, soup)
        main_df.dropna(subset='code', inplace=True)
        df_iraniketab = pd.concat([df_iraniketab, main_df])
        main_df.reset_index(drop=True, inplace=True)
        main_df.to_csv('main.csv', index=False, encoding='utf-8-sig')
        #=======================================================================================
        #lists
        publisher_name_list = list()
        publisher_id_list =list()
        category_list = list()
        category_id_list = list()
        person_name_list = list()
        person_id_list = list()

        print("++++++++")
        print(link)

        for index in range(len(main_df.index)):
            if type(main_df.loc[index, 'code']) == int:
                book_code = main_df.loc[index, 'code']
            else:
                book_code = main_df.loc[index, 'code'].values.tolist()[0]
            


            if type(main_df.loc[index, 'publisher_name']) == str:
                publisher_name_list.append(main_df.loc[index, 'publisher_name'])
            else:
                publisher_name_list.append(main_df.loc[index, 'publisher_name']).values.tolist()[0]
            if type(main_df.loc[index, 'publisher_id'][0]) == int:
                p_id = main_df.loc[index, 'publisher_id'][0]
            else:
                p_id = main_df.loc[index, 'publisher_id'][0].values.tolist()[0]
            if type(p_id) != int:
                p_id = p_id[0]
            publisher_id_list.append(p_id)
            new_dict = {'publisher_id': p_id, 'book_code': book_code}
            df_book_publisher = df_book_publisher._append(new_dict, ignore_index=True)
            try:
                for category in main_df.loc[index, 'category']:
                    category_list.append(category)
                for category_id in main_df.loc[index, 'category_id']:
                    new_dict = {'group_id': main_df.loc[index, 'book_id'],
                                'category_id': category_id}
                    df_group_category = df_group_category._append(new_dict, ignore_index=True)
                    category_id_list.append(category_id) 
            except: continue

            
            for writer_name in main_df.loc[index, 'writer']:
                if type(main_df.loc[index, 'code']) == int:
                    book_code = main_df.loc[index, 'code']
                else:
                    book_code = main_df.loc[index, 'code'].values.tolist()[0]
                try:
                    if len(writer_name[0]) == 1:
                        new_dict = {'book_code': book_code,
                                    'name': writer_name,
                                    'role': 'writer'}
                        df_crew = df_crew._append(new_dict, ignore_index=True)
                        person_name_list.append(writer_name)
                    else:
                        new_dict = {'book_code': book_code,
                                    'name': writer_name[0],
                                    'role': 'writer'}
                        df_crew = df_crew._append(new_dict, ignore_index=True)
                        person_name_list.append(writer_name[0])
                except: 
                    person_name_list.append(writer_name)

            for writer_id in main_df.loc[index, 'writer_id']:
                try:
                    person_id_list.append(writer_id[0])
                except:
                    person_id_list.append(writer_id)
        

        
            for translator_name in main_df.loc[index, 'translator']:
                if type(main_df.loc[index, 'code']) == int:
                    book_code = main_df.loc[index, 'code']
                else: 
                    book_code = main_df.loc[index, 'code'].values.tolist()[0]
                try:
                    if len(translator_name[0]) == 1:
                        new_dict = {'book_code':book_code,
                                    'name': translator_name,
                                    'role': 'translator'}
                        df_crew = df_crew._append(new_dict, ignore_index=True)
                        person_name_list.append(translator_name)
                    else:
                        new_dict = {'book_code': book_code,
                                    'name': translator_name[0],
                                    'role': 'translator'}
                        df_crew = df_crew._append(new_dict, ignore_index=True)
                        person_name_list.append(translator_name[0])
                except: 
                    person_name_list.append(translator_name)
            for translator_id in main_df.loc[index, 'translator_id']:
                try:
                    person_id_list.append(translator_id[0])
                except:
                    person_id_list.append(translator_id)
        # crew
        df_crew.drop_duplicates(inplace=True)
        try:
            # publisher
            pub_df = pd.DataFrame({'id': publisher_id_list, 'name': publisher_name_list})
            df_publisher = pd.concat([df_publisher, pub_df])
            df_publisher.drop_duplicates(inplace=True)
        except: pass
        try:
            #person
            p_df = pd.DataFrame({'id': person_id_list, 'name': person_name_list})
            df_person = pd.concat([df_person, p_df])
            df_person.drop_duplicates(subset=['name'], inplace=True)
        except: pass
        i += 1
    return {'response': response, 'link': link}



#========================================================================================
#request manager
count_of_request = 1000
#requests in each pulse
workers = 10
sleep_time = 2
timeout = 90
max_count = math.ceil((len(links)*1.2) / count_of_request)

bad_links = list()
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
                print(future)
                continue

    for result in out:
        if result['response'].status_code == 200:
            url = result['link']
            if url in links:
                links.remove(url)
        else:
            url = result['link']
            if url in links:
                bad_links.append(url)

    print(count)
    count += 1

# for link in links:
#     get_detail(link)


df_bad_links = pd.DataFrame({'link': bad_links})
#------------------------------------------------------------------------------------------------------------
print("crawl done!")
#inserting into dataframes
#book
df_iraniketab.rename(columns={'exist_bolean': 'exist', 'count_page': 'page_count', 'print_serie': 'print_series', 'realese_year_sh': 'release_year_sh'}, inplace=True)
df_iraniketab.reset_index(drop=True, inplace=True)

df_iraniketab.to_csv('iraniketab.csv', index=False, encoding='utf-8-sig')

#group
df_group_book = pd.DataFrame({'group_id': df_iraniketab['book_id'].values.tolist(),
                              'book_code': df_iraniketab['code'].values.tolist()})


df_book = df_iraniketab[['code', 'title_persian','title_english','price','discount','grade', 'shabak',
                                'page_count','release_year_sh','release_year_mi','exist','earliest_access',
                                'print_series', 'ghate', 'cover']]
df_book.drop_duplicates(inplace=True)


#person_df
df_person_description['id'] = df_person_description['id'].astype('float64')
df_person['id'] = df_person['id'].astype('float64')
df_person = pd.merge(df_person, df_person_description[['id', 'description']], how='left', on='id')
df_person['counter'] = np.arange(1, 1 + len(df_person['name'].values.tolist()))
df_crew.reset_index(drop=True, inplace=True)
for index in df_crew.index.values.tolist():
    name = df_crew.loc[index, 'name']
    try:
        df_crew.loc[index, 'name'] = df_person.loc[df_person.loc[df_person['name'] == name].index.values.tolist()[0], 'counter']
    except:
        try:
            df_crew.loc[index, 'name'] = df_person.loc[df_person.loc[df_person['name'] == name[0]].index.values.tolist()[0], 'counter']
        except:
            df_crew.drop([index], axis=0, inplace=True)
df_crew.rename(columns={'name': 'person_counter'}, inplace=True)




#=======================================================================================
#make csv
df_group.to_csv('group.csv', index=False, encoding='utf-8-sig')
df_person_description.to_csv('person_description.csv', index=False, encoding='utf-8-sig')
df_category.to_csv('category.csv', index=False, encoding='utf-8-sig')
df_iraniketab.to_csv('iraniketab2.csv', index=False, encoding='utf-8-sig')
df_book.to_csv('book.csv', index=False, encoding='utf-8-sig')
df_group_book.to_csv('group_book.csv', index=False, encoding='utf-8-sig')
df_person.to_csv('person.csv', index=False, encoding='utf-8-sig')
df_crew.to_csv('crew.csv', index=False, encoding='utf-8-sig')
df_publisher.to_csv('publisher.csv', index=False, encoding='utf-8-sig')
df_group_category.to_csv('group_category.csv', index=False, encoding='utf-8-sig')
df_book_publisher.to_csv('book_publisher.csv', index=False, encoding='utf-8-sig')
df_bad_links.to_csv('bad_links.csv', index=False, encoding='utf-8-sig')

print("Done!")
