from flask import Flask
from model import db, Material, Item #module
from flask_restful import Resource, Api, reqparse

app= Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///myapi_db.sqlite3"
api= Api(app)
db.init_app(app) # similar to db= SQLAlchemy(app) but here we first make this SQLAlchemy obj in model.py and here we initilize

app.app_context().push()

parser= reqparse.RequestParser()
parser.add_argument('name') ### there are two methods add argument and retrive argument
## what ever attribute value we want from that json file coming to server we add it basically
# parser and then use it , basically parse will be a py dic which will the attri value as argu name
# as you mention above


class MaterialApi(Resource):
  def get(self):
    all_materials_obj= Material.query.all() # list of obj
    all_materials={}
    i=1
    for material in all_materials_obj:
      this_material={}
      this_material['id']= material.id
      this_material['name']= material.name
      all_materials[f'material_{i}']= this_material
      i+=1
    return all_materials


  def post(self):
    args= parser.parse_args() # so when we write this args will have a dic that is JSON in the form of argu that we have created
    new_mat= Material(name= args['name'])
    db.session.add(new_mat)
    db.session.commit()
    return "Add successfully", 201
  
  def put(self, id):
    to_update= Material.query.get(id)
    args= parser.parse_args()
    # updating here
    to_update.name= args["name"]
    db.session.commit()
    return 'Updated successfully'

  def delete(self, id):
    to_delete= Material.query.get(id)
    db.session.delete(to_delete)
    db.session.commit()
    return "Deleted Successfully"







## every successfule operation in the web by default has 200 status code but in general when you create (post)
# a new resource in the database (taking about conventions) you should return 201 status code

api.add_resource(MaterialApi, "/api/all_materials", "/api/create", "/api/<int:id>/update", "/api/<int:id>/delete") # sp args should be (class, resource url or get but alos can work for 'get' bz we are not specifying it or no are method are taking any specific argument so any resouce url can use, second resource url for 'post' but lly you can also use it for 'get')


    

if __name__== '__main__':
  app.run(debug=True)


# now let us configure the api by flask_restful import Resorce, Api objects
# then make api obj


# i seperated out models from my controllers to a diff py file for making things easier
# if i decide to seperate out apis from my controller what will i do 
# i will create new py file and import that 

# now that we were doing in ''''flask'''
# define route with endpt + methods --> mapped view fn --> there functionality --> returned template
# like 1. let @app.route('/home', methods=['GET'])
#               def home():
                  #
#                 return render some html file


# there is slight diff in ''''flask-restful''''
# first define a class( basically it will define our API ) --> in the class we define method(nothing it is functions)  --> functionality --> defining of route
# and that class will inherits resource class

#eg
# 1. class MaterialApi(Resource):  # lly as flask route make step1
#      def get(self): # step2
          # and functionality will be same as flask fn functionality
          # let we are taking all the materials form material table
        # all_materials_obj = Material.query.all()  # gives list of objects

# vvimp the method that we create should be the name of HTTP method or verbs(get, post, put, delete ...etc)
# generally we use 'CURD' methods only get--> read, post --> create, put --> update, delete --> ``
# since it is class methods so they will take 'self' argument must or other also if required 
#  and vvvimp what ever you are going to return i will be in json format so will have to 
# convert this into json --> and it nothing python obj and structor should be like this
#  --> {obj1: {id:1, 'name':'Plastic'}
#       .........} 
# and at the end return that json file

# now final step is defined routes --> when will this fn get triggered (this get fn which we have use to define class method)
# or what should be the url which that triggers this get fn and that is done py using this
# '''" api.add_resurce(api_class, resource) "''' there we direct gave endpy+ methods , but here '''' we will have to provide
# resources differently ''''

# we have to first provide for which class we are creating resource as first parameter and then 
# we will define the resource(endpt)  and by convancion we start it with '/api' that will info that we try to retrieve data from api
# and this endpt also called --> resource URL


# how do we test api it is running or not bz here we are not rendering anything
# --> so for that we have something called as '''' Swagger UI ''''''

# other way is doing it called '''Thunder client''' it is also an extension of vs code
# just download the Thunder client --> for testing you api lly there is also a web application you can check your api is 
# ''''Postman''''
# we will be using ''Thunder client'' => this interface allows you to make request to any URL with any method 
# that is a very good advantage of using this

# now run the application and try to see the output


# so in CRUD
# we have seen the 'R' --> 'get' , it is showing the json file we are not any row data with resource url now we will see
# the C --> 'post' Create and when we create with the help of post the data goes to server as request body

### when we are trying to sent some data to the server. The data using the post method the data goes as request  but how will it know
# that you have to take data from the request body --> for something called '''request parse'' that will make use for it
# so we have to import it by this module is also in that flask_restful --> some assumption as to made
# what should be the data that the server should look , so 1. thing which we have to tell the server that you have to 
# look some data in the request body and 2. thing is what data you should look for

# so the server should know that the data is there in request body and second thing what is that data
# so make sure that server knows that the data is there in the request body we are using ''request-parser''
# and to make sure what data the server should know that is done with the help of '''defining arguments''

# it does in above the class

## now last step is defining routes so add it in the api.add_resouce(MaterialApi, "/api/all_materials", "/api/create") that last one

##### vvipm :--> if there is any issue with the request it has to bad code ; bad request error




######################################## now we will quickly write for ''''delete'' and '''update --> 'put' ''' 
# now use put http method for update , but same problem aries that ; how do you know what to update how do you know what to delete 
# so that you need to provide an argument for this --> so self will be there bz it is a class method but '''id''' that something that you provide
# so you first retrive that element then update 
# 1. first how to you like it with end pt add  new resource url for in ''api.add_resource''  so resource url must be contain ''id''
# so that backend receive it and then update

# and also in for updating argument we can use that 'post' argument bz in material table only have ''name'' , the same arg can we use
# note there are two thing is coming an id from resource url so you can identify which material you have to update
# and which thing you have to update will come through argument (through json file) or from request body and you have to make new obj and then can update

#################### with that do delete very quickly 
# note: code for delete is very easy , and also like to say that for general again that , we don't need any endpt or resource url for delete technicaly
# which we can use any resource url with any methods but what method we are using that is import but for convenstionlly for good understanding
# we use diff url for diff methods



############## finally we can make our documentation
#### remember this convensional resource url
# POST /api/create
# GET /api/any_unique_related_name
# PUT /api/<int:id>/update but in documentation you write something like thing : /api/{id}/update
# DELETE /{id}/delete
# so these thing will be giving to you for backend api document which url is working for which thing 



### at the end imp pt
# if we are going to make api for another table we will be using another class and for that class 
# we should have another ''''api.add_resource(class_name, and_api'es)