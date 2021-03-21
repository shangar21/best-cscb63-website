from database import get_db, query_db, make_dicts
from flask import Flask, render_template,  request, g

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/new_student_acct')
def create_student_page():
    return render_template('student_user.html')

@app.route('/create_student_user', methods=['POST'])
def create_student_user():
    pass

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == "__main__":
    app.run()