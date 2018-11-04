from flask import Flask, render_template, request
from flaskext.mysql import MySQL
import flask
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
app.config['MYSQL_DATABASE_USER'] = 'jsa56'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Rn9inVya'
app.config['MYSQL_DATABASE_DB'] = 'resumeblaster'
app.config['MYSQL_DATABASE_HOST'] = 'sql.njit.edu'
mysql.init_app(app)

def create_table():
	conn = mysql.connect()
	cursor = conn.cursor()
	query1 = "CREATE TABLE IF NOT EXISTS user (user_id INT AUTO_INCREMENT, username VARCHAR(255) \
     	NOT NULL, email VARCHAR(255) NOT NULL, phone INT(255) NOT NULL, DOB DATETIME NOT NULL, \
     	Address TEXT NOT NULL, PRIMARY KEY (user_id))  ENGINE=INNODB;"
	cursor.execute(query1)
	query2 = "CREATE TABLE IF NOT EXISTS companies (comp_id INT AUTO_INCREMENT, \
     compname VARCHAR(255) NOT NULL, compemail VARCHAR(255) NOT NULL,   FOREIGN KEY user_id REFERENCES \
     user(user_id) ON UPDATE CASCADE ON DELETE RESTRICT, PRIMARY KEY (comp_id))  ENGINE=INNODB;"
	cursor.execute(quer2)
	conn.commit()
	conn.close()
	return

create_table()


UPLOAD_FOLDER = os.path.basename('/home/pooja/Documents/resumeblaster')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/login", methods=['GET', 'POST'])
def login():
    return render_template("login.html")

@app.route("/user_auhentication", methods=['GET'])
def user_auhentication():
    # sessiondata = requests.session()
    uname = request.args['name']
    uemail = request.args['email']
    uphonenumber = request.args['phonenumber']
    uaddress = request.args['address']
    udob = request.args['dob']
    datetime_object = datetime.strptime(udob, '%M/%d/%Y')
    conn = mysql.connect()
    cursor = conn.cursor()
    query = "select * from user where email = '%s';"% (uemail)
    result = cursor.execute(query)
    if(result):
        return render_template("login.html", error = "email already exists")
    else:
        query1 = "INSERT INTO user (username, email, phone, DOB, Address) VALUES ('%s', '%s', '%s', '%s', '%s');"% (uname, uemail, uphonenumber, datetime_object, uaddress)
        cursor.execute(query1)
        query2 = "select * from user where email = '%s';"% (uemail)
        cursor.execute(query2)
        resultset = cursor.fetchone ()
        conn.commit()
        conn.close()
        resp = flask.make_response(render_template("uploadfile.html"))
        resp.set_cookie('email', uemail)
        resp.set_cookie('uname', uname)
        resp.set_cookie('user_id', bytes(resultset[0]))
        return resp

@app.route("/send_mail", methods=['GET'])
def send_mail():
    # assert isinstance(send_to, list)
    send_from = request.cookies.get('email')
    filedata = request.cookies.get('filedata')
    username = request.cookies.get('uname')
    send_to = 'canak.nene@gmail.com'
    subject = "Resume %s"%username
    files = '/home/pooja/Documents/resumeblaster/%s'%(filedata)
    text = "Khttp://127.0.0.1:5000/indly check my CV"
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
    msg.attach(part)
    smtp = smtplib.SMTP('smtp.gmail.com',587)
    smtp.starttls()
    smtp.login(send_from, "bal@11335")
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()
    return render_template("thankyou.html")


@app.route("/upload", methods=['GET'])
def upload():

    file = request.args['file']

    with open('/home/pooja/Downloads/%s'%(file), 'r') as theFile:
        file = theFile.read()

    filedata = request.args['file']
    with open('/home/pooja/Documents/resumeblaster/%s'%(filedata), 'w') as file_data:
        file_data.write(file)
    file = request.args['file']
    resp = flask.make_response(render_template("uploadfile.html", filedata = file))
    resp.set_cookie('filedata', file)
    return resp


@app.route("/companies", methods=['GET'])
def companies():
    conn = mysql.connect()
    cursor = conn.cursor()
    compenamelist = []
    compemaillist = []
    uid = request.cookies.get('user_id')
    index = len(request.args) / 2
    for i in range(index):
        query = "select * from companies where compemail = '%s';"% (request.args['compemail%s'%(i)])
        result = cursor.execute(query)
        if(result):
            return render_template("uploadfile.html", error = "company email already exists")
        else:
            compenamelist.append(request.args['company%s'%(i)])
            compenamelist.append(request.args['compemail%s'%(i)])
            queryinsert = "INSERT INTO companies (compname, compemail, user_id) VALUES ('%s', '%s', '%s');"% (request.args['company%s'%(i)], request.args['compemail%s'%(i)], uid)
            cursor.execute(queryinsert)
    conn.commit()
    conn.close()
    return render_template("uploadfile.html", compenamelist = compenamelist, compemaillist = compemaillist)

# send_mail("pujatest1234@gmail.com", 'canak.nene@gmail.com', "resume pooja", text, files='/home/pooja/Downloads/pooja_cv.pdf')

if __name__ == "__main__":
    app.run(debug=True)