from flask import Flask, render_template, session, flash, redirect, url_for
import webbrowser, sqlite3, os

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():

    if session.get('logado'):
        pass
    else:
        return render_template('home.html')
