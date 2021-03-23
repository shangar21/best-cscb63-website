from database import get_db, query_db, make_dicts, close_db
from flask import Flask, render_template,  request, g, current_app
import sqlite3 as sql

app = Flask(__name__)

'''
Page Rendering: 
The code below this (but above the backend) will handle the rendering of pages that students and teachers interact with. 
These pages will be connected to the backend where the backend does the SQL queries as well as adding new values etc.
'''
def hello():
    return render_template('index.html')

@app.route('/new_student_acct')
def create_student_page():
    return render_template('student_user.html')

@app.route('/student_log_in_page')
def log_in_student():
    return render_template('student_log_in.html')


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
        return "Submitted!"
    return "Already an account with that information!"    


@app.route('/verify_student_user')
def verify_student_user():
    username = request.args.get('username')
    password = request.args.get('password')

    if query_db("SELECT s.username FROM StudentUsers s WHERE s.username='{}';".format(username)):
        if query_db("SELECT s.password FROM StudentUsers s WHERE s.username='{}';".format(username))[0][0] == password:
            return "Congrats on the correct log-in info fam!"
        else:
            return "who u is??????? that aint the right password guy"
    return "aint no username like that here dawgy"


if __name__ == "__main__":
    app.run(debug=True)