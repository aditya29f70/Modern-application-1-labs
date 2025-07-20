# what is coding part of week4 1. screen cast
# so in screen cast sir has covered flask, in this
# we have convered what a basic flask application looks like

from flask import Flask, render_template,request

# app= Flask(__name__) # we are feeding our app into Flask
# # this is something that we need to set up before running flask

# if __name__=="__main__":
#   app.run(debug=True)

# ---> this was how to setup flask


# now what does flask usually do
# impvvvvv;  index.html is default file, flask will when ever
# going for any default fall the web browser will always go for 
#  index.html and what is default route --> '/'

# so there are two parts over here that you need to understand
# that are frontend , backend so let you have a good html(frontend file and you want to show it)
# inside the browser so now how will you do that for that you have to actually
# serve this file index.html(let) inside into flask file or any kind of 
# backend server that can handle html file and now question arrieses what backend server do
# (like in flask --> python py_file_name in command-line) so for that we have 
# to mention the routes and everything, right so this py file is nothing backend file
# and flask is working as frame which converting commond so frontend show accordingly and pass data from front to back


# you can directly run and show the frontend what you input data
# will not go any where and utilize anywhere 


# now come how we will coding in flask, we have learn how to setup in flask

# this app means that hole thing (backend) and default value of name in __name__ is main.py, it just say we want to use flask as the bakend server
# for our app over here. (below that line)
app= Flask(__name__)



# that is body part
# route for the home page
@app.route('/', methods=["GET"]) # app is referring the hole backend and route is referring index.html here
# it is saying that the index.html should be rendered to the
# route of '/'
def home():
  return render_template('index.html', name='Rishav')

# note as you see in index.html form tag where i used action= '/sumit' and method= post
# due that when you give the input in initail local host '/' that input will post on url '/submit'

# it says , we have passed everything on to flask. if we have agreed to
# use flask over here as our backend and server only then the app will allow to run
# so for that we should have something in the backend which will handle that post
# and note(post means we are forwarding some data from frontend to backend)

# Route to handle form submission
# note vvi in index.html we use action+ method in form tag
# and action tag help to redirect to another route(/submit here) with method post means what ever input you will
# get from that input tag post it in that route  
@app.route("/submit", methods=["POST"])
def submit():
  user_name= request.form['username']
  # that render store fetch data as a dict key 0, 1, 2.. and value , but here we directly getting value bz there is only value
  return render_template('greeting.html', name= user_name)
# what does 'request' do?: request is able to fetch whatever
# data we pass inside of the form, like from the frontend


if __name__=='__main__':
  app.run(debug=True)


# let talk about method, there are mostly two method 
# 1. 'GET'(otherwise use get, mostly when you have to show the html template
# ), 2. 'POST'(used when you have some forms and stuff to sent data)