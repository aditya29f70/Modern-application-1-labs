from jinja2 import Template

# now in jinja2 see how we can formatting printing
# note why we use jinja bz it support looping and if else condition


name= 'Rishav'
place= 'bihar'
profession= 'course instructor'

# step1 : make formatting 
temp= "my name is {{name}}, i live in {{place}}, i am a {{profession}}"

# step2 : make template for this
made_temp= Template(temp)

# step3 : render it with data by using render template fn
# and inside that render fn we have to declare variable with values
output= made_temp.render(name= name, place= place, profession= profession)

print(output)

# in ''case of jinja'' if you don't provide value for the variable it will simipaly keep it a variable
# as blind , it will not through error

# now we are going to see how to use for loop in jinja









