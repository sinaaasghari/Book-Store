import pandas as pd
import mysql.connector
from sqlalchemy import create_engine, MetaData, URL, Identity
from sqlalchemy import Table, Column, Integer, String, BOOLEAN, DATE, ForeignKey


#Creating Database,Connection
meta = MetaData()
USERNAME = 'root'
PASSWORD = 'A1382L1234i@#'
SERVER = 'localhost'
PORT = 3306
DATABASE = 'book-store'

url_object = URL.create("mysql+mysqlconnector",
                        username=USERNAME,
                        password=PASSWORD,
                        host=SERVER,
                        database=DATABASE)
engine = create_engine(url_object)
conn = engine.connect()

#Creating Tables
#book
book = Table(
    'book', meta,
    Column('code', Integer, primary_key=True),
    Column('title_persian', String(50)),
    Column('title_english', String(50)),
    Column('price', Integer),
    Column('discount', Integer),
    Column('grade', Integer),
    Column('shabak', String(30)),
    Column('page_count', Integer),
    Column('release_year_sh', Integer),
    Column('release_year_mi', Integer),
    Column('exist', BOOLEAN),
    Column('earliest_access', DATE),
    Column('print_series', Integer),
    Column('cover', String(50)),
    Column('ghate', String(50))
)

#group
group = Table(
    'group', meta,
    Column('id', Integer, primary_key=True),
    Column('description', String(500))
)

#group_book
group_book = Table(
    'group_book', meta,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('group_id', Integer, ForeignKey('group.id'))
)

#person
person = Table(
    'person', meta,
    Column('counter', Identity, primary_key=True),
    Column('id', Integer),
    Column('name', String(50)),
    Column('description', String(500))
)

#publisher
publisher = Table(
    'publisher', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String(50))
)

#category
category = Table(
    'category', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String(50)),
    Column('description', String(500))
)

#group_category
group_category = Table(
    'group_category', meta,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('group_id', Integer, ForeignKey('group.id')),
    Column('category_id', Integer, ForeignKey('category.id'))
)

#book_publisher
book_publisher = Table(
    'book_publisher', meta,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('book_code', Integer, ForeignKey('book.code')),
    Column('publisher_id', Integer, ForeignKey('publisher.id'))
)

#crew
crew = Table(
    'crew', meta,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('book_code', Integer, ForeignKey('book.code')),
    Column('person_counter', Integer, ForeignKey('person.id')),
    Column('role', String(15))
)

meta.create_all(engine)