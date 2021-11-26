from flask import Blueprint, request, render_template, redirect, url_for
import psycopg2 as db
import os

airlines = Blueprint('airlines', import_name=__name__,
                     template_folder="templates")


@airlines.route("/airlines",  methods=["GET", "POST"])
def airlines_page():
    connection = db.connect(os.getenv("DATABASE_URL"))
    cur = connection.cursor()
    if request.method == "GET":
        cur.execute("SELECT * FROM airlines")
        list_airlines = cur.fetchall()
        cur.close()
        return render_template("airlines_page.html", list_airlines=list_airlines)
    else:
        airline_keys = request.form.getlist("airline_keys")
        for form_airline_key in airline_keys:
            cur.execute('DELETE FROM airlines WHERE id = {0}'.format(form_airline_key))
        connection.commit()
        cur.close()
        return redirect(url_for('airlines.airlines_page'))



@airlines.route("/add_airline",  methods=["POST"])
def add_airline():
    connection = db.connect(os.getenv("DATABASE_URL"))
    cur = connection.cursor()
    if request.method == 'POST':
        airline_ticker = request.form['airline_ticker']
        airline_name = request.form['airline_name']
        cur.execute("INSERT INTO airlines(ticker,name) VALUES (%s,%s)",
                    (airline_ticker, airline_name))
        connection.commit()
        cur.close()
        return redirect(url_for('airlines.airlines_page'))