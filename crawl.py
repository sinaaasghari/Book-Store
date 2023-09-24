import requests
from bs4 import BeautifulSoup
import json
import re
import pandas as pd
from time import sleep
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
import urllib.parse
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

links = list(set(links[1:10]))

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

#=================================================================================================================
#Getting each page details
#getting description
def get_writer_translators_groub_category_description(url):
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

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

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

    df_book = pd.DataFrame({"group_id": book_id, "description": book_description}, index=[0])




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
    df_group_description = pd.concat([df_group_description, df_book])
    df_group_description.drop_duplicates(inplace=True)
    #inserting data into person df
    df_person = pd.concat([df_person, df_person_book])
    df_person.drop_duplicates(inplace=True)
    #inserting data into category df
    df_category = pd.concat([df_category, df_hashtags])
    df_category.drop_duplicates(inplace=True)

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
        future_to_url = (executer.submit(get_writer_translators_groub_category_description, link) for link in req_list)
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



#=======================================================================================
#make csv
df_group_description.to_csv('group_description.csv', index=False, encoding='utf-8-sig')
df_person.to_csv('person.csv', index=False, encoding='utf-8-sig')
df_category.to_csv('category.csv', index=False, encoding='utf-8-sig')

print("Done!")
