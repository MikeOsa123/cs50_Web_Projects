import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import csv

# database engine object from SQLAlchemy that manages connections to the database
engine = create_engine(os.getenv("DATABASE_URL"))

# DATABASE_URL is an environment variable that indicates where the database lives

# create a 'scoped session' that ensures different users' interactions with the database are kept separate
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("/Users/admin/git_repo/cs50_Web_Projects/project1/books.csv")
    reader = csv.reader(f)
    # loop gives each column a name
    line_count = 0 #track how many lines of data is committed to the database
    next(reader, None)
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
        {"isbn":isbn, "title":title, "author":author, "year":year})
        # substitute values from CSV line into SQL command, as per this dict
        print(f"Added {title} written by {author}, published in the year {year}.")
        line_count += 1

        if line_count % 1000 == 0:
            db.commit()
            print("1000 lines of data has been committed to the database!")


if __name__ == "__main__":
    main()