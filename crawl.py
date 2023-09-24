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

csv_file = 'book_url.csv'
with open(csv_file, 'r') as file:
    csv_reader = csv.reader(file)
    links = list()
    for row in csv_reader:
        links.append(row[0])

links = list(set(links[1:]))

#header of each request
headers = {"Accept-Language": "en-US,en;q=0.5",
           "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}

#Getting each page details
def get_book_detail(link):
    response = requests.get(link, headers=headers, timeout=timeout)
    return response



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
        future_to_url = (executer.submit(get_book_detail, link) for link in req_list)
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
    print(count)
    count += 1




