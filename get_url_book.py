import requests
from bs4 import BeautifulSoup
import logging
import pandas as pd
import csv
# https://www.iranketab.ir/book?pagenumber=1&pagesize=1000
url = 'https://www.iranketab.ir/book'

logging.basicConfig(filename="logfile.txt",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.WARNING)

def list_link_books(url,count):
    """_summary_
    Args:
        url (_str_):  url site
        count (_int_): count url book its a multiple 1000
    """
    fields = ["book_url"]
    with open("book_url.csv", "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        
    headers = {
    'Accept-Language': 'en-US,en;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }
    pagenumber = int(count/1000)
    pagesize =int(count/pagenumber)
    for pagenumber in range(1,pagenumber+1):
        url_pagenumber = url + f'?pagenumber={pagenumber}&pagesize={pagesize}'
        response = requests.get(url_pagenumber, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        books_list = soup.find_all('div',attrs={'class':'col-lg-6 col-md-6 col-xs-12'})
        i=0
        for book in books_list:
            i=i+1
            try:
                book_tag_a = book.find('a',attrs={'class':'product-item-link'})
                book_url ='https://www.iranketab.ir'+ book_tag_a.get('href')
                book_url =[book_url]
                with open('book_url.csv', 'a',newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(book_url)
            except:
                logging.warning(f'failed to find url book[{pagenumber},{i}]')
            print(i)
results = list_link_books(url,50000)