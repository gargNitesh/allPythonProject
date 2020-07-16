from flask import Flask, render_template,request,session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from flask_mail import Mail,Message
import mysql.connector
import random



app=Flask(__name__)
app.secret_key="attendence"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/data1'
db = SQLAlchemy(app)

app.config.update(
    DEBUG=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='sy3103yk@gmail.com',
    MAIL_PASSWORD='Sumit@3031#@'
)
mail=Mail(app)

class management1(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Email_ID = db.Column(db.String(100))
    PASSWORD= db.Column(db.String(100))
    OTP= db.Column(db.Integer)

class student(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Roll_NO= db.Column(db.String(100))
    NAME=db.Column(db.String(100))
    EMAIL_ID= db.Column(db.String(100))
    SECTION= db.Column(db.String(100))
    SEMESTER= db.Column(db.String(100))
    MOBILE_NO= db.Column(db.String(100))
    PASSWORD = db.Column(db.String(100))
    present=   db.Column(db.Integer)
    OTP = db.Column(db.Integer)

class attendance(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    SECTION= db.Column(db.String(100))
    PHYSICS=db.Column(db.Integer)
    MATHEMATICS = db.Column(db.Integer)
    CHEMISTRY = db.Column(db.Integer)
    Computer_Programming = db.Column(db.Integer)
    Environmental_Engineering = db.Column(db.Integer)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    database="data1"
    )

@app.route("/")
def index():
    return render_template("management.html")

@app.route("/A")
def index11():
    session['SEC']='A'
    session['SEM'] = '1'
    return render_template("a.html" )

@app.route("/B")
def index16():
    session['SEC']='B'
    session['SEM'] = '1'
    return render_template("a.html" )

@app.route("/C")
def index65():
    session['SEC']='C'
    session['SEM'] = '1'
    return render_template("a.html" )

@app.route("/D")
def index66():
    session['SEC']='D'
    session['SEM'] = '1'
    return render_template("a.html" )


@app.route("/student")
def index1():
    return render_template("slogin.html")

@app.route("/management")
def index2():
    return render_template("managlogin.html")

@app.route("/register")
def index3():
    return render_template("register.html")

@app.route("/1")
def index7():
    session['SEM'] = '1'
    return render_template("1.html")

@app.route("/managlogin",methods=['post'])
def index6():
    ID = request.form.get("ID")
    print("my id is ",ID)
    e = request.form.get("pwd")
    mycursor=mydb.cursor()
    sql="select * from management1 where Email_ID='"+ID+"'"
    mycursor.execute(sql)
    data=mycursor.fetchone()
    print("my data is",data)
    if(e==data[2]):
        return render_template("SEM.html")
    else:
        return render_template("managlogin.html", msg="password invalid")



@app.route("/click",methods=['post','get'])
def index8():
    ROLL=request.form.get('Roll_ID')
    NAME = request.form.get('NAME')
    EMAIL= request.form.get('EMAIL_ID')
    SEC = request.form.get('SECTION')
    SEM = request.form.get('SEMESTER')
    MOB= request.form.get('MOBILE_NO')
    PASS= request.form.get('pwd')
    print(ROLL,NAME,EMAIL,SEC,SEM,MOB,PASS)
    x=student(Roll_NO=ROLL,NAME=NAME,EMAIL_ID=EMAIL,SECTION=SEC,SEMESTER=SEM,MOBILE_NO=MOB,PASSWORD=PASS,present=0,OTP=0)
    db.session.add(x)
    db.session.commit()
    p=student.query.filter_by(Roll_NO=ROLL).first()
    print(p.ID)
    sql=attendance(ID=p.ID,SECTION=p.SECTION,PHYSICS=0,MATHEMATICS=0,CHEMISTRY=0)
    db.session.add(sql)
    db.session.commit()
    return render_template("register.html",msg="register successfully")




@app.route("/forget",methods=['post'])
def index85():
    key=request.form.get('key')
    EMAIL = request.form.get('Email')
    print(key)
    if key == '1':
        print("manager")
        mycursor = mydb.cursor()
        sql = "select * from management1 where Email_ID='" + EMAIL + "'"
        mycursor.execute(sql)
    else:
        mycursor = mydb.cursor()
        sql = "select * from student where EMAIL_ID='" + EMAIL + "'"
        mycursor.execute(sql)
    data = mycursor.fetchone()
    print(data)
    if(not data):
        return render_template("forget.html",msg="emailId not exist",key=key)
    else:
        x=random.randint(1000,10000)
        s=str(x)
        if key == '1' :
            print("hello")
            mycursor = mydb.cursor()
            sql = "update management1 set OTP='"+s+"'where Email_ID='" + EMAIL + "' "
            mycursor.execute(sql)
            mydb.commit()
        else:
            mycursor = mydb.cursor()
            sql = "update student set OTP='" + s + "'where EMAIL_ID='" + EMAIL + "' "
            mycursor.execute(sql)
            mydb.commit()

        msg = Message("hello",
                      sender='sy3103yk@gmail.com',
                      recipients=[EMAIL])
        msg.body="your otp is '"+s+"'"
        mail.send(msg)
        return render_template("Otp.html",email=EMAIL,key=key)


@app.route("/con",methods=['post'])
def index31():
    EMAIL = request.form.get('email')
    Key = request.form.get('key')
    PASSWORD = request.form.get('password')
    if Key == '1' :
        mycursor = mydb.cursor()
        sql = "update management1 set PASSWORD='" + PASSWORD + "'where Email_ID='" + EMAIL + "' "
        mycursor.execute(sql)
        mydb.commit()
    else:
        mycursor = mydb.cursor()
        sql = "update student set PASSWORD='" + PASSWORD + "'where EMAIL_ID='" + EMAIL + "' "
        mycursor.execute(sql)
        mydb.commit()

    return render_template("managlogin.html")





@app.route("/otpverify",methods=['post'])
def index87():
    EMAIL = request.form.get('email')
    OTP=request.form.get('Otp')
    key=request.form.get('key')
    if key == '1' :
        mycursor = mydb.cursor()
        sql = "select * from management1 where Email_ID='" + EMAIL + "'"
        mycursor.execute(sql)
    else:
        mycursor = mydb.cursor()
        sql = "select * from student where EMAIL_ID='" + EMAIL + "'"
        mycursor.execute(sql)
    data = mycursor.fetchone()
    #print(data[0])
    if(not data):
        return render_template("forget.html",key=key)
    else:
        if key == '1' :
            if(data[4] == int(OTP)):
                return render_template("confm.html",email=EMAIL,key=key)
            else:
                return render_template("Otp.html", msg="OTP is invalid", email=EMAIL,key=key)
        else:
            if (data[9] == int(OTP)):
                return render_template("confm.html", email=EMAIL,key=key)
            else:
                return render_template("Otp.html", msg="OTP is invalid", email=EMAIL,key=key)


@app.route("/ForgotPassword")
@app.route("/ForgotPassword")
def index17():
    key=request.args.get('key')
    return render_template("forget.html",key=key)




@app.route("/Physics",methods=['post'])
def index12():
    session['SUB']='PHYSICS'
    session['SEM'] = '1'
    session['SEC'] = 'A'
    sec=session.get('SEC')
    print(sec)
    s=str(0)
    mycursor = mydb.cursor()
    sql="UPDATE student SET present='"+s+"'"
    mycursor.execute(sql)
    mydb.commit()
    details= student.query.filter_by(SECTION=sec)
    print(details)
    present=0
    SEC='A'
    return render_template("pattend.html",d=present,data=details )

@app.route("/present",methods=["post"])
def present():
    id=request.form.get('ID')
    roll=request.form.get('rollNo')
    s=1
    q=str(s)
    print("hello")
    print(id)
    session['SUB'] = 'PHYSICS'
    session['SEM'] = '1'
    session['SEC'] = 'A'
    session['ID']=id
    sec=session.get('SEC')
    print(sec)
    mycursor = mydb.cursor()
    sql = "UPDATE student SET  present='"+q+"' WHERE ID='"+id+"' and  SECTION ='"+sec+"'"
    mycursor.execute(sql)
    mydb.commit()
    sql=("SELECT PHYSICS FROM attendance WHERE ID='"+id+"'")
    mycursor.execute(sql)
    details=mycursor.fetchone()
    p=details[0]
    physics=details[0]+1
    sql="UPDATE attendance SET  PHYSICS={} WHERE ID={}".format(physics,id)
    mycursor.execute(sql)
    mydb.commit()
    details= student.query.filter_by(SECTION=sec).all()
    print(details)
    return render_template("pattend.html", data =details)



@app.route("/Mathematics",methods=['post'])
def index18():
    session['SUB']='MATHEMATICS'
    session['SEM'] = '1'
    session['SEC'] = 'A'
    sec = session.get('SEC')
    print(sec)
    s = str(0)
    mycursor = mydb.cursor()
    sql = "UPDATE student SET present='" + s + "'"
    mycursor.execute(sql)
    mydb.commit()
    details = student.query.filter_by(SECTION=sec)
    print(details)
    present = 0
    SEC = 'A'
    return render_template("pattend1.html", d=present, data=details)


@app.route("/presentMath",methods=["post"])
def presentMath():
    id=request.form.get('ID')
    roll=request.form.get('rollNo')
    s=1
    q=str(s)
    print("hello")
    print(id)
    session['SUB'] = 'MATHEMATICS'
    session['SEM'] = '1'
    session['SEC'] = 'A'
    session['ID']=id
    sec=session.get('SEC')
    print(sec)
    mycursor = mydb.cursor()
    sql = "UPDATE student SET  present='"+q+"' WHERE ID='"+id+"' and  SECTION ='"+sec+"'"
    mycursor.execute(sql)
    mydb.commit()
    sql=("SELECT MATHEMATICS FROM attendance WHERE ID='"+id+"'")
    mycursor.execute(sql)
    details=mycursor.fetchone()
    p=details[0]
    physics=details[0]+1
    sql="UPDATE attendance SET  MATHEMATICS={} WHERE ID={}".format(physics,id)
    mycursor.execute(sql)
    mydb.commit()
    details= student.query.filter_by(SECTION=sec).all()
    print(details)
    return render_template("pattend1.html", data =details)



@app.route("/Chemistry",methods=['post'])
def index19():
    session['SUB']='CHEMISTRY'
    session['SEM'] = '1'
    session['SEC'] = 'A'
    sec = session.get('SEC')
    print(sec)
    s = str(0)
    mycursor = mydb.cursor()
    sql = "UPDATE student SET present='" + s + "'"
    mycursor.execute(sql)
    mydb.commit()
    details = student.query.filter_by(SECTION=sec)
    print(details)
    present = 0
    SEC = 'A'
    return render_template("pattend.html", d=present, data=details)


@app.route("/presentChemistry",methods=["post"])
def presentChemistry():
    id=request.form.get('ID')
    roll=request.form.get('rollNo')
    s=1
    q=str(s)
    print("hello")
    print(id)
    session['SUB'] = 'CHEMISTRY'
    session['SEM'] = '1'
    session['SEC'] = 'A'
    session['ID']=id
    sec=session.get('SEC')
    print(sec)
    mycursor = mydb.cursor()
    sql = "UPDATE student SET  present='"+q+"' WHERE ID='"+id+"' and  SECTION ='"+sec+"'"
    mycursor.execute(sql)
    mydb.commit()
    sql=("SELECT PHYSICS FROM attendance WHERE ID='"+id+"'")
    mycursor.execute(sql)
    details=mycursor.fetchone()
    p=details[0]
    physics=details[0]+1
    sql="UPDATE attendance SET  PHYSICS={} WHERE ID={}".format(physics,id)
    mycursor.execute(sql)
    mydb.commit()
    details= student.query.filter_by(SECTION=sec).all()
    print(details)
    return render_template("pattend.html", data =details)


@app.route("/Computer_Programming",methods=['post'])
def index29():
    session['SUB']='Computer_Programming'
    session['SEM'] = '1'
    session['SEC'] = 'A'
    sec = session.get('SEC')
    print(sec)
    s = str(0)
    mycursor = mydb.cursor()
    sql = "UPDATE student SET present='" + s + "'"
    mycursor.execute(sql)
    mydb.commit()
    details = student.query.filter_by(SECTION=sec)
    print(details)
    present = 0
    SEC = 'A'
    return render_template("pattend.html", d=present, data=details)


@app.route("/presentcomp",methods=["post"])
def presentcomp():
    id=request.form.get('ID')
    roll=request.form.get('rollNo')
    s=1
    q=str(s)
    print("hello")
    print(id)
    session['SUB'] = 'PHYSICS'
    session['SEM'] = '1'
    session['SEC'] = 'A'
    session['ID']=id
    sec=session.get('SEC')
    print(sec)
    mycursor = mydb.cursor()
    sql = "UPDATE student SET  present='"+q+"' WHERE ID='"+id+"' and  SECTION ='"+sec+"'"
    mycursor.execute(sql)
    mydb.commit()
    sql=("SELECT PHYSICS FROM attendance WHERE ID='"+id+"'")
    mycursor.execute(sql)
    details=mycursor.fetchone()
    p=details[0]
    physics=details[0]+1
    sql="UPDATE attendance SET  PHYSICS={} WHERE ID={}".format(physics,id)
    mycursor.execute(sql)
    mydb.commit()
    details= student.query.filter_by(SECTION=sec).all()
    print(details)
    return render_template("pattend.html", data =details)


@app.route("/Environmental_Engineering",methods=['post'])
def index39():
    session['SUB']='Environmental_Engineering'
    session['SEM'] = '1'
    session['SEC'] = 'A'
    sec = session.get('SEC')
    print(sec)
    s = str(0)
    mycursor = mydb.cursor()
    sql = "UPDATE student SET present='" + s + "'"
    mycursor.execute(sql)
    mydb.commit()
    details = student.query.filter_by(SECTION=sec)
    print(details)
    present = 0
    SEC = 'A'
    return render_template("pattend.html", d=present, data=details)


@app.route("/presentenvir",methods=["post"])
def presentenvir():
    id=request.form.get('ID')
    roll=request.form.get('rollNo')
    s=1
    q=str(s)
    print("hello")
    print(id)
    session['SUB'] = 'PHYSICS'
    session['SEM'] = '1'
    session['SEC'] = 'A'
    session['ID']=id
    sec=session.get('SEC')
    print(sec)
    mycursor = mydb.cursor()
    sql = "UPDATE student SET  present='"+q+"' WHERE ID='"+id+"' and  SECTION ='"+sec+"'"
    mycursor.execute(sql)
    mydb.commit()
    sql=("SELECT PHYSICS FROM attendance WHERE ID='"+id+"'")
    mycursor.execute(sql)
    details=mycursor.fetchone()
    p=details[0]
    physics=details[0]+1
    sql="UPDATE attendance SET  PHYSICS={} WHERE ID={}".format(physics,id)
    mycursor.execute(sql)
    mydb.commit()
    details= student.query.filter_by(SECTION=sec).all()
    print(details)
    return render_template("pattend.html", data =details)





@app.route("/click",methods=['post'])
def index5():
    Roll_ID =request.form.get("Roll_ID")
    print(Roll_ID)
    e = request.form.get("pwd")

    x=management1(Roll_ID=Roll_ID,PASSWORD=e)
    db.session.add(x)
    db.session.commit()
    mydb.commit()
    print(e)
    return render_template("slogin.html")
app.run(debug=True)
