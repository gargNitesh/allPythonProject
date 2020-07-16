from flask import *
from flask_mail import Mail, Message
import mysql.connector
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename
from flask import send_from_directory,send_file,safe_join


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    database="bugtracking"
)

app = Flask(__name__)

app.secret_key = 'code planet techno'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/bugtracking'
app.config.update(
    DEBUG=True,
    # EMAIL SETTINGS
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='kumarsatyam128@gmail.com',
    MAIL_PASSWORD='Satyam@1997'
)
mail = Mail(app)
db = SQLAlchemy(app)


class students(db.Model):
    user_id = db.Column(db.Integer(), primary_key=True, nullable=False)
    Name = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(50), unique=True, nullable=False)
    Mob_no = db.Column(db.Integer(), nullable=False)
    Field = db.Column(db.String(50), nullable=False)
    Password = db.Column(db.String(50), nullable=False)
    Reg_date = db.Column(db.String(50), nullable=False)
    verify = db.Column(db.Integer(), nullable=False)


class bug_details(db.Model):
    user_id = db.Column(db.Integer(), nullable=False)
    bug_id = db.Column(db.Integer(), unique=True, nullable=False, primary_key=True)
    Project_Name = db.Column(db.String(80), unique=True)
    Modules = db.Column(db.String(80), unique=False)
    Sub_Modules = db.Column(db.String(120), unique=False)
    Assigned_To = db.Column(db.String(100), unique=False)
    Bug_Title = db.Column(db.String(100), unique=True)
    Bug_Type = db.Column(db.String(100), unique=False)
    Bug_Severity = db.Column(db.String(100), unique=False)
    Bug_Status = db.Column(db.String(100), unique=False)
    Bug_Description = db.Column(db.String(100), unique=False)
    Round = db.Column(db.String(100), unique=False)
    File_Upload = db.Column(db.String(100), unique=False)
    Depends = db.Column(db.String(100), unique=False)


@app.route("/")
def hello():
    session['login'] = False
    session['user_id'] = 0
    session['user_role'] = 0
    return render_template("app.html")


@app.route("/login")
def validation():
    temp_email = None
    email = request.args.get('email')
    passd = request.args.get('passwd')
    print(passd)
    print(email)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT Email FROM students WHERE Email ='" + email + "'")
    temp_email = mycursor.fetchall()
    print(temp_email)
    mycursor.execute("SELECT Password,verify,user_id,Field FROM students  WHERE Email ='" + email + "'")
    result = mycursor.fetchall()
    print(result)
    if temp_email != []:
        if email == temp_email[0][0]:
            if passd == result[0][0]:
                if result[0][1] == 1:
                    session['login'] = True
                    session['user_id'] = result[0][2]
                    session['user_role'] = result[0][3]
                    if session.get('login') == True and session.get('user_role') == "2":
                        return render_template("test.html",approval=bug_details.query.filter_by(Assigned_To=session.get("user_id")).all())
                    elif session.get('login') == True and session.get('user_role') == "1":
                        return render_template("tester.html",data=bug_details.query.filter_by(user_id=session.get("user_id")).all())





                else:
                    print('verify your email')
                    return render_template("test.html", msg="Verify Your Email")
            else:
                print('password does not matched')
                return render_template("app.html", msg="Enter Correct Password")
        else:
            print('email does not exist ,please register first')
            return render_template("app.html")
    else:
        return render_template("app.html", msg="email doesnt exist please register first")




@app.route("/signup")
def sign():
    return render_template("signup.html")


@app.route("/verify")
def veri():
    email = request.args.get('email')
    print(email)
    mycursor = mydb.cursor()
    mycursor.execute("UPDATE students SET verify =1 WHERE Email =email")
    mydb.commit()
    return email


@app.route("/fpassword")
def reset():
    return render_template("fpassword.html")


@app.route("/reset_password",methods=['post'])
def forgetpassword():
    email=request.form.get("email")
    print(email)
    msg = Message('Reset Password', sender='kumarsatyam128@gmail.com', recipients=[email])
    msg.html = render_template('preset.html', email=email)
    mail.send(msg)

    return render_template("app.html",msg="check your mail to reset password")

@app.route("/preset",methods=['get','post'])
def preset():
    return render_template("reset.html")


@app.route("/reset",methods=['post'])
def pass_uptade():
    email = request.form.get('email')
    pswd=request.form.get('password')
    print(email)
    print(pswd)
    mycursor = mydb.cursor()
    mycursor.execute(" UPDATE students SET Password =' "+ pswd +" ' WHERE Email ='" + email + "'")
    mydb.commit()
    return render_template("app.html",msg="password successfully reset")


@app.route("/signedup", methods=["POST", "GET"])
def signedup():
    Name = request.form.get('Name')
    email = request.form.get('email')
    mob_no = request.form.get('mob_no')
    field = request.form.get('Field')
    pswd = request.form.get('passwd')
    mycursor = mydb.cursor()
    sql = "SELECT Email FROM students WHERE Email='" + email + "'"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    print(result)
    print(email)
    # reg_date=request.form.get('reg_date')
    print(Name, email, mob_no, field, pswd)
    if result==[] :
        entry = students(Name=Name, Email=email, Mob_no=mob_no, Field=field, Password=pswd)
        db.session.add(entry)
        db.session.commit()
        msg = Message('Hello', sender='kumarsatyam128@gmail.com', recipients=[email])
        msg.html = render_template('about.html', email=email)
        mail.send(msg)

        return render_template("signedup.html")



    else:
        return render_template("signup.html", name=Name,mob=mob_no,field=field, msg="email already registered please try other email")


@app.route("/bug")
def test():
    result=students.query.filter_by(Field='2').all()
    print(result)
    return render_template("bug.html",data=result)


@app.route("/Issue",methods=["POST"])
def issue():
    bugId=request.form.get('bug_no')
    print(bugId)
    details=bug_details.query.filter_by(bug_id=bugId).first()
    print(details)
    return render_template('issue.html',detail=details)




@app.route("/bug_entry", methods=["POST", "GET"])
def bug_entry():
    uid=session.get("user_id")
    projectName = request.form.get('projectName')
    Modules = request.form.get('moduleId')
    Sub_Modules = request.form.get('subModuleId')
    Assigned_To = request.form.get('assignTo')
    Bug_Title = request.form.get('bugName')
    Bug_Type = request.form.get('BugType')
    Bug_Severity = request.form.get('bugSeverity')
    Bug_Status = request.form.get('bugStatus')
    Bug_Description = request.form.get('BugDescription')
    Round = request.form.get('round')
    File_Uploads = request.form.get('FileData')
    Depends = request.form.get('depends')
    if request.method =="POST":
        file=request.files['FileData']
        for i in range(1,uid+1):
            if i==uid:         #creating folder to save files
                os.makedirs(os.path.join(app.instance_path,'user_ID'+str(i)),exist_ok=True)
                file.save(os.path.join(app.instance_path,'user_ID'+str(i),secure_filename(file.filename)))

    entry = bug_details(user_id=uid,Project_Name=projectName, Modules=Modules, Sub_Modules=Sub_Modules, Assigned_To=Assigned_To,
                        Bug_Title=Bug_Title, Bug_Type=Bug_Type, Bug_Severity=Bug_Severity, Bug_Status=Bug_Status,
                        Bug_Description=Bug_Description, Round=Round, File_Upload=file.filename, Depends=Depends)
    print(projectName)
    db.session.add(entry)
    db.session.commit()

    return render_template("tester.html",data=bug_details.query.filter_by(user_id=uid).all())


@app.route('/download',methods=["post","GET"])
def download():
    bugid=request.form.get('bug_no')
    print(bugid)
    for i in range(1,session.get('user_id')+1):
        if i==session.get('user_id'):
            b=db.session.query(bug_details.File_Upload).filter_by(bug_id=bugid).first()
            print(b)
            p=(os.path.abspath("instance/user_id"+str(i)))
            return send_file(filename_or_fp=safe_join(p,b[0]),as_attachment=True,  attachment_filename=b[0])

@app.route('/edit',methods=['post'])
def edit():
    bugid=request.form.get('bug_no')

    details=bug_details.query.filter_by(bug_id=bugid).first()
    print(details)
    return render_template('editbug.html',detail=details)

@app.route('/update',methods=['post'])
def update():
    bugid= request.form.get('bugId')
    print("hghghgdfh"+bugid)
    projectName = request.form.get('projectName')
    Modules = request.form.get('moduleId')
    Sub_Modules = request.form.get('subModuleId')
    Assigned_To = request.form.get('assignTo')
    Bug_Title = request.form.get('bugName')
    Bug_Type = request.form.get('BugType')
    Bug_Severity = request.form.get('bugSeverity')
    Bug_Status = request.form.get('bugStatus')
    Bug_Description = request.form.get('BugDescription')
    Round = request.form.get('round')
    File_Uploads = request.form.get('FileData')
    Depends = request.form.get('depends')
    update= bug_details.query.filter_by(bug_id=bugid).update( dict(Project_Name=projectName, Modules=Modules, Sub_Modules=Sub_Modules,
                        Assigned_To=Assigned_To,
                        Bug_Title=Bug_Title, Bug_Type=Bug_Type, Bug_Severity=Bug_Severity, Bug_Status=Bug_Status,
                        Bug_Description=Bug_Description, Round=Round, File_Upload=File_Uploads, Depends=Depends))

    db.session.commit()
    return redirect(url_for('validation') )


app.run(debug=True)
