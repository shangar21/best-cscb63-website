from database import get_db, query_db, make_dicts, close_db, convert_dict
from flask import Flask, render_template,  request, g, current_app, flash, redirect, url_for
import sqlite3 as sql



app = Flask(__name__)
instructor = False
user = ''

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
    global instructor
    global user
    syllabus = query_db('SELECT * FROM Syllabus;')
    info = convert_dict(syllabus, 0)
    for key in info:
       for i in range(len(info[key])):
           info[key][i] = info[key][i].split(",")
    
    return render_template('syllabus.html', user=user, instructor=instructor, info=info)

@app.route('/labs')
def labs():
    global instructor
    global user
    syllabus = query_db('SELECT * FROM Labs;')
    info = convert_dict(syllabus, 0)
    for key in info:
       for i in range(len(info[key])):
           info[key][i] = info[key][i].split(",")
    
    return render_template('labs.html', user=user, instructor=instructor, info=info)

@app.route('/assignments')
def assignments():
    global instructor
    global user 
    assignments = query_db('SELECT * FROM Assignments;')
    info = convert_dict(assignments, 0)
    return render_template('assignments.html', user=user, instructor=instructor, info=info);

@app.route('/home')
def home():
    global instructor
    global user
    return render_template('home.html', user=user, instructor=instructor)

@app.route('/calendar')
def calendar():
    global instructor
    global user
    return render_template('calendar.html', user=user, instructor=instructor)

@app.route('/dashboard')
def admin():
    global instructor
    global user
    assignment_grades = query_db('SELECT * FROM AssignmentGrades')
    info = convert_dict(assignment_grades, 1)
    return render_template('dashboard.html', user=user, instructor=instructor, info=info)

@app.route('/logout')
def log_out():
    global user
    global instructor
    user = ''
    instructor = False
    return redirect('/')
    
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
        with sql.connect("database.db") as con:
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
        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("Insert INTO InstructorUsers VALUES (?,?,?,?,?,?);", (sid, username, password, firstName, lastName, instructorNo))
        return redirect(url_for('home'))
    flash("There is already an account with those credentials!")
    return redirect("/new_instructor_acct")    

@app.route('/verify_student_user')
def verify_student_user():
    global user
    username = request.args.get('username')
    password = request.args.get('password')

    if query_db("SELECT s.username FROM StudentUsers s WHERE s.username='{}';".format(username)):
        if query_db("SELECT s.password FROM StudentUsers s WHERE s.username='{}';".format(username))[0][0] == password:
            flash('Log In Sucessful')
            user = username
            return redirect(url_for('home'))
    flash('Invalid Credentials, please try again or create new account')
    return redirect('/student_log_in_page')

@app.route('/verify_instructor_user')
def verify_instructor_user():
    global user
    global instructor
    username = request.args.get('username')
    password = request.args.get('password')

    if query_db("SELECT s.username FROM InstructorUsers s WHERE s.username='{}';".format(username)):
        if query_db("SELECT s.password FROM InstructorUsers s WHERE s.username='{}';".format(username))[0][0] == password:
            flash('Log In Sucessful')
            user = username
            instructor = True 
            return redirect('/home')
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
        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("Insert INTO Assignments VALUES (?,?,?,?,?,?);", (aid, pdf, tex, dueDate, weight, assignmentDescription))
        flash("Assignment Successfully added!")
        return redirect('/dashboard')
    flash("There is already an assignment with that description!")
    return redirect("/dashboard")   

@app.route('/add_to_syllabus')
def add_to_syllabus():
    topic = request.args.get('topic')    
    wed_pre_lec = request.args.get('wed_pre_lec')
    wed_pre_lec_labels = request.args.get('wed_pre_lec_labels')
    thurs_pre_lec = request.args.get('thurs_pre_lec')
    thurs_pre_lec_labels = request.args.get('thurs_pre_lec_labels')
    wed_lec = request.args.get('wed_lec')
    wed_lec_labels = request.args.get('wed_lec_labels')
    thurs_lec = request.args.get('thurs_lec')
    thurs_lec_labels = request.args.get('thurs_lec_labels')

    sid = query_db('SELECT MAX(s.id) FROM Syllabus s;')[0][0] + 1

    if not query_db("SELECT s.topic FROM Syllabus s WHERE s.topic='{}';".format(topic)):            
        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("Insert INTO Syllabus VALUES (?,?,?,?,?,?,?,?,?,?);", (sid, topic, wed_pre_lec, wed_pre_lec_labels, thurs_pre_lec, thurs_pre_lec_labels, wed_lec, wed_lec_labels, thurs_lec, thurs_lec_labels))
        flash("Sucessfully added to syllabus!")
        return redirect('/dashboard')
    flash("There is already an assignment with that description!")
    return redirect("/dashboard")   

@app.route('/add_to_labs')
def add_to_labs():
    topic = request.args.get('topic')    
    handout = request.args.get('handout')
    handout_label = request.args.get('handout_label')
    solutions = request.args.get('solutions')
    solutions_label = request.args.get('solutions_label')

    lid = query_db('SELECT MAX(l.id) FROM Labs l;')[0][0] + 1

    if not query_db("SELECT s.topic FROM Labs s WHERE s.topic='{}';".format(topic)):            
        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("Insert INTO Syllabus VALUES (?,?,?,?,?,?);", (lid, topic, handout, handout_label, solutions, solutions_label))
        flash("Successfully added to Labs!")
        return redirect('/dashboard')
    flash("There is already an assignment with that description!")
    return redirect("/dashboard")

@app.route('/update_student_grade')
def update_student_grade():
    aid = request.args.get('aid')
    username = request.args.get('username')
    grade = request.args.get('grade')

    if query_db("SELECT s.username FROM StudentUsers s WHERE s.username='{}';".format(username)) and query_db('SELECT a.id FROM Assignments a WHERE a.id={};'.format(aid)):
        if not query_db("SELECT g.username, g.aid FROM AssignmentGrades g WHERE g.username='{}' AND g.aid={};".format(username, aid)):            
            weight = query_db("SELECT a.weight FROM Assignments a WHERE a.id='{}';".format(aid))[0][0]
            with sql.connect('database.db') as con:
                cur = con.cursor()
                cur.execute('INSERT INTO assignmentGrades VALUES(?,?,?,?)', (aid, username, grade, weight))
            flash("Sucessfully updated Grade!")
            return redirect('/dashboard')
        flash("Grade Already Updated!")
        return redirect('/dashboard')
    flash("User not registered!")
    return redirect('/dashboard')
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