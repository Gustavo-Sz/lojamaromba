from flask import Flask, render_template, url_for
import webbrowser

app = Flask(__name__)

@app.route("/")
def inicial():
    return render_template("teste.html")

webbrowser.open('http:\\localhost:5000')
app.run(debug=True)
