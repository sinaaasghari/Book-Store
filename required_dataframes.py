#creating required tables

import matplotlib.pyplot as plt
from sqlalchemy import create_engine, MetaData, table, column, URL, Select, Table
import pandas as pd
import mysql.connector

#Creating Database,Connection
meta = MetaData()
USERNAME = 'root'
PASSWORD = 'A1382L1234i@#'
SERVER = 'localhost'
PORT = 3306
DATABASE = 'book-store'

conn = mysql.connector.connect(
  host=SERVER,
  user=USERNAME,
  password=PASSWORD,
  database=DATABASE
)

#first request
def request_one():
    query = '''
    SELECT DISTINCT person.name,  COUNT(code) OVER (PARTITION BY counter) as num_of_romance_books, AVG(grade) OVER (PARTITION BY counter) as avg_grade,
                    person_prize.num_of_award_tags as num_of_awards_tags, person_list_tags.num_of_list_tags as num_of_list_tags, person.description as description
    FROM person
    JOIN crew on person.counter = crew.person_counter
    JOIN book on crew.book_code = book.code
    JOIN group_book on book.code = group_book.book_code
    JOIN `group` on group_book.group_id = `group`.id
    JOIN group_category on `group`.id = group_category.group_id
    JOIN category on group_category.category_id = category.id
    LEFT OUTER JOIN (SELECT DISTINCT person.name, COUNT(category.name) OVER (PARTITION BY (counter)) as num_of_award_tags
                     FROM person
                     JOIN crew on person.counter = crew.person_counter
                     JOIN book on crew.book_code = book.code
                     JOIN group_book on book.code = group_book.book_code
                     JOIN `group` on group_book.group_id = `group`.id
                     JOIN group_category on `group`.id = group_category.group_id
                     JOIN category on group_category.category_id = category.id
                     WHERE category.name LIKE '%جایزه%' AND book.code in (SELECT book.code
                                                                          FROM book
                                                                          JOIN group_book on book.code = group_book.book_code
                                                                          JOIN `group` on group_book.group_id = `group`.id
                                                                          JOIN group_category on `group`.id = group_category.group_id
                                                                          JOIN category on group_category.category_id = category.id
                                                                          WHERE category.name LIKE '%عاشقانه%')) as person_prize on person.name = person_prize.name
    LEFT OUTER JOIN (SELECT DISTINCT person.name, COUNT(category.name) OVER (PARTITION BY (counter)) as num_of_list_tags
                     FROM person
                     JOIN crew on person.counter = crew.person_counter
                     JOIN book on crew.book_code = book.code
                     JOIN group_book on book.code = group_book.book_code
                     JOIN `group` on group_book.group_id = `group`.id
                     JOIN group_category on `group`.id = group_category.group_id
                     JOIN category on group_category.category_id = category.id
                     WHERE category.name LIKE '%گزیده%' OR category.name LIKE '%ترین%' AND book.code in (SELECT book.code
                                                                          FROM book
                                                                          JOIN group_book on book.code = group_book.book_code
                                                                          JOIN `group` on group_book.group_id = `group`.id
                                                                          JOIN group_category on `group`.id = group_category.group_id
                                                                          JOIN category on group_category.category_id = category.id
                                                                          WHERE category.name LIKE '%عاشقانه%')) as person_list_tags on person.name = person_list_tags.name
    WHERE category.name LIKE '%عاشقانه%' AND role = 'writer'
    ORDER BY num_of_romance_books DESC, avg_grade DESC;
    '''
    return pd.read_sql(query, conn)

#second request
def request_two():
    query = '''
    SELECT DISTINCT book.code, book.title_persian, title_english,price, release_year_mi, release_year_sh, grade, page_count, cover, book_prize.num_of_award_tags,
                    book_list_tags.num_of_list_tags
    FROM book
    JOIN group_book on book.code = group_book.book_code
    JOIN `group` on group_book.group_id = `group`.id
    JOIN group_category on `group`.id = group_category.group_id
    join category on group_category.category_id = category.id
    LEFT OUTER JOIN (SELECT DISTINCT book.code, COUNT(category.name) OVER (PARTITION BY (book.code)) as num_of_award_tags
                 FROM book
                 JOIN group_book on book.code = group_book.book_code
                 JOIN `group` on group_book.group_id = `group`.id
                 JOIN group_category on `group`.id = group_category.group_id
                 JOIN category on group_category.category_id = category.id
                 WHERE category.name LIKE '%جایزه%') as book_prize on book.code = book_prize.code
    LEFT OUTER JOIN (SELECT DISTINCT DISTINCT book.code, COUNT(category.name) OVER (PARTITION BY (code)) as num_of_list_tags
                     FROM book
                     JOIN group_book on book.code = group_book.book_code
                     JOIN `group` on group_book.group_id = `group`.id
                     JOIN group_category on `group`.id = group_category.group_id
                     JOIN category on group_category.category_id = category.id
                     WHERE category.name LIKE '%گزیده%' OR category.name LIKE '%ترین%') as book_list_tags on book.code = book_list_tags.code;
    
    '''
    return pd.read_sql(query, conn)


#third request
def request_three():
    query = '''
    SELECT DISTINCT publisher.name, count(book.code) OVER (partition by publisher.id) as num_of_historic_books,
           AVG(grade) OVER (PARTITION BY publisher.id) as avg_grade,
           publisher_prize.num_of_award_tags,
           publisher_list_tags.num_of_list_tags
    FROM publisher
    JOIN book_publisher on publisher.id = book_publisher.publisher_id
    JOIN book on book_publisher.book_code = book.code
    JOIN group_book on book.code = group_book.book_code
    JOIN `group` on group_book.group_id = `group`.id
    JOIN group_category on `group`.id = group_category.group_id
    JOIN category on group_category.category_id = category.id
    LEFT OUTER JOIN (SELECT DISTINCT publisher.id, COUNT(category.name) OVER (PARTITION BY (publisher.id)) as num_of_award_tags
                 FROM publisher
                 JOIN book_publisher on publisher.id = book_publisher.publisher_id
                 JOIN book on book_publisher.book_code = book.code
                 JOIN group_book on book.code = group_book.book_code
                 JOIN `group` on group_book.group_id = `group`.id
                 JOIN group_category on `group`.id = group_category.group_id
                 JOIN category on group_category.category_id = category.id
                 WHERE category.name LIKE '%جایزه%' AND book.code in (SELECT book.code
                                                                          FROM book
                                                                          JOIN group_book on book.code = group_book.book_code
                                                                          JOIN `group` on group_book.group_id = `group`.id
                                                                          JOIN group_category on `group`.id = group_category.group_id
                                                                          JOIN category on group_category.category_id = category.id
                                                                          WHERE category.name LIKE '%تاریخ%')) as publisher_prize on publisher.id = publisher_prize.id
    LEFT OUTER JOIN (SELECT  DISTINCT publisher.id, COUNT(category.name) OVER (PARTITION BY (publisher.id)) as num_of_list_tags
                     FROM publisher
                     JOIN book_publisher on publisher.id = book_publisher.publisher_id
                     JOIN book on book_publisher.book_code = book.code
                     JOIN group_book on book.code = group_book.book_code
                     JOIN `group` on group_book.group_id = `group`.id
                     JOIN group_category on `group`.id = group_category.group_id
                     JOIN category on group_category.category_id = category.id
                     WHERE category.name LIKE '%گزیده%' OR category.name LIKE '%ترین%' AND book.code in (SELECT book.code
                                                                          FROM book
                                                                          JOIN group_book on book.code = group_book.book_code
                                                                          JOIN `group` on group_book.group_id = `group`.id
                                                                          JOIN group_category on `group`.id = group_category.group_id
                                                                          JOIN category on group_category.category_id = category.id
                                                                          WHERE category.name LIKE '%تاریخ%')) as publisher_list_tags on publisher.id = publisher_list_tags.id
    WHERE category.name LIKE '%تاریخ%'
    ORDER BY num_of_historic_books DESC , num_of_award_tags DESC , num_of_list_tags DESC ;
    
    '''
    return pd.read_sql(query, conn)


#first hypothesis
def hypothesis_one():
    query = '''
    SELECT code, price
    FROM book
    JOIN crew on book.code = crew.book_code
    WHERE code not in (SELECT DISTINCT book_code
                       FROM crew
                       WHERE role = 'translator')
    ORDER BY price DESC ;
    '''
    return pd.read_sql(query, conn)

#second hypothesis
def hypothesis_two():
    query = '''
    SELECT code, price, cover
    FROM book
    WHERE cover = 'جلدسخت' OR cover = 'شومیز'
    ORDER BY price DESC, cover ;
    '''
    return pd.read_sql(query, conn)

