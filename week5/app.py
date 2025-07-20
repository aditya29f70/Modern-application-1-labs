
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Nullable 

app= Flask(__name__) # here we have made a flask obj

app.config["SQLALCHEMY_DATABASE_URI"]= 'sqlite:///many_to_many.sqlite3'


db= SQLAlchemy(app) # and give that app info by giving that app as argument for only the connection
# so db creatiion done by this


app.app_context().push()



class User(db.Model):
  id= db.Column(db.Integer, primary_key=True)
  username=  db.Column(db.String(20) , nullable=False, unique=True)
  password=  db.Column(db.String() , nullable=False)
  roles= db.relationship('Role', backref= 'users', secondary='association')

class Role(db.Model):
  id= db.Column(db.Integer, primary_key=True)
  role_name= db.Column(db.String(20), nullable=False, unique=True)

class Association(db.Model):
  id= db.Column(db.Integer, primary_key=True)
  user_id= db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # note vvvvimp alway in case of foreign key gives table name and tb name alway small here
  role_id= db.Column(db.Integer, db.ForeignKey('role.id'), nullable= False)






# we will be desaling with two types of relation that is 
# 1. one to many
# 2. many to many
# and also try to see how to crate those useing flask_sql_alchemy


# so we have done 'one to many ' and very similary will done 'many to many'
# #################################### many to many
# 
# so in many_to_many the models are sibilings means both the tables will be independent 
# there is no any child parent , so they can co-exist and are independent 


# so one role can be given to many users and one user can have many roles
# ques is where you will the foreign keys --> we don't add foreign key in the table
# so what do we do here --> we create a ****new table**** and this tb is called
# '''''association table'''''' and what does association table stores --> only stores
# the primary keys of both the tb and also some own attribute if having and primary key of itself -> the primary key of this tb
# is collection of these primary keys also posible but here there we can make there own primary key for each new combinatin of primary keys

# now lets go to the code
# 1. first have to make '''association table''''

# we need to tell these models that your association or correspondence is stored in
# some other table with the help of 'db.Relationship' again and you can choose any of
# the table let we choose user table ==> i want to access all the roles with this 
# attri called 'roles' and this one getting by telling 'User.roles' and get all the users of a role by 
# telling user.roles ---> for that we have to an extra thing as to provide where
# exactly the association or the correspondence of this table is store --> association table
# and that needs to be knows to these models , using this attribute called 'secondary'= 'give_that_association_table_name' note: have to give 'tb name'



# note: whenever you ask user.roles it will give you '''list''' of roles of that particular obj
# lly role.users bz it is a many to many relation
# and all list method can be applicabel on it 


# now assign user_1 to role_1, do in the shell --> role_1.users.append(user_1)
# and want to save this change in association table --> do commit

# you can also do it manually by make a obj of assocaition and after that make a session
# and the commit it 

# you will see how to use these commands (python commands) within the 
# controllers --> bz these are the python statements and do some bussiness logic with that
# 



######## some import theory
# what is controller: it retrive the data from the db
# process it if there is requirement and dump it onto
# a template

# so a controller will always return a template rendered
# with correct data (always return htlm template) this is a one fn

# what are the other fn of controller
# it will do all the process and redirect to some other
# controller or some other end point 


## now what is API does
# API does not return an HTML , it doesn't know that what i am returning (unstructure data)
# so it will always return json file