from flask import Flask,render_template,request,send_from_directory
import pymysql.cursors
import os
from _datetime import date

drive=Flask(__name__)

images_root=r"E:\User_Folders\\"

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             db='drive',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
mycursor = connection.cursor()

@drive.route("/")
def login():
    return render_template('login.html')

@drive.route("/signup")
def signup():
    return render_template("signup.html")

@drive.route("/login")
def login1():
    email=request.args.get("email")
    password=request.args.get("pass")
    mycursor = connection.cursor()
    sql = "select * from users where user_email='" + email + "'"
    mycursor.execute(sql)
    data = mycursor.fetchone()
    print(data)
    if(data!=None):
        if(data['password']== password):
            user = os.listdir(r"E:\User_Folders\\"+email+"")
            print(user)
            return render_template("main.html",data=email,data1=user)
        else:
            return render_template("login.html",error="Password Incorrect")
    else:
        return render_template("login.html",error="User is not register")


@drive.route("/Forgot_Password")
def Fg_Pass():
    return render_template("Reset_Pass.html")

@drive.route("/Reset",methods=["post"])
def rest():
    email = request.form.get("Email")
    password1 = request.form.get("password")
    print(email,password1)
    mycursor = connection.cursor()
    sql = "select * from users where user_email='" + email + "'"
    mycursor.execute(sql)
    data = mycursor.fetchone()
    print(data)
    if (data is not None):
        mycursor = connection.cursor()
        sql1 = "update users set password='"+ password1 +"' where user_email='" + email + "'"
        mycursor.execute(sql1)
        return render_template("Reset_Pass.html", Error="Password is Reset")
    else:
        return render_template("Reset_Pass.html", Error="Email Not Rergister")



@drive.route("/adduser")
def add():
    name=request.args.get("name")
    email = request.args.get("email")
    password = request.args.get("password")
    date1 = date.today()
    date4 = date1.strftime("%b-%d-%Y")
    today=str(date4)
    print(name,email,password,today)

    mycursor = connection.cursor()
    sql = "select * from users where user_email='" + email + "'"
    mycursor.execute(sql)
    data = mycursor.fetchone()
    if data is not None:
        mycursor.close()
        return render_template("signup.html", error="This email is already registered.")

    else:
        try:
            mycursor = connection.cursor()
            sql = "insert into users(user_name, user_email,password) " \
                    "values('"+name+"','"+email+"','"+password+"');"
            mycursor.execute(sql)
            data = mycursor.fetchall()
            if len(data) is 0:
                connection.commit()
                print('User information saved successfully !')
                os.mkdir(r"E:\User_Folders\\"+email+"")

            else:
                print('error: ', str(data[0]))

        except Exception as e:
            print(e)
        finally:
            mycursor.close()
            connection.close()
    return render_template("login.html")

@drive.route("/upload", methods=["post"])
def upload():
    email=str(request.form.get("email"))
    Select_folder = str(request.form.get("Select_folder"))
    print(email)
    user=os.listdir(r"E:\User_Folders\\")
    print(user)
    for i in user:
        print(i)
        if(email==i):
            targat = os.path.join(r"E:\User_Folders\\"+i+"\\"+Select_folder+"")
            print(targat)

            if not os.path.isdir(targat):
                os.mkdir(targat)

            for file in request.files.getlist("file"):
                print("file")
                filename = file.filename
                destination = "/".join([targat, filename])
                print(destination)
                file.save(destination)
                user1 = os.listdir(r"E:\User_Folders\\" + email + "")


            return render_template("main.html", error="File Upload Successfully", user_image=filename,data=email,data1=user1)
        else:
            continue
            return render_template("main.html", error="File Not Uploaded")



@drive.route("/add_folder")
def add_folder():
    email = request.args.get("email")
    user_Folder_name=request.args.get("user_crt")
    os.mkdir(r"E:\User_Folders\\"+ email +"\\" + user_Folder_name +"")
    user = os.listdir(r"E:\User_Folders\\" + email + "")
    return render_template("main.html",error1="Folder Created",data=email,data1=user)

@drive.route("/Del_Folder", methods=["post"])
def del_folder():
    email = request.form.get("email")
    folder= request.form.get("ID")
    print(email)
    print(folder)
    user = os.listdir(r"E:\User_Folders\\" + email + "")
    print(user)

    return render_template("main.html", data=email, data1=user)

@drive.route('/logout', methods=["post"])
def logout():
    return render_template("login.html")


drive.run()
