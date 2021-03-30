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

@app.route('/add_to_feedback')
def addToFeedback():
    instructor = request.args.get('instructor')
    rating = request.args.get('rating')
    likeTeach = request.args.get('likeTeach')
    impTeach = request.args.get('impTeach')
    likeLab = request.args.get('likeLab')
    impLab = request.args.get('impLab')

    fid = query_db('SELECT MAX(f.id) FROM Feedback f;')[0][0] + 1

    with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("Insert INTO Feedback VALUES (?,?,?,?,?,?,?);", (fid, instructor, rating, likeTeach, impTeach, likeLab, impLab))
    flash("Feedback Successfully sent!")
    return redirect('/feedback')

@app.route('/submit_regrade')
def addToRegrade():
    userName = request.args.get('student_username')
    assignment = request.args.get('assignment')
    reason = request.args.get('reason')

    rid = query_db('SELECT MAX(r.id) FROM Regrade r;')[0][0] + 1

    with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("Insert INTO Regrade VALUES (?,?,?,?);", (rid, userName, assignment, reason))
    flash("Regrade Successfully sent!")
    return redirect('/dashboard')

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

