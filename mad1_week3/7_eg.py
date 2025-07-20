# now we are going to use 'string module' that is also used for templating

from string import Template

temp= Template("Today is $today and tomorrow is $tomorrow.")
# out= temp.substitute(today='Monday', tomorrow='Tuesday')

# out= temp.substitute(today='Monday') # keyError: 'tomorrow'

out= temp.safe_substitute(today= 'Monday')

print(out)

# jinja --> {{}}, render--> means we use 'render' fn to render the info, doesn't throw error if value not passed
# string --> $, substitute, throws error if value not assigned, so for solution you should you 
# 'safe_substitute'