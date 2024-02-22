import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from jinja2 import Environment, FileSystemLoader


from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # Getting the users' stock
    user_id = int(session["user_id"])
    stock_owned = db.execute("SELECT * FROM bought WHERE user_id=?", user_id)
    total = list()
    i = 0
    lenght = len(stock_owned)
    for stock in stock_owned:
        price = str(stock["stock_price"])
        price = price.replace(",", "")
        price = str(price[1:])
        total.append(float(price) * float(stock["shares"]))
        total[i] = "{:.2f}".format(total[i])
        i += 1

    # Getting users' cash
    cash_user = db.execute("SELECT cash FROM users WHERE id=?",user_id)
    cash_user = usd(cash_user[0]["cash"])

    # Returning the index page
    return render_template("/index.html", user_stock=stock_owned, total=total, lenght=lenght, cash=cash_user)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        # Ensure 'shares' input is valid
        try:
            if not request.form.get("shares") or (int(request.form.get("shares")) < 1):
                return apology("must provide a valid number")
        except:
            return apology("must provide a valid number")

        # Ensure 'stock' symbol is valid and if there is an input
        if (lookup(request.form.get("symbol")) == None) or not request.form.get("symbol"):
            return apology("couldn't find the stock symbol")

        # Getting the stocks symbol and shares
        symbol = lookup(request.form.get("symbol"))
        shares = int(request.form.get("shares"))

        # Getting all variables needed
        user_id = int(session["user_id"])
        cash_user = db.execute("SELECT cash FROM users WHERE id=?",user_id)
        cash_user = int(cash_user[0]["cash"])
        cost = float(symbol["price"]) * shares
        price = usd(symbol["price"])

        # Checking if user can afford the stock
        if (cash_user) < (cost):
            return apology("can't afford stock")

        # Executing purchase
        else:
            stock_owned = db.execute("SELECT * FROM bought WHERE user_id=?", user_id)

            # Checking if the stock already exists
            for stock in stock_owned:
                if stock["stock_symbol"] == symbol["symbol"]:
                    # UPDATE shares
                    db.execute("UPDATE bought SET shares=? WHERE stock_symbol=? AND stock_name=? AND user_id=?",
                              (int(stock["shares"]) + shares), symbol["symbol"], symbol["name"], user_id)
                    return redirect("/")

                # If it doesn't, create a new space in the bought db
            db.execute("INSERT INTO bought VALUES (?, ?, ?, ?, ?)",
                        user_id, shares, price, symbol["name"], symbol["symbol"])
            db.execute("UPDATE users SET cash=? WHERE id=?", (cash_user - cost), user_id)
            return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO: HISTORY")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # User reached route via POST
    if request.method == "POST":

        # Getting the stock symbol and saving it in a dict
        query = request.form.get("symbol")

        # Ensure that there is stock
        if lookup(query) == None:
            return apology("Couldn't find stock symbol")

        # Returning the quoted values
        quoted = lookup(query)
        price = usd(quoted["price"])
        return render_template("quoted.html", quoted=quoted, price=price)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure user submitted username and password
        if not request.form.get("username"):
            return apology("must provide username", 400)
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        elif not request.form.get("confirmation"):
            return apology("must provide a confirmation", 400)

        # Ensure both password and confirmation password match
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("password and confirmation doesn't match", 400)

        # Checking if the username is already taken
        rows = db.execute("SELECT username FROM users WHERE username = ?", request.form.get("username"))
        if len(rows) > 0:
            return apology("username is already taken", 400)

        # Generating a hash of the password
        hash = generate_password_hash(request.form.get("password"))

        # Adding the user
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get("username"), hash)
        user_id = db.execute("SELECT id FROM users WHERE username = ?", request.form.get("username"))
        session[user_id[0]["id"]] = user_id[0]["id"]
        return redirect("/")

    # User reached via GET
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure user selected a symbol
        if not request.form.get("symbol"):
            return apology("must provide a symbol")

        # Ensure user typed a share and a positive number
        if (not request.form.get("shares")) or (int(request.form.get("shares")) < 1):
            return apology("must provide a valid share number")

        # Executing the sale
        else:
            # Getting the users' stock
            user_id = int(session["user_id"])
            stock_owned = db.execute("SELECT * FROM bought WHERE user_id=?", user_id)
            symbol = lookup(request.form.get("symbol"))
            shares = int(request.form.get("shares"))

            # Deleting the symbol from users bought or shares
            for stock in stock_owned:
                if stock["stock_symbol"] == symbol["symbol"]:
                    if (int(stock["shares"]) - shares) == 0:
                        db.execute("DELETE FROM bought WHERE user_id=? AND stock_name=?",
                                    user_id, symbol["name"])
                    elif int(stock["shares"]) < shares:
                        return apology("can't sell that amount of shares")
                    else:
                        stock["shares"] = int(stock["shares"]) - shares
                        db.execute("UPDATE bought SET shares=? WHERE user_id=? AND stock_symbol=?",
                                    stock["shares"], user_id, symbol["symbol"])

            # Getting the money back
            current_cash = db.execute("SELECT cash FROM users WHERE id=?",user_id)
            new_cash = (float(symbol["price"]) * float(shares)) + current_cash[0]["cash"]
            db.execute("UPDATE users SET cash=? WHERE id=?", new_cash, user_id)
            return redirect("/")

    # User reached via GET
    else:
        user_id = int(session["user_id"])
        stock_owned = db.execute("SELECT * FROM bought WHERE user_id=?", user_id)
        return render_template("sell.html", user_stock=stock_owned)
