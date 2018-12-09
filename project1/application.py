import os

from flask import Flask, session, render_template, request, flash, redirect, url_for
from forms import RegistrationForm, LoginForm
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


app = Flask(__name__)

app.config['SECRET_KEY'] = '727be3890612929864c8ed60b06d361b'

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