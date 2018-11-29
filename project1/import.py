import csv
import os

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import insert
import pandas as pd

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
books = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()

class Books(Base):
    __tablename__ = "books"
    isbn = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    year = Column(Integer)

Base.metadata.create_all(engine)

df = pd.read_csv('/Users/michael.osamwonyi/CS50/cs50_Web_Projects/project1/books.csv')

df.columns = [c.lower() for c in df.columns] #postgres doesn't like capitals or spaces

df.to_sql("books_test2", engine, if_exists="append",index=False)




'''books_list = []

with open('books.csv', 'rb') as csvfile:
    tbl_reader = csv.reader(csvfile, delimiter=',')
    for row in tbl_reader:
        data = {'isbn':row[0], 'title':row[1], 'author':row[2], 'year':row[3]}
        books_list.append(data)'''
        



        
