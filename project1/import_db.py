import csv
import os

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import insert

# Create an engine that setups connection to the database
engine = create_engine('postgres://mpqnzaliuamutf:e13162afb75547673fa5b9616074eeb400fd5609cee4a2eefe3602a6211a778a@ec2-54-217-235-16.eu-west-1.compute.amazonaws.com:5432/d4mmdaqctskcqf')

Base = declarative_base()

class Books(Base):
    # Define columns for the table books
    __tablename__ = "books"
    bookid = Column(Integer, primary_key=True)
    isbn = Column(String)
    title = Column(String)
    author = Column(String)
    year = Column(String)

# Creates all tables in the engine.
Base.metadata.create_all(engine)

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object.

session = DBSession()


# read from books.csv file using the reader object
with open('/Users/michael.osamwonyi/CS50/cs50_Web_Projects/project1/books.csv') as file:
        data = csv.reader(file)
        line_count = 0
        data_list = list(data)
        data_list = data_list[1:]
        for row in data_list:
            session.add(Books(isbn=row[0], title=row[1], author=row[2], year=row[3]))
            line_count += 1
            if line_count % 1000 == 0:
                session.commit()


        
