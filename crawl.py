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
df_group_description = pd.DataFrame(columns=['group_id', 'description'])
#person
df_person = pd.DataFrame(columns=['id', 'name' , 'description'])
#category
df_category = pd.DataFrame(columns=['id', 'name', 'description'])
#all detais
df_iraniketab = pd.DataFrame(columns=['title_persian','title_english','price','discount','grade','code','shabak',
                                'count_page','realese_year_sh','release_year_mi','exist_bolean','earliest_access',
                                'print_serie', 'publisher_name','category','ghate','cover', 'writer',
                                'translator','book_id','writer_id','translator_id','category_id','publisher_id'])

#transform date
def convert_to_jalali(date_string):
    day = int(''.join(filter(str.isdigit, date_string)))
    month = None
    if 'فروردین' in date_string:
        month = 1
    elif 'اردیبهشت' in date_string:
        month = 2
    elif 'خرداد' in date_string:
        month = 3
    elif 'تیر' in date_string:
        month = 4
    elif 'مرداد' in date_string:
        month = 5
    elif 'شهریور' in date_string:
        month = 6
    elif 'مهر' in date_string:
        month = 7
    elif 'آبان' in date_string:
        month = 8
    elif 'آذر' in date_string:
        month = 9
    elif 'دی' in date_string:
        month = 10
    elif 'بهمن' in date_string:
        month = 11
    elif 'اسفند' in date_string:
        month = 12
    else:
        raise ValueError('ماه نامعتبر است')

    jalali_date = JalaliDate(1402, month, day)
    new = jalali_date.strftime("%Y-%m-%d")
    return new
#=================================================================================================================
#Getting each page details
#getting description
def get_detail(link):
    response = requests.get(link, headers=headers, timeout=timeout)
    soup = BeautifulSoup(response.content, "html.parser")    

    def get_description(url, soup):
        global df_group_description, df_person, df_category
        # Search the blocks for all author and translator links
        def get_person_links(soup):
            blocks = soup.find_all("div", class_="clearfix")
            persons = {}

            for block in blocks:
                author_links = block.find_all("a", itemprop="author")

                for link in author_links:
                    name = link.find("span", itemprop="name").text
                    href = link["href"]
                    persons[name] = href

            return persons



        persons = get_person_links(soup)

        details_list = []

        for name, link in persons.items():
            person_response = requests.get(f"https://www.iranketab.ir{link}")
            person_soup = BeautifulSoup(person_response.content, "html.parser")

            person_id = link.split("/")[-1].split("-")[0]
            person_div = person_soup.find("div", class_="col-md-9")

            if person_div:
                person_description = person_div.find("h5").text.strip()
            else:
                person_description = None

            details_list.append(
                {"name": name, "id": person_id, "description": person_description}
            )

        df_person_book = pd.DataFrame(details_list)

        # Create dataframe for book descriptions
        book_id = url.split("/")[-1].split("-")[0]

        soup = BeautifulSoup(response.content, "html.parser")

        description_div = soup.find("div", class_="product-description")

        if description_div:
            book_description = description_div.text.strip()
        else:
            book_description = None

        df_book1 = pd.DataFrame({"group_id": book_id, "description": book_description}, index=[0])




        #getting categories
        tag_links = soup.find_all("a", class_="product-tags-item")

        details_list = []

        for link in tag_links:
            hashtag_url = f"https://www.iranketab.ir{link['href']}"

            hashtag_response = requests.get(hashtag_url)
            hashtag_soup = BeautifulSoup(hashtag_response.content, "html.parser")

            hashtag_id = link["href"].split("/")[-1].split("-")[0]

            description_div = hashtag_soup.find("div", class_="col-md-10")

            if description_div:
                description = description_div.find("h2").text.strip()
            else:
                description = None

            hashtag_text = link.text.strip()

            details_list.append(
                {"id": hashtag_id, "name": hashtag_text, "description": description}
            )

        df_hashtags = pd.DataFrame(details_list)

        #inserting data into dataframes 
        #inserting data into group_description df
        df_group_description = pd.concat([df_group_description, df_book1])
        df_group_description.drop_duplicates(inplace=True)
        #inserting data into person df
        df_person = pd.concat([df_person, df_person_book])
        df_person.drop_duplicates(inplace=True)
        #inserting data into category df
        df_category = pd.concat([df_category, df_hashtags])
        df_category.drop_duplicates(inplace=True) 

    #==========================================================================================================================================
    #getting group2 detail
    def mge_jnge(url_main, soup):
        global df_iraniketab
        main_df = pd.DataFrame(columns=['title_persian','title_english','price','discount','grade','code','shabak',
                                'count_page','realese_year_sh','release_year_mi','exist_bolean','earliest_access',
                                'print_serie', 'publisher_name','category','ghate','cover', 'writer',
                                'translator','book_id','writer_id','translator_id','category_id','publisher_id'])
        
        
        rows = soup.find_all('div',{'class':'col-md-9 col-sm-9'})
        for i in rows:
            #dataframe
            df = pd.DataFrame(columns=['title_persian','title_english','price','discount','grade','code','shabak',
                                'count_page','realese_year_sh','release_year_mi','exist_bolean','earliest_access',
                                'print_serie', 'publisher_name','category','ghate','cover', 'writer',
                                'translator','book_id','writer_id','translator_id','category_id','publisher_id'])
            
            #title_persian
            title_persian = i.select('.product-name strong')[0].text
            title_persian= title_persian.replace('کتاب ' , '')
            df.loc[0,'title_persian'] = title_persian
            
            #title_english
            title_english = i.select('.product-name-englishname')[0].text
            df.loc[0,'title_english'] = title_english
        
            #price
            price_each_row = i.select('.clearfix~ .clearfix+ .clearfix .price , .col-md-7 .price-special')[0].text
            price = int(price_each_row.replace(',',''))
            df.loc[0,'price'] = price
        
            #discount
            try:
                discount_each_row = i.select('.col-md-7 li:nth-child(1) div')[0].text
                temp_discount = re.findall(r'\d+', discount_each_row)[0]
                df.loc[0,'discount'] = temp_discount
            except:
                df.loc[0,'discount'] = np.nan
        
            #grade
            try:
                Grade_each_row = i.find_all('div', {'class':'my-rating'})
                attribute_grade = [x['data-rating'] for x in Grade_each_row if 'data-rating' in x.attrs]
                df.loc[0,'grade'] = float(attribute_grade[0])
            except:
                df.loc[0,'grade'] = np.nan

            #realese_year_sh
            try:
                realese_year_sh_each_row = i.select('tr:nth-child(6) .rtl')[0].text
                realese_year_sh_each_row = realese_year_sh_each_row.replace('\r\n','')
                realese_year_sh_each_row = realese_year_sh_each_row.replace(' ','')
                df.loc[0,'realese_year_sh'] = int(realese_year_sh_each_row)
            except:
                df.loc[0,'realese_year_sh'] = np.nan
            #exist_bolean
            try:
                exist_bolean_each_row = i.select('.icon-exit , .exists-book span')[0].text
                exist_bolean_each_row = exist_bolean_each_row.replace(' ','')
                if exist_bolean_each_row == 'موجود':
                    df.loc[0,'exist_bolean'] = (True)
                else:
                    df.loc[0,'exist_bolean'] = (False)
            except:
                df.loc[0,'exist_bolean'] = np.nan
            #publisher_name
            try:
                publisher_name_each_row = i.select('.prodoct-attribute-items:nth-child(1) a .prodoct-attribute-item')[0].text
                df.loc[0,'publisher_name'] = publisher_name_each_row
            except:
                df.loc[0,'publisher_name'] = np.nan
            #category
            try:
                category_each_row = soup.select('.product-tags-item')
                category = [name.text for name in category_each_row]
                df.loc[0,'category'] = category
            except:
                df.loc[0,'category'] = np.nan
            #writer
            try:
                writer_each_row = i.select('.prodoct-attribute-items+ .prodoct-attribute-items a .prodoct-attribute-item')
                writer_each_row = [name.text for name in writer_each_row]
                df.loc[0,'writer'] = writer_each_row
            except:
                df.loc[0,'writer'] = np.nan
            #translator 
            try:
                translator_each_row = i.select('.product-table .prodoct-attribute-item')
                translator_each_row = [name.text for name in translator_each_row]
                df.loc[0,'translator'] = translator_each_row
            except:
                df.loc[0,'translator'] = np.nan
                
            #book_id
            match_book_id= re.search(r'(\d+)', url_main)
            number_book_id = int(match_book_id.group(1))
            df.loc[0,'book_id'] = number_book_id
            
            #writer_id
            try:
                w_id = []
                writer_each_row = i.select('.prodoct-attribute-items+ .prodoct-attribute-items a')
                writer_each_row = [name.get('href') for name in writer_each_row]
                for sublist in writer_each_row:
                    match_writer_id = re.search(r'(\d+)', sublist)
                    number_writer_id = int(match_writer_id.group(1))
                    w_id.append(number_writer_id)
                df.loc[0,'writer_id'] = w_id
            except:
                df.loc[0,'writer_id'] = np.nan
            #translator_id
            try:
                tr_id = []
                translator_id_each_rows = i.select('tr:nth-child(2) td+ td a')
                translator_id_each_row = [name.get('href') for name in translator_id_each_rows]
                for sublist in translator_id_each_row:
                    match_translator_id = re.search(r'(\d+)', sublist)
                    number_translator_id= int(match_translator_id.group(1))
                    tr_id.append(number_translator_id)
                df.loc[0,'translator_id'] = tr_id
            except:
                df.loc[0,'translator_id'] = np.nan
                
            #category_id
            try:
                category_id_each_row = soup.select('.product-tags-item')
                category_id = [name.get('href') for name in category_id_each_row]
                category_ids = [re.findall(r'[0-9]+', name)[0] for name in category_id]
                df.loc[0,'category_id'] = category_ids
            except:
                df.loc[0,'category_id'] = np.nan
                
            #publisher_id
            try:
                pub_id = []
                publisher_id_each_rows = i.select('.prodoct-attribute-items:nth-child(1) a')
                publisher_id_each_row = [name.get('href') for name in publisher_id_each_rows]
                for sublist in publisher_id_each_row:
                    match_publisher_id = re.search(r'(\d+)', sublist)
                    number_publisher_id = int(match_publisher_id.group(1))
                    pub_id.append(number_publisher_id)
                df.loc[0,'publisher_id'] = pub_id
            except:
                df.loc[0,'publisher_id'] = np.nan
                
            #table
            for j in i.select('.row .col-md-5 tr'):
                j = str(j.text)
                
                #code
                if 'کد کتاب' in j:
                    temp_code = int(re.findall(r'\d+', j)[0])
                    df.loc[0,'code'] = temp_code
                    
                #shabak
                elif 'شابک' in j:
                    temp_shabak = j.replace('شابک', '')
                    temp_shabak = temp_shabak.replace(':', '')
                    temp_shabak = temp_shabak.replace(' ', '')
                    temp_shabak = temp_shabak.replace('\n', '')
                    temp_shabak = temp_shabak.replace('\r', '')
                    df.loc[0,'shabak'] = temp_shabak
                    
                #ghate
                elif 'قطع' in j:
                    temp_ghate = j.replace('قطع', '')
                    temp_ghate = temp_ghate.replace(':', '')
                    temp_ghate = temp_ghate.replace(' ', '')
                    temp_ghate = temp_ghate.replace('\n', '')
                    temp_ghate = temp_ghate.replace('\r', '')
                    df.loc[0,'ghate'] = temp_ghate
                    
                #counter
                elif 'تعداد صفحه' in j:
                    temp_count = int(re.findall(r'\d+', j)[0])
                    df.loc[0,'count_page'] =int(temp_count)
                    
                #shamsi
                elif 'سال انتشار شمسی' in j:
                    temp_shamsi = int(re.findall(r'\d+', j)[0])
                    df.loc[0,'realese_year_sh'] = int(temp_shamsi)
                    
                #miladi
                elif 'سال انتشار میلادی' in j:
                    temp_miladi = int(re.findall(r'\d+', j)[0])
                    df.loc[0,'release_year_mi'] = int(temp_miladi)
                    
                #cover
                elif 'نوع جلد' in j:
                    temp_cover = j.replace('نوع جلد', '')
                    temp_cover = temp_cover.replace(':', '')
                    temp_cover = temp_cover.replace(' ', '')
                    temp_cover = temp_cover.replace('\n', '')
                    temp_cover = temp_cover.replace('\r', '')
                    df.loc[0,'cover'] = temp_cover
                    
                #serie
                elif 'سری چاپ' in j:
                    temp_serie = int(re.findall(r'\d+', j)[0])
                    df.loc[0,'print_serie'] = int(temp_serie)
                    
                #earliest
                elif 'زودترین زمان ارسال' in j:
                    temp_earliest = j.replace('زودترین زمان ارسال', '')
                    temp_earliest  = temp_earliest .replace(':', '')
                    temp_earliest  = temp_earliest .replace(' ', '')
                    temp_earliest  = temp_earliest .replace('\n', '')
                    temp_earliest  = temp_earliest .replace('\r', '')
                    try:
                        earliest_access_date = convert_to_jalali(temp_earliest)
                        df.loc[0,'earliest_access'] = earliest_access_date
                    except:
                        df.loc[0,'earliest_access'] = np.nan
            main_df = pd.concat([main_df,df], axis=0)

        df_iraniketab = pd.concat([df_iraniketab, main_df])



    #run functions
    # get_description(link, soup)
    mge_jnge(link, soup)

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
#inserting into dataframes
#book
df_book = df_iraniketab[['title_persian','title_english','price','discount','grade','code','shabak',
                                'count_page','realese_year_sh','release_year_mi','exist_bolean','earliest_access',
                                'print_serie', 'ghate', 'cover']]
df_book.drop_duplicates(inplace=True)

#group




#=======================================================================================
#make csv
df_group_description.to_csv('group_description.csv', index=False, encoding='utf-8-sig')
df_person.to_csv('person.csv', index=False, encoding='utf-8-sig')
df_category.to_csv('category.csv', index=False, encoding='utf-8-sig')
df_iraniketab.to_csv('iraniketab.csv', index=False, encoding='utf-8-sig')


print("Done!")
