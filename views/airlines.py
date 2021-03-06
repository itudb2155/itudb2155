from flask import Blueprint, request, render_template, redirect, url_for, session, flash
import psycopg2 as db
import os

airlines = Blueprint("airlines", import_name=__name__, template_folder="templates")


@airlines.route("/airlines", methods=["GET", "POST"])
def airlines_page():
    connection = db.connect(os.getenv("DATABASE_URL"))
    cur = connection.cursor()
    if request.method == "GET":
        cur.execute("SELECT * FROM airlines ORDER by ticker")
        list_airlines = cur.fetchall()
        print(list_airlines)
        cur.close()
        return render_template("airlines_page.html", list_airlines=list_airlines)
    else:
        if session["isAdmin"] == False:
            flash("Only admins have operate on this", "danger")
            return redirect(url_for("airlines.airlines_page"))
        airline_keys = request.form.getlist("airline_keys")
        for form_airline_key in airline_keys:
            cur.execute("DELETE FROM airlines WHERE id = {0}".format(form_airline_key))
        connection.commit()
        cur.close()
        return redirect(url_for("airlines.airlines_page"))


@airlines.route("/add_airline", methods=["POST", "GET"])
def add_airline():
    if session["isAdmin"] == False:
        flash("Only admins have operate on this", "danger")
        return redirect(url_for("airlines.airlines_page"))
    connection = db.connect(os.getenv("DATABASE_URL"))
    if request.method == "GET":
        return render_template("airlines_add.html")
    if "username" in session:
        cur = connection.cursor()
        if request.method == "POST":
            airline_ticker = request.form["airline_ticker"]
            airline_name = request.form["airline_name"]
            if len(airline_ticker) != 2:
                flash("Ticker must be 2 consists by two characters", "danger")
                return redirect(url_for("airlines.airlines_page"))
            cur.execute(
                "INSERT INTO airlines(ticker,name) VALUES (%s,%s)",
                (airline_ticker, airline_name),
            )
            connection.commit()
            cur.close()
            return redirect(url_for("airlines.airlines_page"))


@airlines.route("/airline_update/<id>", methods=["POST", "GET"])
def update_airline(id):
    if session["isAdmin"] == False:
        flash("Only admins have operate on this", "danger")
        return redirect(url_for("airlines.airlines_page"))
    connection = db.connect(os.getenv("DATABASE_URL"))
    cur = connection.cursor()
    if request.method == "GET":
        cur.execute("SELECT * FROM airlines WHERE id = {0}".format(id))
        airline_info = cur.fetchall()
        cur.close()
    if request.method == "POST":
        airline_ticker = request.form["airline_ticker"]
        airline_name = request.form["airline_name"]
        if len(airline_ticker) != 2:
            flash("Ticker must be 2 consists by two characters", "danger")
            return redirect(url_for("airlines.airlines_page"))
        cur.execute(
            "UPDATE airlines SET ticker = %s, name = %s WHERE id = %s",
            (airline_ticker, airline_name, id),
        )
        connection.commit()
        cur.close()
        return redirect(url_for("airlines.airlines_page"))
    return render_template("airlines_update.html", airline_info=airline_info)
