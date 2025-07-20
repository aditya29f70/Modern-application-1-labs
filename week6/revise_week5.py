# in this week we will be learning more about the api
# all of things which we have done in till w5 will use it again for frontend
# so take those app.py code first and till that all the works are for 

from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

app= Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///database.sqlite3"

db= SQLAlchemy(app)

app.app_context().push()

class User(db.Model):
  id= db.Column(db.Integer, primary_key=True)
  username= db.Column(db.String(), nullable=False, unique=True)
  password= db.Column(db.String(), nullable= False)
  email=db.Column(db.String())
  roles= db.relationship('Role', backref='users', secondary='association')

class Role(db.Model):
  id= db.Column(db.Integer, primary_key= True)
  r_name= db.Column(db.String(), nullable=False, unique= True)

class association(db.Model):
  id= db.Column(db.Integer, primary_key=True)
  user_id= db.Column(db.Integer, db.ForeignKey('user.id'), nullable= False)
  role_id= db.Column(db.Integer, db.ForeignKey('role.id'), nullable= False)





# ########################### for routes
# --> every routes or endpoint will trigger a fn and
# that fn is nothing but a controller that fn also called as
# ''view fn '''

# now let we have sample database in many to many
# and we are going to create a frontend application
# based on this data(that we have create w5) which will list all the users on
# the page first

# code --> connect to server (backend code) --> map endpoints with fn and connect to local machine
# and in bz we (clicking the end pt let /create_users ---> trigger fn)

# in this structure what we are doing only 'code' part how it is connecting with server or mapping endpoint with fn
# etc we are not doing --> so how these thinsg are happening
#  ans --> due to this '@' sign --> so what is happening due this @ sign is
# --> is referring to ''decorator' what is that --> adds additinal functinality
# on top of your fn so that you only need to write code other addition works are done 

# but question where these additional funcationalty are written in your app when you created that app obj
# it come already written you have only gives that @ 

# it is always better to create intuitive route names
# with intuitive fn name 
# means route (endpt name ) and fn name try to take related will help to understand others




if __name__== '__main__':
  app.run(debug=True)

