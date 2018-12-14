import os

from flask import Flask, session, render_template, request, flash, redirect, url_for
from forms import RegistrationForm, LoginForm
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from rauth.service import OAuth1Service, OAuth1Session
import json


app = Flask(__name__)

app.config['SECRET_KEY'] = '727be3890612929864c8ed60b06d361b'

# consumer key & secret from: https://www.goodreads.com/api/keys
CONSUMER_KEY = 'EETgcvhVNUCW6Xd7fCRBQ'
CONSUMER_SECRET = '6RvW9pjgDxhUgZGOeYORhTpdqd4eODdcMTRtgmAneg'

goodreads = OAuth1Service(
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    name='goodreads',
    request_token_url='https://www.goodreads.com/oauth/request_token',
    authorize_url='https://www.goodreads.com/oauth/authorize',
    access_token_url='https://www.goodreads.com/oauth/access_token',
    base_url='https://www.goodreads.com/'
    )

# head_auth=True is important here; this doesn't work with oauth2 for some reason
request_token, request_token_secret = goodreads.get_request_token(header_auth=True)

authorize_url = goodreads.get_authorize_url(request_token)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = os.getenv("SECRET_KEY")

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")


# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/", methods=['GET','POST'])
def index():
    if request.method == 'POST':
        session['search'] = request.form['search']
        session['column'] = request.form['column']

        return redirect(url_for('results'))

    return render_template("index.html")

@app.route("/results")
def results():
    # return list of queried search
    query = db.execute("Select * from books where " + session['column'] + " ilike '%" + session['search'] + "%'").fetchall()
    if query is None:
        flash('Book not found, please search again!', 'danger')
        return redirect(url_for('index'))
    
    return render_template("results.html", query = query)

# Registration route and acpturing user information into the database
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        print(f"The user {username} has just registered using the email address: {email}")

        # checks database for duplicate username entries, must be unique
        try: 
            db.execute('INSERT INTO users (username, email, password) VALUES (:username, :email, :password)',
            {'username': username, 'email': email, 'password': password})
            db.commit()        
        except:
            flash('username taken, try another, or if this is your username, go to the sign in page', 'danger')
            return redirect(url_for('register'))

    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for("index"))


    return render_template("register.html", form=form)

# Login route and authenticating user login credentials 
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        
        if db.execute('SELECT username, password FROM users WHERE username = :username AND password = :password', {"username": username, "password": password}).rowcount == 0:
            print("Error occured")
            flash('username and/or password does not match', 'danger')
            return redirect(url_for("login"))

        else:
            print("success")
            session['username'] = request.form['username']
            print(session['username'])

    if form.validate_on_submit():
        flash(f'{username} you are now logged in!', 'success')
        return redirect(url_for("index"))

    return render_template("login.html", form=form)

    if __name__ == '__main__':
        app.run(debug=true)

@app.route('/logout')
def logout():
       # remove the username from the session if it is there
   session.pop('username', None)
   flash('You have now been logged out!', 'warning')
   return redirect(url_for('login'))

@app.route("/about")
def about():
    return render_template("index.html")

@app.route("/books")
def books():
    return render_template("book_page.html")

@app.route('/<isbn_variable>', methods=['Get', 'POST'])
def book(isbn_variable):
    """Creates a Book page for a specific book by ISBN"""
    # searches for book information in the database
    book = db.execute("Select * from books where isbn = '" + isbn_variable + "'").fetchall()
    # makes API call to Goodreads for needed information
    APIcall = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": CONSUMER_KEY, "isbns": isbn_variable})
    stuff = APIcall.json()
    avg_rating = stuff['books'][0]['average_rating']
    ratings_count = stuff['books'][0]['ratings_count']
    # searches for reviews in our review database
    reviews = db.execute("Select * from reviews where isbn = '" + isbn_variable + "'").fetchall()
    # adds review for user if they haven't posted one yet. 
    if request.method == 'POST':
        user = session['username']
        stars = request.form['stars']
        review = request.form['review']
        try:
            db.execute('INSERT into reviews (username, isbn, stars, review) VALUES (:username, :isbn, :stars, :review)',
            {"username": user, "isbn": isbn_variable, "stars": stars, "review": review})
            db.commit()
            flash('Review Submitted')
        except:
            flash("You've already submitted a review for this book")
        return render_template('result.html', book=book, reviews=reviews, avg_rating=avg_rating, ratings_count=ratings_count)
    return render_template('result.html', book=book, reviews=reviews, avg_rating=avg_rating, ratings_count=ratings_count)