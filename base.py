from flask import Flask, render_template, request
from flaskext.mysql import MySQL
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

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


@app.route("/")
def login():
	# print request.args
    return render_template("login.html")


def user_auhentication():
    return


def send_mail(send_from, send_to, subject, text, files=None):
    # assert isinstance(send_to, list)

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


text = "Kindly check my CV"
send_mail("pujatest1234@gmail.com", 'canak.nene@gmail.com', "resume pooja", text, files='/home/pooja/Downloads/pooja_cv.pdf')

if __name__ == "__main__":
    app.run(debug=True)