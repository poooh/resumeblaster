from flask import Flask
from flask import Flask, render_template

app = Flask(__name__)
# @app.route("/")

mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '1604baba'
app.config['MYSQL_DATABASE_DB'] = 'resumeblaster'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

create_table()
# conn = mysql.connect()
# cursor = conn.cursor()


@app.route("/")
def login():
    return render_template("login.html")

# def home():
#     return "Hello, World!"

def create_table():
	conn = mysql.connect()
	cursor = conn.cursor()
    # cursor = mysql.get_db().cursor()
    query = "CREATE TABLE IF NOT EXISTS user (user_id INT AUTO_INCREMENT, username VARCHAR(255) NOT NULL, email VARCHAR(255) NOT NULL, phone INT(255) NOT NULL, DOB DATETIME NOT NULL, Address TEXT NOT NULL, PRIMARY KEY (user_id))  ENGINE=INNODB;"
    cursor.execute(query)
    conn.commit()
    conn.close()
    return


def user_auhentication():
    return


if __name__ == "__main__":
    app.run(debug=True)