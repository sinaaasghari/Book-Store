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



def mge_jnge(url_main, soup):
    main_df = pd.DataFrame(
        columns=['title_persian', 'title_english', 'price', 'discount', 'grade', 'code', 'shabak',
                 'count_page', 'realese_year_sh', 'release_year_mi', 'exist_bolean', 'earliest_access',
                 'print_serie', 'publisher_name', 'category', 'ghate', 'cover', 'writer',
                 'translator', 'book_id', 'writer_id', 'translator_id', 'category_id', 'publisher_id'])
    rows = soup.find_all('div', {'class': 'col-md-9 col-sm-9'})
    for i in rows:
        # dataframe
        df = pd.DataFrame(columns=['title_persian', 'title_english', 'price', 'discount', 'grade', 'code', 'shabak',
                                   'count_page', 'realese_year_sh', 'release_year_mi', 'exist_bolean',
                                   'earliest_access',
                                   'print_serie', 'publisher_name', 'category', 'ghate', 'cover', 'writer',
                                   'translator', 'book_id', 'writer_id', 'translator_id', 'category_id',
                                   'publisher_id'])

        # title_persian
        try:
            title_persian = i.select('.product-name strong')[0].text
            title_persian = title_persian.replace('کتاب ', '')
            df.loc[0, 'title_persian'] = title_persian
        except:
            df.loc[0, 'title_persian'] = np.nan

        # title_english
        try:
            title_english = i.select('.product-name-englishname')[0].text
            df.loc[0, 'title_english'] = title_english
        except:
            df.loc[0, 'title_english'] = np.nan

        # price
        try:
            price_each_row = i.find_all('span', attrs={'class': 'price'})[0].text
            price = int(price_each_row.replace(',', ''))
            df.loc[0, 'price'] = price
        except:
            df.loc[0, 'price'] = np.nan
        # discount
        try:
            discount_each_row = i.select('.col-md-7 li:nth-child(1) div')[0].text
            temp_discount = re.findall(r'\d+', discount_each_row)[0]
            df.loc[0, 'discount'] = temp_discount
        except:
            df.loc[0, 'discount'] = np.nan

        # grade
        try:
            Grade_each_row = i.find_all('div', {'class': 'my-rating'})
            attribute_grade = [x['data-rating'] for x in Grade_each_row if 'data-rating' in x.attrs]
            df.loc[0, 'grade'] = float(attribute_grade[0])
        except:
            df.loc[0, 'grade'] = np.nan

        # realese_year_sh
        try:
            realese_year_sh_each_row = i.select('tr:nth-child(6) .rtl')[0].text
            realese_year_sh_each_row = realese_year_sh_each_row.replace('\r\n', '')
            realese_year_sh_each_row = realese_year_sh_each_row.replace(' ', '')
            df.loc[0, 'realese_year_sh'] = int(realese_year_sh_each_row)
        except:
            df.loc[0, 'realese_year_sh'] = np.nan
        # exist_bolean
        try:
            exist_bolean_each_row = i.select('.icon-exit , .exists-book span')[0].text
            exist_bolean_each_row = exist_bolean_each_row.replace(' ', '')
            if exist_bolean_each_row == 'موجود':
                df.loc[0, 'exist_bolean'] = (True)
            else:
                df.loc[0, 'exist_bolean'] = (False)
        except:
            df.loc[0, 'exist_bolean'] = np.nan
        # publisher_name
        try:
            publisher_name_each_row = i.select('.prodoct-attribute-items:nth-child(1) a .prodoct-attribute-item')[
                0].text
            df.loc[0, 'publisher_name'] = publisher_name_each_row
        except:
            df.loc[0, 'publisher_name'] = np.nan
        # category
        try:
            category_each_row = soup.select('.product-tags-item')
            category = [name.text for name in category_each_row]
            df.loc[0, 'category'] = category
        except:
            df.loc[0, 'category'] = np.nan

        # writer
        ws = []
        try:
            for w_id in i.find_all('div', attrs={"class": "row clearfix"}):
                span_tags_w_id = w_id.find_all('span', attrs={"itemprop": "name"})
                ws = [name.text for name in span_tags_w_id]
                if len(ws) == 0:
                    df.at[0, 'writer'] = [np.nan]
                else:
                    df.at[0, 'writer'] = ws
        except:
            df.at[0, 'writer'] = [np.nan]

        # translator
        try:
            translator_each_row = i.select('.product-table .prodoct-attribute-item')
            translator_each_row = [name.text for name in translator_each_row]
            if len(translator_each_row) == 0:
                df.at[0, 'translator'] = [np.nan]
            else:
                df.at[0, 'translator'] = translator_each_row
        except:
            df.at[0, 'translator'] = [np.nan]

        # book_id
        match_book_id = re.search(r'(\d+)', url_main)
        number_book_id = int(match_book_id.group(1))
        df.loc[0, 'book_id'] = number_book_id

        # writer_id
        w_ids = []
        try:
            for w_id in i.find_all('div', attrs={"class": "row clearfix"}):
                span_tags_w_id = w_id.find_all('span', attrs={"itemprop": "name"})
                for tag in span_tags_w_id:
                    if tag.find_parent('a'):
                        up = tag.find_parent('a')
                        match_writer_id = re.search(r'(\d+)', up.get('href'))
                        number_writer_ids = int(match_writer_id.group(1))
                        w_ids.append(number_writer_ids)
                    else:
                        w_ids.append(np.nan)

                if len(w_ids) == 0:
                    df.loc[0, 'writer_id'] = [np.nan]
                else:
                    df.at[0, 'writer_id'] = w_ids

        except:
            df.loc[0, 'writer_id'] = [np.nan]

        # translator_id
        for j in i.select('tr:nth-child(2) td+ td'):
            tr_id = []
            span_tags = j.find_all('span')
            for tag in span_tags:
                up = tag.parent
                if up.name == 'a':
                    match_translator_id = re.search(r'(\d+)', up.get('href'))
                    number_translator_id = int(match_translator_id.group(1))
                    tr_id.append(number_translator_id)
                else:
                    tr_id.append(np.nan)
        if len(tr_id) == 0:
            df.at[0, 'translator_id'] = [np.nan]
        else:
            df.at[0, 'translator_id'] = tr_id

        # category_id
        try:
            category_id_each_row = soup.select('.product-tags-item')
            category_id = [name.get('href') for name in category_id_each_row]
            category_ids = [re.findall(r'[0-9]+', name)[0] for name in category_id]
            df.loc[0, 'category_id'] = category_ids
        except:
            df.loc[0, 'category_id'] = np.nan

        # publisher_id
        try:
            pub_id = []
            publisher_id_each_rows = i.select('.prodoct-attribute-items:nth-child(1) a')
            publisher_id_each_row = [name.get('href') for name in publisher_id_each_rows]
            for sublist in publisher_id_each_row:
                match_publisher_id = re.search(r'(\d+)', sublist)
                number_publisher_id = int(match_publisher_id.group(1))
                pub_id.append(number_publisher_id)
            df.loc[0, 'publisher_id'] = pub_id
        except:
            df.loc[0, 'publisher_id'] = np.nan

        # table
        for j in i.select('.row .col-md-5 tr'):
            j = str(j.text)

            # code
            if 'کد کتاب' in j:
                temp_code = int(re.findall(r'\d+', j)[0])
                df.loc[0, 'code'] = temp_code

            # shabak
            elif 'شابک' in j:
                temp_shabak = j.replace('شابک', '')
                temp_shabak = temp_shabak.replace(':', '')
                temp_shabak = temp_shabak.replace(' ', '')
                temp_shabak = temp_shabak.replace('\n', '')
                temp_shabak = temp_shabak.replace('\r', '')
                df.loc[0, 'shabak'] = temp_shabak

            # ghate
            elif 'قطع' in j:
                temp_ghate = j.replace('قطع', '')
                temp_ghate = temp_ghate.replace(':', '')
                temp_ghate = temp_ghate.replace(' ', '')
                temp_ghate = temp_ghate.replace('\n', '')
                temp_ghate = temp_ghate.replace('\r', '')
                df.loc[0, 'ghate'] = temp_ghate

            # counter
            elif 'تعداد صفحه' in j:
                temp_count = int(re.findall(r'\d+', j)[0])
                df.loc[0, 'count_page'] = int(temp_count)

            # shamsi
            elif 'سال انتشار شمسی' in j:
                temp_shamsi = int(re.findall(r'\d+', j)[0])
                df.loc[0, 'realese_year_sh'] = int(temp_shamsi)

            # miladi
            elif 'سال انتشار میلادی' in j:
                temp_miladi = int(re.findall(r'\d+', j)[0])
                df.loc[0, 'release_year_mi'] = int(temp_miladi)

            # cover
            elif 'نوع جلد' in j:
                temp_cover = j.replace('نوع جلد', '')
                temp_cover = temp_cover.replace(':', '')
                temp_cover = temp_cover.replace(' ', '')
                temp_cover = temp_cover.replace('\n', '')
                temp_cover = temp_cover.replace('\r', '')
                df.loc[0, 'cover'] = temp_cover

            # serie
            elif 'سری چاپ' in j:
                temp_serie = int(re.findall(r'\d+', j)[0])
                df.loc[0, 'print_serie'] = int(temp_serie)

            # earliest
            elif 'زودترین زمان ارسال' in j:
                temp_earliest = j.replace('زودترین زمان ارسال', '')
                temp_earliest = temp_earliest.replace(':', '')
                temp_earliest = temp_earliest.replace(' ', '')
                temp_earliest = temp_earliest.replace('\n', '')
                temp_earliest = temp_earliest.replace('\r', '')
                try:
                    earliest_access_date = convert_to_jalali(temp_earliest)
                    df.loc[0, 'earliest_access'] = earliest_access_date
                except:
                    df.loc[0, 'earliest_access'] = np.nan
        main_df = pd.concat([main_df, df], axis=0)

    return main_df


#=====================================================================================================================================
def get_description(url, soup, linkp_list, hashtag_urls_list):
    # Search the blocks for all author and translator links
    def get_person_links(soup):
        if soup is None:
            return 0

        containers = soup.find_all("div", class_="product-container well clearfix")
        if not containers or len(containers) == 0:
            return 0

        container = containers[0]

        persons = {}

        blocks = container.find_all(
            lambda tag: tag.name == "div" and tag.get("class") == ["clearfix"]
        )
        for block in blocks:
            if block:
                anchors = block.find_all("a", itemprop="author")
                for anchor in anchors:
                    if anchor:
                        name_span = anchor.find("span", itemprop="name")
                        name = name_span.text.strip() if name_span else None
                        href = anchor["href"] if "href" in anchor.attrs else None

                        if name:
                            persons[name] = href

        return persons



    persons = get_person_links(soup)

    details_list = []

    for name, link in persons.items():
        if link not in linkp_list:
            person_response = requests.get(f"https://www.iranketab.ir{link}", timeout=30)
            if person_response.status_code == 200:
                person_soup = BeautifulSoup(person_response.content, "html.parser")

                person_id = link.split("/")[-1].split("-")[0]
                person_div = person_soup.find("div", class_="col-md-9")

                person_description = None
                if person_div:
                    h5_tag = person_div.find("h5")
                    if h5_tag:
                        person_description = h5_tag.text.strip()

                details_list.append(
                    {"name": name, "id": person_id, "description": person_description}
                )
                linkp_list.append(link)

    df_person_book = pd.DataFrame(details_list)

    book_id = url.split("/")[-1].split("-")[0]

    description_div = soup.find("div", class_="product-description")

    book_description = None
    if description_div:
        book_description = description_div.text.strip()

    df_book1 = pd.DataFrame({"group_id": book_id, "description": book_description}, index=[0])


    #getting categories
    tag_links = soup.find_all("a", class_="product-tags-item")

    details_list = []
    for link in tag_links:
        hashtag_url = f"https://www.iranketab.ir{link['href']}"
        if hashtag_url not in hashtag_urls_list:
            hashtag_response = requests.get(hashtag_url, timeout=30)
            if hashtag_response.status_code == 200:
                hashtag_urls_list.append(hashtag_url)
                hashtag_soup = BeautifulSoup(hashtag_response.content, "html.parser")

                hashtag_id = link["href"].split("/")[-1].split("-")[0]

                description_div = hashtag_soup.find("div", class_="col-md-10")

                description = None
                if description_div:
                    h2_tag = description_div.find("h2")
                    if h2_tag:
                        description = h2_tag.text.strip()

                hashtag_text = link.text.strip()

                details_list.append(
                    {"id": hashtag_id, "name": hashtag_text, "description": description}
                )

    df_hashtags = pd.DataFrame(details_list)
    return df_hashtags, df_book1, df_person_book, linkp_list, hashtag_urls_list
