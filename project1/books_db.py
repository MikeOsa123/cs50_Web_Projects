import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# database engine object from SQLAlchemy that manages connections to the database
engine = create_engine(os.getenv("DATABASE_URL"))

# DATABASE_URL is an environment variable that indicates where the database lives

# create a 'scoped session' that ensures different users' interactions with the database are kept separate
db = scoped_session(sessionmaker(bind=engine))


db.execute("CREATE TABLE books(isbn VARCHAR NOT NULL PRIMARY KEY UNIQUE, title VARCHAR NOT NULL, author VARCHAR NOT NULL, year INT NOT NULL)")

db.execute("CREATE TABLE users(id SERIAL, username VARCHAR NOT NULL PRIMARY KEY UNIQUE, email VARCHAR NOT NULL UNIQUE, password VARCHAR NOT NULL)")

db.execute("CREATE TABLE reviews(username VARCHAR NOT NULL PRIMARY KEY UNIQUE REFERENCES users, isbn VARCHAR UNIQUE REFERENCES books NOT NULL, rating INT NOT NULL, review VARCHAR NOT NULL)")

db.commit()
