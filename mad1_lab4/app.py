from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.exc import IntegrityError

app= Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]= "sqlite:///database.sqlite3"

db= SQLAlchemy(app)


class Student(db.Model):
  student_id= db.Column(db.Integer, primary_key=True)
  roll_number= db.Column(db.String(), unique=True, nullable=False)
  first_name= db.Column(db.String(), nullable=False)
  last_name= db.Column(db.String())
  courses= db.relationship('Course', backref='students', secondary='enrollments')

class Course(db.Model):
  course_id= db.Column(db.Integer, primary_key= True)
  course_code= db.Column(db.String(), unique=True, nullable=False)
  course_name= db.Column(db.String(), nullable=False)
  course_description= db.Column(db.String())

class Enrollments(db.Model):
  enrollment_id= db.Column(db.Integer, primary_key=True)
  estudent_id= db.Column(db.Integer, db.ForeignKey("student.student_id"), nullable=False)
  ecourse_id= db.Column(db.Integer, db.ForeignKey("course.course_id"), nullable=False)

@app.route('/', methods=["GET", "POST"])
def stud_del():
  if request.method=='GET':
    lis = Student.query.filter_by().all()
    dic={}
    for obj in lis:
      dic[obj.student_id]= [obj.roll_number, obj.first_name, obj.last_name]
    return render_template('index.html', dic= dic)

@app.route('/student/create', methods=["GET", "POST"])
def create_stu():
  if request.method=="GET":
    return render_template('stu_create.html')
  else:
    s_roll= request.form.get('roll')
    s_f_name= request.form.get('f_name')
    s_l_name= request.form.get('l_name')
    selected_courses= request.form.getlist('courses')
    stu= Student(roll_number=s_roll, first_name=s_f_name, last_name=s_l_name)
    try:
      db.session.add(stu)
      db.session.commit()
    except IntegrityError:
      db.session.rollback()
      return render_template('already_s_roll.html')
    for c in selected_courses:
      if c=='course_1':
        course= Course.query.filter_by(course_name='MAD I').first()
      elif c=='course_2':
        course= Course.query.filter_by(course_name='DBMS').first()
      elif c=='course_3':
        course= Course.query.filter_by(course_name='PDSA').first()
      else:
        course= Course.query.filter_by(course_name='BDM').first()
      stu.courses.append(course)
      db.session.commit()
    
  return redirect(url_for("stud_del"))

@app.route("/student/<int:student_id>/update", methods=["GET", "POST"])
def update_student(student_id):
  lis = Student.query.filter_by().all()
  dic={}
  for obj in lis:
    dic[obj.student_id]= [obj.roll_number, obj.first_name, obj.last_name]
  
  stu= Student.query.get(student_id)
  c= stu.courses
  selected_courses=[]
  for cour in c:
    if cour.course_name== 'MAD I':
      selected_courses.append('course_1')
    elif cour.course_name== 'DBMS':
      selected_courses.append('course_2')
    elif cour.course_name== 'PDSA':
      selected_courses.append('course_3')
    else:
      selected_courses.append('course_4')
  if request.method=='GET':
    return render_template('update_stu.html', student_id= student_id , current_roll= int(dic[student_id][0]), current_f_name= dic[student_id][1], current_l_name= dic[student_id][2], selected_courses= selected_courses)
  else:
    f_name= request.form.get("f_name")
    l_name= request.form.get("l_name")
    c_s= request.form.getlist("courses")
    print(f_name)
    stu.first_name= f_name
    stu.last_name= l_name
    db.session.commit()
    stu.courses=[]
    for c in c_s:
      if c=='course_1':
        course= Course.query.filter_by(course_name='MAD I').first()
      elif c=='course_2':
        course= Course.query.filter_by(course_name='DBMS').first()
      elif c=='course_3':
        course= Course.query.filter_by(course_name='PDSA').first()
      else:
        course= Course.query.filter_by(course_name='BDM').first()
      stu.courses.append(course)
    db.session.commit()
  return redirect(url_for("stud_del"))

@app.route('/student/<int:student_id>/delete', methods=["GET"])
def delete_stu(student_id):
  stu= Student.query.get(student_id)
  stu.courses=[]
  db.session.delete(stu)
  db.session.commit()
  return redirect(url_for('stud_del'))


@app.route("/student/<int:student_id>", methods=["GET"])
def stu_info(student_id):
  stu= Student.query.get(student_id)
  courses= stu.courses 

  cour_info={}
  for c in courses:
    cour_info[c.course_id]= [c.course_code, c.course_name, c.course_description]
  
  return render_template('stu_info.html', roll= stu.roll_number, f_name= stu.first_name
                         , l_name= stu.last_name, cour_info= cour_info)



if __name__=='__main__':
  app.run(debug=True)





















