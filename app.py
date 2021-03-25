from database import get_db, query_db, make_dicts, close_db, convert_dict
from flask import Flask, render_template,  request, g, current_app, flash, redirect, url_for
import sqlite3 as sql



app = Flask(__name__)

'''
Page Rendering: 
The code below this (but above the backend) will handle the rendering of pages that students and teachers interact with. 
These pages will be connected to the backend where the backend does the SQL queries as well as adding new values etc.
'''
@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/new_student_acct')
def create_student_page():
    return render_template('student_creation.html')

@app.route('/student_log_in_page')
def log_in_student():
    return render_template('student_log_in.html')

@app.route('/new_instructor_acct')
def create_instructor_page():
    return render_template('instructor_creation.html')

@app.route('/instructor_log_in')
def log_in_instructor():
    return render_template('instructor_log_in.html')

@app.route('/syllabus')
def syllabus():
    return render_template('syllabus.html')

@app.route('/assignments')
def assignments():
    assignments = query_db('SELECT * FROM Assignments;')
    info = convert_dict(assignments)
    return render_template('assignments.html', info=info);

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

@app.route('/studentmarks')
def studentMarks():
    return render_template('studentmarks.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')
    
'''
Back End:
Front end uses this for data processing
'''

@app.route('/create_student_user')
def create_student_user():    
    username = request.args.get('username')
    password = request.args.get('password')
    firstName = request.args.get('firstName')
    lastName = request.args.get('lastName')
    studentNo = request.args.get('studentNo')

    sid = query_db('SELECT MAX(s.id) FROM StudentUsers s;')[0][0] + 1

    if not query_db("SELECT s.username FROM StudentUsers s WHERE s.username='{}';".format(username)) and not query_db("SELECT s.studentNo FROM StudentUsers s WHERE s.studentNo='{}';".format(studentNo)):            
        with sql.connect("./database.db") as con:
            cur = con.cursor()
            cur.execute("Insert INTO StudentUsers VALUES (?,?,?,?,?,?);", (sid, username, password, firstName, lastName, studentNo))
        return redirect(url_for('home'))
    flash("There is already an account with those credentials!")
    return redirect("/new_student_acct") 

@app.route('/create_instructor_user')
def create_isntructor_user():    
    username = request.args.get('username')
    password = request.args.get('password')
    firstName = request.args.get('firstName')
    lastName = request.args.get('lastName')
    instructorNo = request.args.get('instructorNo')

    sid = query_db('SELECT MAX(s.id) FROM InstructorUsers s;')[0][0] + 1

    if not query_db("SELECT s.username FROM InstructorUsers s WHERE s.username='{}';".format(username)) and not query_db("SELECT s.instructorNo FROM InstructorUsers s WHERE s.instructorNo='{}';".format(instructorNo)):            
        with sql.connect("./database.db") as con:
            cur = con.cursor()
            cur.execute("Insert INTO InstructorUsers VALUES (?,?,?,?,?,?);", (sid, username, password, firstName, lastName, instructorNo))
        return redirect(url_for('home'))
    flash("There is already an account with those credentials!")
    return redirect("/new_instructor_acct")    

@app.route('/verify_student_user')
def verify_student_user():
    username = request.args.get('username')
    password = request.args.get('password')

    if query_db("SELECT s.username FROM StudentUsers s WHERE s.username='{}';".format(username)):
        if query_db("SELECT s.password FROM StudentUsers s WHERE s.username='{}';".format(username))[0][0] == password:
            flash('Log In Sucessful')
            return redirect(url_for('home'))
    flash('Invalid Credentials, please try again or create new account')
    return redirect('/student_log_in_page')

@app.route('/verify_instructor_user')
def verify_instructor_user():
    username = request.args.get('username')
    password = request.args.get('password')

    if query_db("SELECT s.username FROM InstructorUsers s WHERE s.username='{}';".format(username)):
        if query_db("SELECT s.password FROM InstructorUsers s WHERE s.username='{}';".format(username))[0][0] == password:
            flash('Log In Sucessful')
            return render_template('instructor_home.html')
    flash('Invalid Credentials, please try again or create new account')
    return redirect('/instructor_log_in')


@app.route('/create_assignment')
def create_new_assignemnt():    
    pdf = request.args.get('pdf')
    tex = request.args.get('tex')
    dueDate = request.args.get('dueDate')
    weight = request.args.get('weight')
    assignmentDescription = request.args.get('assignmentDescription')

    aid = query_db('SELECT MAX(a.id) FROM Assignments a;')[0][0] + 1

    if not query_db("SELECT a.description FROM Assignments a WHERE a.description='{}';".format(assignmentDescription)):            
        with sql.connect("./database.db") as con:
            cur = con.cursor()
            cur.execute("Insert INTO Assignments VALUES (?,?,?,?,?,?);", (aid, pdf, tex, dueDate, weight, assignmentDescription))
        return render_template('admin.html')
    flash("There is already an assignment with that description!")
    return redirect("/admin")   

'''
Database closing
'''
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == "__main__":
    app.secret_key = 'VyC74LX3hb'
    app.run(debug=True)