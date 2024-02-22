import requests
import urllib.parse
import os

import sys
from cs50 import SQL
from flask import Flask, render_template, redirect, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
from jinja2 import Environment, FileSystemLoader
from functools import wraps
from werkzeug.utils import secure_filename

# Configure app
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///bakery.db")

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Upload image configuration
app.config["IMAGE_UPLOADS"] = "/workspaces/100541283/final_project/bakery_webpage/static"

# Global variables
brand_password = "r#NF%$9>A6fK"


""" Finance login_required function """
def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

# Running the webpage
#_______________________________________#
@app.route("/")
def index():
    """ Homepage """
    return redirect("/home")

#_______________________________________#
@app.route("/home")
def home():
    """ Homepage """

    # Getting all homepages' stuff
    slides = db.execute("SELECT * FROM slides")
    welcoming = db.execute("SELECT * FROM welcoming")
    products = db.execute("SELECT * FROM products")
    contacts = db.execute("SELECT * FROM contacts")

    return render_template("home.html", slides=slides, welcoming=welcoming, products=products, contacts=contacts)

#_______________________________________#
@app.route("/breads")
def breads():
    """ Breads list products """
    breads = db.execute("SELECT * FROM breads")

    return render_template("breads.html", breads_list=breads)

#_______________________________________#
@app.route("/desserts")
def desserts():
    """ desserts list products """
    desserts = db.execute("SELECT * FROM desserts")

    return render_template("desserts.html", desserts_list=desserts)


#_______________________________________#
@app.route("/cakes")
def cakes():
    """ Cakes list products """
    cakes = db.execute("SELECT * FROM cakes")

    return render_template("cakes.html", cakes_list=cakes)

#_______________________________________#
@app.route("/login", methods=["GET", "POST"])
def login():
    """ Log in """
        # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("apology.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("apology.html")

        # Query database for username
        rows = db.execute("SELECT * FROM admin WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("apology.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/edit")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


#_______________________________________#
@app.route("/register", methods=["GET", "POST"])
def register():
    """ Register """
    # User reached route via POST
    if request.method == "POST":
        global brand_password

        # Ensure user submitted username and password
        if not request.form.get("username"):
            return render_template("apology.html")

        elif not request.form.get("password"):
            return render_template("apology.html")

        elif not request.form.get("confirmation"):
            return render_template("apology.html")

        elif not request.form.get("brand_key") or (request.form.get("brand_key") != brand_password):
            return render_template("apology.html")

        # Ensure both password and confirmation password match
        if request.form.get("password") != request.form.get("confirmation"):
            return render_template("apology.html")


        # Generating a hash of the password
        hash = generate_password_hash(request.form.get("password"))

        # Adding the user
        db.execute("INSERT INTO admin (username, hash) VALUES (?, ?)", request.form.get("username"), hash)
        user_id = db.execute("SELECT id FROM admin WHERE username = ?", request.form.get("username"))
        session[user_id[0]["id"]] = user_id[0]["id"]
        return redirect("/login")

    # User reached via GET
    else:
        return render_template("register.html")


#_______________________________________#
@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    # User reached via POST
    if request.method == "POST":

        # Changing first slide if wanted
        slide1 = request.files['first_slide']
        if not slide1.filename == "":
            filename = secure_filename(slide1.filename)

            basedir = os.path.abspath(os.path.dirname(__file__))
            slide1.save(os.path.join(basedir,app.config["IMAGE_UPLOADS"], filename))
            delete_filename = db.execute("SELECT name FROM slides WHERE id='first'")
            os.remove("/workspaces/100541283/final_project/bakery_webpage/static/" + str(delete_filename[0]['name']))

            db.execute("UPDATE slides SET name=? WHERE id='first'", filename)
            return redirect("/edit")

        # Changing first slide if wanted
        slide2 = request.files['second_slide']
        if not slide2.filename == "":
            filename = secure_filename(slide2.filename)

            basedir = os.path.abspath(os.path.dirname(__file__))
            slide2.save(os.path.join(basedir,app.config["IMAGE_UPLOADS"], filename))
            delete_filename = db.execute("SELECT name FROM slides WHERE id='second'")
            os.remove("/workspaces/100541283/final_project/bakery_webpage/static/" + str(delete_filename[0]['name']))

            db.execute("UPDATE slides SET name=? WHERE id='second'", filename)
            return redirect("/edit")

        # Changing first slide if wanted
        slide3 = request.files['third_slide']
        if not slide3.filename == "":
            filename = secure_filename(slide3.filename)

            basedir = os.path.abspath(os.path.dirname(__file__))
            slide3.save(os.path.join(basedir,app.config["IMAGE_UPLOADS"], filename))
            delete_filename = db.execute("SELECT name FROM slides WHERE id='third'")
            os.remove("/workspaces/100541283/final_project/bakery_webpage/static/" + str(delete_filename[0]['name']))

            db.execute("UPDATE slides SET name=? WHERE id='third'", filename)
            return redirect("/edit")

        return redirect("/apology")


    # User reached via GET
    else:
        slides = db.execute("SELECT * FROM slides")
        return render_template("edit.html", slides=slides)


#_______________________________________#
@app.route("/breads_edit", methods=["GET", "POST"])
@login_required
def breads_edit():
    """ Breads Admin Page """
    # User reached via POST
    if request.method == "POST":
        # Getting the amount of products are
        breads_count = db.execute("SELECT count FROM products_count WHERE product='breads'")
        breads_count = breads_count[0]["count"]

        # Getting all the ids of the db
        ids = db.execute("SELECT id FROM breads")

        # Checking if the user wants to delete a product
        for i in range(breads_count):
            if not request.form.get(str(ids[i]['id'])):
                continue
            else:
                filename = db.execute("SELECT image FROM breads WHERE id=?", str(ids[i]['id']))
                os.remove("/workspaces/100541283/final_project/bakery_webpage/static/" + str(filename[0]['image']))
                db.execute("DELETE FROM breads WHERE id=?", str(ids[i]['id']))
                db.execute("UPDATE products_count SET count=? WHERE product='breads'", breads_count-1)
                return redirect("/breads_edit")

        # Ensure user input all required sections
        image = request.files['file']
        if not request.files['file'] or image.filename == "":
            return render_template("apology.html")

        if not request.form.get("product_title"):
            return render_template("apology.html")

        if not request.form.get("product_cost"):
            return render_template("apology.html")

        if not request.form.get("product_description"):
            return render_template("apology.html")

        # Getting the image and downoading it
        filename = secure_filename(image.filename)

        basedir = os.path.abspath(os.path.dirname(__file__))
        image.save(os.path.join(basedir,app.config["IMAGE_UPLOADS"], filename))

        # Adding each input to the database
        db.execute("INSERT INTO breads (image, title, cost, description) VALUES (?, ?, ?, ?)",
                  filename, request.form.get("product_title"), request.form.get("product_cost"), request.form.get("product_description"))
        db.execute("UPDATE products_count SET count=? WHERE product='breads'", breads_count+1)
        return redirect("/breads_edit")

    # User reached via GET
    else:
        breads = db.execute("SELECT * FROM breads")
        return render_template("breads_edit.html", breads_list=breads)


#_______________________________________#
@app.route("/cakes_edit", methods=["GET", "POST"])
@login_required
def cakes_edit():
    """ Cakes Admin Page """
    # User reached via POST
    if request.method == "POST":
        # Getting the amount of products are
        cakes_count = db.execute("SELECT count FROM products_count WHERE product='cakes'")
        cakes_count = cakes_count[0]["count"]

        # Getting all the ids of the db
        ids = db.execute("SELECT id FROM cakes")

        # Checking if the user wants to delete a product
        for i in range(cakes_count):
            if not request.form.get(str(ids[i]['id'])):
                continue
            else:
                filename = db.execute("SELECT image FROM cakes WHERE id=?", str(ids[i]['id']))
                os.remove("/workspaces/100541283/final_project/bakery_webpage/static/" + str(filename[0]['image']))
                db.execute("DELETE FROM cakes WHERE id=?", str(ids[i]['id']))
                db.execute("UPDATE products_count SET count=? WHERE product='cakes'", cakes_count-1)
                return redirect("/cakes_edit")

        # Ensure user input all required sections
        image = request.files['file']
        if not request.files['file'] or image.filename == "":
            return render_template("apology.html")

        if not request.form.get("product_title"):
            return render_template("apology.html")

        if not request.form.get("product_cost"):
            return render_template("apology.html")

        if not request.form.get("product_description"):
            return render_template("apology.html")

        # Getting the image and downoading it
        filename = secure_filename(image.filename)

        basedir = os.path.abspath(os.path.dirname(__file__))
        image.save(os.path.join(basedir,app.config["IMAGE_UPLOADS"], filename))

        # Adding each input to the database
        db.execute("INSERT INTO cakes (image, title, cost, description) VALUES (?, ?, ?, ?)",
                  filename, request.form.get("product_title"), request.form.get("product_cost"), request.form.get("product_description"))
        db.execute("UPDATE products_count SET count=? WHERE product='cakes'", cakes_count+1)
        return redirect("/cakes_edit")

    # User reached via GET
    else:
        cakes = db.execute("SELECT * FROM cakes")
        return render_template("cakes_edit.html", cakes_list=cakes)


#_______________________________________#
@app.route("/desserts_edit", methods=["GET", "POST"])
@login_required
def desserts_edit():
    """ Desserts Admin Page """
    # User reached via POST
    if request.method == "POST":
        # Getting the amount of products are
        breads_count = db.execute("SELECT count FROM products_count WHERE product='breads'")
        breads_count = breads_count[0]["count"]

        # Getting all the ids of the db
        ids = db.execute("SELECT id FROM breads")

        # Checking if the user wants to delete a product
        for i in range(breads_count):
            if not request.form.get(str(ids[i]['id'])):
                continue
            else:
                filename = db.execute("SELECT image FROM breads WHERE id=?", str(ids[i]['id']))
                os.remove("/workspaces/100541283/final_project/bakery_webpage/static/" + str(filename[0]['image']))
                db.execute("DELETE FROM breads WHERE id=?", str(ids[i]['id']))
                db.execute("UPDATE products_count SET count=? WHERE product='breads'", breads_count-1)
                return redirect("/breads_edit")

        # Ensure user input all required sections
        image = request.files['file']
        if not request.files['file'] or image.filename == "":
            return render_template("apology.html")

        if not request.form.get("product_title"):
            return render_template("apology.html")

        if not request.form.get("product_cost"):
            return render_template("apology.html")

        if not request.form.get("product_description"):
            return render_template("apology.html")

        # Getting the image and downoading it
        filename = secure_filename(image.filename)

        basedir = os.path.abspath(os.path.dirname(__file__))
        image.save(os.path.join(basedir,app.config["IMAGE_UPLOADS"], filename))

        # Adding each input to the database
        db.execute("INSERT INTO breads (image, title, cost, description) VALUES (?, ?, ?, ?)",
                  filename, request.form.get("product_title"), request.form.get("product_cost"), request.form.get("product_description"))
        db.execute("UPDATE products_count SET count=? WHERE product='breads'", breads_count+1)
        return redirect("/breads_edit")

    # User reached via GET
    else:
        breads = db.execute("SELECT * FROM breads")
        return render_template("breads_edit.html", breads_list=breads)


@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/login")