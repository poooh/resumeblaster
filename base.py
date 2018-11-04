from flask import Flask, render_template, request
from flaskext.mysql import MySQL
import smtplib
import os
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from datetime import datetime

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


UPLOAD_FOLDER = os.path.basename('/home/pooja/Downloads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/login", methods=['GET', 'POST'])
def login():
    return render_template("login.html")

@app.route("/user_auhentication", methods=['GET'])
def user_auhentication():
    uname = request.args['name']
    uemail = request.args['email']
    uphonenumber = request.args['phonenumber']
    uaddress = request.args['address']
    udob = request.args['dob']
    datetime_object = datetime.strptime(udob, '%M/%d/%Y')
    # conn = mysql.connect()
    # cursor = conn.cursor()
    # query = "INSERT INTO user (username, email, phone, DOB, Address) VALUES ('%s', '%s', '%s', '%s', '%s');"% (uname, uemail, uphonenumber, datetime_object, uaddress)
    # print query
    # cursor.execute(query)
    # conn.commit()
    # conn.close()
    return render_template("index.html")


def send_mail(send_from, send_to, subject, text, files=None):
    # assert isinstance(send_to, list)
    text = "Kindly check my CV"
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))
    fil = open(files, "rb")
    part = MIMEApplication(fil.read(),Name=basename(files))
    # After the file is closed
    part['Content-Disposition'] = 'attachment; filename="%s"' % basename(files)
    # print part
    msg.attach(part)
    # print msg
    print send_to
    smtp = smtplib.SMTP('smtp.gmail.com',587)
    # smtp = smtplib.SMTP("mail.openedoo.org", 465)
    smtp.starttls()
    # server.set_debuglevel(1)
    smtp.login("pujatest1234@gmail.com", "bal@11335")
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()


@app.route("/upload", methods=['GET'])
def upload():
    print request.args
    file = request.args['image']
    filename = os.path.join(app.config['UPLOAD_FOLDER'], file)
    # add your custom code to check that the uploaded file is a valid image and not a malicious file (out-of-scope for this post)
    # print filename
    # import sys
    # sys.exit()
    # file.write(filename)
    return render_template("index.html", filedata = filename)



# send_mail("pujatest1234@gmail.com", 'canak.nene@gmail.com', "resume pooja", text, files='/home/pooja/Downloads/pooja_cv.pdf')

if __name__ == "__main__":
    app.run(debug=True)