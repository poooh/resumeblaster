from flask import Flask
from flask import Flask, render_template
from flaskext.mysql import MySQL
import pymysql
import MySQLdb

app = Flask(__name__)
# @app.route("/")

mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'poojaroot'
app.config['MYSQL_DATABASE_PASSWORD'] = '1604@Baba'
app.config['MYSQL_DATABASE_DB'] = 'resumeblaster'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


def create_table():
	conn = mysql.connect()
	cursor = conn.cursor()
	query = "CREATE TABLE IF NOT EXISTS user (user_id INT AUTO_INCREMENT, username VARCHAR(255) \
    	NOT NULL, email VARCHAR(255) NOT NULL, phone INT(255) NOT NULL, DOB DATETIME NOT NULL, \
    	Address TEXT NOT NULL, PRIMARY KEY (user_id))  ENGINE=INNODB;"
	cursor.execute(query)
	conn.commit()
	conn.close()
	return


create_table()
# conn = mysql.connect()
# cursor = conn.cursor()
# cursor = mysql.get_db().cursor()


@app.route("/")
def login():
    return render_template("login.html")


def user_auhentication():
    return


if __name__ == "__main__":
    app.run(debug=True)