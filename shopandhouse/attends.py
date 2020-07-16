import pymysql
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail,Message
import mysql.connector
import random


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  database="test"
)

app = Flask(__name__)
app.secret_key = "test"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost/test"
db = SQLAlchemy(app)

app.config.update(
    DEBUG=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='',
    MAIL_PASSWORD=''
)
mail=Mail(app)

class user_details(db.Model):
    uid=db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80),nullable=True)
    email = db.Column(db.String(120),nullable=True)
    password = db.Column(db.String(120),nullable=True)
    otp = db.Column(db.String(5),nullable=True)


class house(db.Model):
    hid = db.Column(db.Integer, primary_key=True)
    property=db.Column(db.String(50),nullable=True)
    size = db.Column(db.Integer,nullable=True)
    location1 = db.Column(db.String(50),nullable=True)
    location2 = db.Column(db.String(50), nullable=True)
    location3 = db.Column(db.String(50), nullable=True)
    location4 = db.Column(db.String(50), nullable=True)
    name = db.Column(db.String(50), nullable=True)
    contact = db.Column(db.String(50), nullable=True)
    price = db.Column(db.String(50), nullable=True)


app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'panpatidar180@gmail.com',
	MAIL_PASSWORD = 'patel@98'
	)

mail=Mail(app)



@app.route("/")
def index():
    return render_template("login1.html")

@app.route("/registerSign",methods=['post'])
def registerSign():
    name=request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('pwd')
    entry = user_details(name=name, email=email, password=password, otp=0)
    db.session.add(entry)
    db.session.commit()
    return render_template("login1.html")


@app.route("/login1",methods=['post'])
def index5():
    email = request.form.get("email")
    password= request.form.get("password")
    print(password)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM user_details WHERE email='"+email+"'")

    p = mycursor.fetchone()

    if(p is not None):
        if (password==p[3]):
            if(p[4]==0):
                return render_template("house.html")
            else:
                return render_template("admin.html")
        else:
            return render_template("login1.html",msg="invalid password")
    else:
        return render_template("login1.html", msg="email is not exist")




'''@app.route("/hello",methods=['post'])
def h():
   return render_template("house2.html")'''

'''@app.route("/hello2",methods=['post'])
def hello2():
   return render_template("shop.html")'''

@app.route("/signUp")
def signUp():
    return render_template("register.html")

@app.route("/register", methods=['post'])
def hello2():
    return render_template("login1.html")


@app.route("/login3",methods=['post'])
def login3():
    return render_template("house2.html")

@app.route("/required",methods=['post'])
def required():
    property=request.form.get("property")
    size=request.form.get("size")
    sarea=request.form.get("sclarea")
    harea = request.form.get("harea")
    barea = request.form.get("barea")
    rarea = request.form.get("rarea")
    if(sarea is None):
        sarea="null"
    if (harea is None):
        harea = "null"
    if (barea is None):
        barea = "null"
    if (rarea is None):
        rarea = "null"
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM house WHERE ((property='" + property + "' and size='" + size + "') and (location1='" + sarea + "'or location2='" + harea + "' or location3='" + barea + "' or location4='" + rarea + "'))  " )

    p = mycursor.fetchall()
    print(p)
    return render_template("view.html",list=p)

@app.route("/details",methods=['post'])
def details():
    property = request.form.get("property")
    size = request.form.get("size")
    sarea = request.form.get("sclarea")
    harea = request.form.get("harea")
    barea = request.form.get("barea")
    rarea = request.form.get("rarea")
    owner_name = request.form.get("name")
    contact = request.form.get("contact")
    price = request.form.get("price")
    if (sarea is None):
        sarea = "null"
    if (harea is None):
        harea = "null"
    if (barea is None):
        barea = "null"
    if (rarea is None):
        rarea = "null"
    entry = house(property=property, size=size, location1=sarea, location2=harea, location3=barea, location4=rarea,name=owner_name,contact=contact,price=price)
    db.session.add(entry)
    db.session.commit()
    print(harea, sarea, barea, rarea, property, size, owner_name, contact, price)
    return render_template("view.html")


@app.route("/register.html",methods=['post','get'])
def register():

    user_name=request.form.get('name')
    email = request.form.get('email')
    pwd = request.form.get('pwd')
    print(user_name,pwd,email)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM user_details WHERE email='"+email+"'" )

    p=mycursor.fetchone()
    print (p)
    if email==p[2]:
        return render_template("register.html",msg="mail already exists")

    else:
        entry=user_details(name=user_name,email=email,password=pwd)
        db.session.add(entry)
        db.session.commit()
        return render_template("login1.html",msg='registered successfully')

'''@app.route("/h",methods=['post'])
def h():
    return render_template("prop.html")'''

@app.route("/s",methods=['post'])
def s():
       return render_template("house2.html")

'''@app.route("/")
def register():
    return render_template("register.html")'''



@app.route("/a",methods=['post'])
def a():
       return render_template("shop2.html")

'''@app.route("/b",methods=['post'])
def b():
       return render_template("view.html")'''


@app.route("/forget",methods=['post'])
def index85():
    EMAIL = request.form.get('email')
    mycursor = mydb.cursor()
    sql = "select * from user_details where email='" + EMAIL + "'"
    mycursor.execute(sql)
    data = mycursor.fetchone()
    print(data)
    if(not data):
        return render_template("Forgot.html",msg="emailId not exist")
    else:
        x=random.randint(1000,10000)
        s=str(x)
        mycursor = mydb.cursor()
        sql = "update user_details set otp='"+s+"'where email='" + EMAIL + "' "
        mycursor.execute(sql)
        mydb.commit()

        msg = Message("hello",
                      sender='panpatidar180@gmail.com',
                      recipients=[EMAIL])
        msg.body="your otp is '"+s+"'"
        mail.send(msg)
        return render_template("Otp.html",email=EMAIL)


@app.route("/con",methods=['post'])
def index31():
    EMAIL = request.form.get('email')
    PASSWORD = request.form.get('password')
    mycursor = mydb.cursor()
    sql = "update user_details set password='" + PASSWORD + "'where email='" + EMAIL + "' "
    mycursor.execute(sql)
    mydb.commit()
    return render_template("login1.html")





@app.route("/otpverify",methods=['post'])
def index87():
    EMAIL = request.form.get('email')
    OTP=request.form.get('Otp')
    mycursor = mydb.cursor()
    sql = "select * from user_details where email='" + EMAIL + "'"
    mycursor.execute(sql)
    data = mycursor.fetchone()
    if(not data):
        return render_template("Forgot.html")
    else:
        if(data[5] == int(OTP)):
            return render_template("confm.html",email=EMAIL)
        else:
            return render_template("Otp.html", msg="OTP is invalid", email=EMAIL)

@app.route("/ForgotPassword")
def index17():
    return render_template("Forgot.html")



app.run(debug=True)





