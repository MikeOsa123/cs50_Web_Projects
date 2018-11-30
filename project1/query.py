from import_db import Base, Books
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgres://mpqnzaliuamutf:e13162afb75547673fa5b9616074eeb400fd5609cee4a2eefe3602a6211a778a@ec2-54-217-235-16.eu-west-1.compute.amazonaws.com:5432/d4mmdaqctskcqf')
Base.metadata.bind = engine

DBSession = sessionmaker()
DBSession.bind = engine
session = DBSession()

first_book = session.query(Books).first()
print(first_book.title)