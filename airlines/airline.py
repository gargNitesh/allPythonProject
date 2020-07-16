from flask import Flask,render_template,request
from flask_sqlalchemy import *
from flask_mail import Mail,Message
import mysql.connector
import random

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/application'
db = SQLAlchemy(app)
mydb = mysql.connector.connect(host="localhost",user="root",database="application")

app.config.update(
    DEBUG=True,
    #EMAIL SETTING
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='jatinyadav605@gmail.com',
    MAIL_PASSWORD='jatin@605'
)


mail = Mail(app)

class userdetails(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name= db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    otp = db.Column(db.Integer)

class flight_details(db.Model):
    Flightid = db.Column(db.Integer, primary_key=True)
    Flight_name = db.Column(db.String(50))
    Flight_From = db.Column(db.String(50))
    Flight_To = db.Column(db.String(50))
    Deperature = db.Column(db.DateTime)
    Arrival = db.Column(db.DateTime)
    Classtype = db.Column(db.String(50))
    Seats_available= db.column(db.Integer)


@app.route("/")
def index():
    return render_template("index.html")

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/signup')
def signup():
    name=request.args.get('name')
    email=request.args.get('email')
    password=request.args.get('psw')
    print(name+email+password)
    entry=userdetails(name=name,email=email,password=password)
    db.session.add(entry)
    db.session.commit()
    return render_template("null")
@app.route('/searching')
def searching():
    #Flightid=request.args.get('Flightid')
    #Flightname=request.args.get('Flightname')
    Flight_Name = request.args.get('Flight_Name')
    Flight_From=request.args.get('Flight_from')
    Flight_To = request.args.get('Flight_to')
    Deperature = request.args.get('Deperature')
    Arrival = request.args.get('Arrival')
    Classtype = request.args.get('Classtype')
    Seats = request.args.get('Seats')
    print(Flight_From,Flight_To,Deperature,Arrival,Classtype,Seats)

    entry=flight_details(Flight_name =Flight_Name,Flight_From=Flight_From, Flight_To=Flight_To, Deperature= Deperature, Arrival=Arrival,Classtype=Classtype,Seats_available= Seats)
    db.session.add(entry)
    db.session.commit()
    return render_template("airline.html")


@app.route('/login',methods=['post'])
def login():
    email=request.form.get('email')
    password=request.form.get('psw')
    print(email+password)
    mycursor = mydb.cursor()
    sql = "select * from userdetails where email='" + email + "'"
    mycursor.execute(sql)
    data = mycursor.fetchone()
    if(not data):
        return render_template("index.html",msg="email not exist")
    else:
        if(data[3]==password):
            return render_template("airline.html")
        else:
            return render_template("index.html", msg="password not matched")


@app.route("/forget",methods=['post'])
def index85():
    EMAIL = request.form.get('email')
    print(EMAIL)
    mycursor = mydb.cursor()
    sql = "select * from userdetails where email='" + EMAIL + "'"
    mycursor.execute(sql)
    data = mycursor.fetchone()
    print(data)
    if(not data):
        return render_template("Forgot.html",msg="emailId not exist")
    else:
        x=random.randint(1000,10000)
        s=str(x)
        mycursor = mydb.cursor()
        sql = "update userdetails set otp='"+s+"'where email='" + EMAIL + "' "
        mycursor.execute(sql)
        mydb.commit()

        msg = Message("hello",
                      sender='jatinyadav605@gmail.com',
                      recipients=[EMAIL])
        msg.body="your otp is '"+s+"'"
        mail.send(msg)
        return render_template("Otp.html",email=EMAIL)


@app.route("/con",methods=['post'])
def index31():
    EMAIL = request.form.get('email')
    PASSWORD = request.form.get('password')
    mycursor = mydb.cursor()
    sql = "update userdetails set password='" + PASSWORD + "'where email='" + EMAIL + "' "
    mycursor.execute(sql)
    mydb.commit()
    return render_template("index.html")





@app.route("/otpverify",methods=['post'])
def index87():
    EMAIL = request.form.get('email')
    OTP=request.form.get('Otp')
    mycursor = mydb.cursor()
    sql = "select * from userdetails where email='" + EMAIL + "'"
    mycursor.execute(sql)
    data = mycursor.fetchone()
    if(not data):
        return render_template("Forgot.html")
    else:
        if(data[4] == int(OTP)):
            return render_template("confm.html",email=EMAIL)
        else:
            return render_template("Otp.html", msg="OTP is invalid", email=EMAIL)

@app.route("/ForgotPassword")
def index17():
    return render_template("Forgot.html")
@app.route("/signin")
def signin():
    return render_template("index.html")


app.run()