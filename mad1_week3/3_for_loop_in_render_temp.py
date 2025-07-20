from jinja2 import Template
data= ["Analyst", "Programmer", "Developer"]

temp="""
    {% for item in data %}
      {{item}}
    {% endfor %}
    """

# you can see in output there are some gap space bz here temp is a text and
# spaces are present as you can see

made_temp= Template(temp)
output= made_temp.render(data= data)
print(output)