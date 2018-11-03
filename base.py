from flask import Flask
from flask import Flask, render_template

app = Flask(__name__)
# @app.route("/")

@app.route("/")
def login():
    return render_template("login.html")

# def home():
#     return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True)