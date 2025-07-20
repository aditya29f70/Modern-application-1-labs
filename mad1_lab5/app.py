from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse


app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///api_database.sqlite3'

db= SQLAlchemy(app)
api= Api(app)

app.app_context().push()

# api's for course

class Course(db.Model):
  course_id= db.Column(db.Integer, primary_key=True)
  course_name= db.Column(db.String(), nullable=False)
  course_code= db.Column(db.String(), nullable=False, unique=True)
  course_description= db.Column(db.String())
  
class Student(db.Model):
  student_id= db.Column(db.Integer, primary_key=True)
  roll_number = db.Column(db.String(), unique=True, nullable=False)
  first_name = db.Column(db.String(), nullable=False)
  last_name = db.Column(db.String())
  courses= db.relationship('Course', backref='students', secondary='enrollment') # db.relationship('model', backref, secondary(table so in small))

class Enrollment(db.Model):
  enrollment_id= db.Column(db.Integer, primary_key=True)
  student_id= db.Column(db.Integer, db.ForeignKey('student.student_id'))
  course_id= db.Column(db.Integer, db.ForeignKey('course.course_id'))
  


Errors={
  "COURSE001":"Course Name is required",
  "COURSE002":"Course Code is required",
  "STUDENT001":"Roll Number required",
  "STUDENT002":"First Name is required",
  "ENROLLMENT001":"Course does not exist",
  "ENROLLMENT002":"Student does not exist.",
}

def error_info(error_code):
  return {
    "error_code":error_code,
    "error_message":Errors[error_code]
  }

def info(des,value, status=200):
  return {
    "Description":des,
    "message":value
  }, status

def find_course(val):
  all_course= Course.query.all()
  course_ids= []
  course_codes=[]
  for course in all_course:
    course_ids.append(course.course_id)
    course_codes.append(course.course_code)
  if val== 'id':
    return course_ids
  else:
    return course_codes

parser= reqparse.RequestParser()
parser.add_argument('course_name')
parser.add_argument('course_code')
parser.add_argument('course_description')


class CourseApi(Resource):
  def get(self, course_id):
    try:
      if (not course_id):
        return "BAD REQUEST", 400
      elif (course_id not in find_course('id')):
        return f"Course not found", 404
      else:
        selected_course= Course.query.get(course_id)
    except Exception as e:
      return 'Internal Server Error', 500
    else:
      return info("Request Successful", {
        "course_id":selected_course.course_id,
        "course_name":selected_course.course_name,
        "course_code":selected_course.course_code,
        "course_description":selected_course.course_description
      }, 200)
  
    
  def put(self, course_id):
    args= parser.parse_args()
    try:
      
      if (not args["course_name"]):
        return info("Bad request", error_info("COURSE001"), 400)
      elif (not args['course_code']):
        return info("Bad request", error_info("COURSE002"), 400)
      elif course_id not in find_course('id'):
        return f"Course not found", 404
      else:
        corr_course= Course.query.get(course_id)
        corr_course.course_name= str(args.course_name)
        corr_course.course_code= str(args.course_code)
        corr_course.course_description= str(args.course_description)
        db.session.commit()
        to_updated= {
        "course_id": corr_course.course_id,
        "course_name": corr_course.course_name,
        "course_code": corr_course.course_code,
        "course_description": corr_course.course_description
        }
    except Exception as e:
      return f"Internal Server Error", 500
    else:
        return info("Successfuly updated",to_updated, 200)
    

  def delete(self, course_id):
    try:
      if (not course_id):
        return "BAD REQUEST", 400
      elif (course_id not in find_course('id')):
        return f"Course not found", 404
      to_delete= Course.query.get(course_id)
      db.session.delete(to_delete)
      db.session.commit()
    except Exception as e:
      return f"Intenal Server Error", 500
    else:
      return f"Successfully Deleted", 200

  def post(self):
    args= parser.parse_args()
    try:
      if (not args["course_name"]):
        return info("Bad request", error_info("COURSE001"), 400)
      elif (args['course_code']==""):
        return info("Bad request", error_info("COURSE002"), 400)
      elif args['course_code'] in find_course('code'):
        return f"course_code already exist", 409
      else:
        created= Course(course_name=args.course_name, course_code=args.course_code,course_description=args.course_description )
        db.session.add(created)
        db.session.commit()
    except Exception as e:
      return f"Internal Server Error", 500
    else:
        return f"Successfully Created", 201
    
api.add_resource(CourseApi, "/api/course/<int:course_id>", "/api/course")


# api's for student table

def find_student(val):
  student_ids= []
  student_roll_numbers=[]
  students= Student.query.all()
  for student in students:
    student_ids.append(student.student_id)
    student_roll_numbers.append(student.roll_number)
  if val=='id':
    return student_ids
  else:
    return student_roll_numbers


parser1= reqparse.RequestParser()
parser1.add_argument("first_name")
parser1.add_argument("last_name")
parser1.add_argument("roll_number")


class StudentApi(Resource):
  def get(self, student_id):
    try:
      if (not student_id):
        return "BAD REQUEST", 400
      if (student_id not in find_student('id')):
        return f"Student not found", 404
      else:
        selected_student = Student.query.get(student_id)
    except Exception as e:
      return 'Internal Server Error', 500
    else:
      return {
        "student_id":selected_student.student_id,
        "first_name":selected_student.first_name,
        "last_name":selected_student.last_name,
        "roll_number":selected_student.roll_number
      }

  def put(self, student_id):
    args= parser1.parse_args()
    try:
      
      if (not args["first_name"]):
        return info("Bad request", error_info("STUDENT002"), 400)
      elif (args["roll_number"]==""):
        return info("Bad request", error_info("STUDENT001"), 400)
      elif student_id not in find_student('id'):
        return f"Student not found", 404
      else:
        corr_student= Student.query.get(student_id)
        corr_student.first_name= str(args.first_name)
        corr_student.last_name= str(args.last_name)
        corr_student.roll_number= str(args.roll_number)
        db.session.commit()
        to_updated= {
        "student_id": corr_student.student_id,
        "first_name": corr_student.first_name,
        "last_name": corr_student.last_name,
        "roll_number": corr_student.roll_number
        }
    except Exception as e:
      return f"Internal Server Error", 500
    else:
        return info("Successfully updated", to_updated)
    
  def delete(self, student_id):
    try:
      if (not student_id):
        return "BAD REQUEST", 400
      if (student_id not in find_student('id')):
        return f"Student not found", 404
    
      else:
        to_delete= Student.query.get(student_id)
        db.session.delete(to_delete)
        db.session.commit()
    except Exception:
      return f"Internal Server Error", 500
    else:
      return f"Successfully Deleted", 200


  def post(self):
    args= parser1.parse_args()
    try:
      if (not args["first_name"]):
        return info("Bad request", error_info("STUDENT002"), 400)
      elif (args['roll_number']==""):
        return info("Bad request",error_info("STUDENT001"), 400)
      elif args['roll_number'] in find_student('roll_number'):
        return f"Student already exist", 409
      else:
        created= Student(first_name=args.first_name, last_name=args.last_name,roll_number=args.roll_number )
        db.session.add(created)
        db.session.commit()
    except Exception as e:
      return f"Internal Server Error", 500
    else:
        return info("Successfully Created", created, 201)
    
api.add_resource(StudentApi, "/api/student/<int:student_id>", "/api/student")


parser2=reqparse.RequestParser()
parser2.add_argument('course_id')



enroll_student_ids=[]
enrolled_students= Enrollment.query.all()
for student in enrolled_students:
  if student.student_id not in enroll_student_ids:
    enroll_student_ids.append(student.student_id)

class EnrollmentApi(Resource):
  def get(self, student_id):
    try:
      if (not student_id):
        return "BAD REQUEST", 400
      if (student_id not in find_student('id')):
        return info("Invalid Student Id", error_info("ENROLLMENT002"), 400)
      elif (student_id not in enroll_student_ids):
        return f"Student is not enrolled in any course", 404
      else:
        student= Student.query.get(student_id)
        student_enrolled= student.courses

      for course in student_enrolled:
        if course.course_id not in find_course('id'):
          return info('Invalid Student Id',error_info("ENROLLMENT001"), 400)
      to_enrolled=[]
      student_enrolled= Enrollment.query.filter_by(student_id= int(student_id)).all()
      for student in student_enrolled:
        to_enrolled += [{
          "enrollment_id":student.enrollment_id,
          "student_id":student.student_id,
          "course_id":student.course_id
        }]
    except Exception as e:
      return f'Internal Server Error', 500
    else:
      return info("Request Successful", to_enrolled,)


  def post(self, student_id):
    args= parser2.parse_args()
    try:
      if (not student_id):
        return "BAD REQUEST", 400
      if (student_id not in find_student('id')):
        return info("Bad request", error_info("ENROLLMENT002"), 400)
      elif (student_id not in enroll_student_ids):
        return f"Student not found", 404
      else:
        student= Student.query.get(student_id)
        student_enrolled= student.courses

      for course in student_enrolled:
        if course.course_id not in find_course('id'):
          return info("Bad request", error_info("ENROLLMENT001"), 400)

      to_add_course= Course.query.get(args['course_id']) 
      student_enrolled.append(to_add_course)
      db.session.commit()
      to_enrolled=[]
      student_enrolled= Enrollment.query.filter_by(student_id= int(student_id)).all()
      for student in student_enrolled:
        to_enrolled += [{
          "enrollment_id":student.enrollment_id,
          "student_id":student.student_id,
          "course_id":student.course_id
        }]

    except Exception as e:
      return f'Internal Server Error{e}', 500
    else:
      return info("Enrollment successful", to_enrolled, 201)


  def delete(self, student_id, course_id):
    try:
      if (not student_id):
        return "BAD REQUEST", 400
      elif (student_id not in find_student('id')):
        return info("Invalid Student Id", error_info("ENROLLMENT002"), 400)
      elif (not course_id):
        return f"Required", 400
      elif (course_id not in find_course('id')):
        return info("Invalid Course Id", error_info("ENROLLMENT001"), 400)
      elif (student_id not in enroll_student_ids):
        return f"Enrollment for the student not found", 404
      else:
        student= Student.query.get(student_id)
        student_enrolled= student.courses

      for course in student_enrolled:
        if course.course_id not in find_course('id'):
          return info("Invalid Course Id", error_info("ENROLLMENT001"), 400)
      course= Course.query.get(course_id)
      student_enrolled.remove(course)
      db.session.commit()
    except Exception as e:
      return f'Internal Server Error', 500
    else:
      return "Successfully deleted", 200

api.add_resource(EnrollmentApi, "/api/student/<int:student_id>/course", "/api/student/<int:student_id>/course/<int:course_id>")


if __name__== "__main__":
  app.run(debug=True)









