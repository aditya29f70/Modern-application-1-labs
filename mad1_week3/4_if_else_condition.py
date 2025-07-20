from jinja2 import Template

sub= "MAD 1" 
temp="""
    {% if '1' in sub %}
      The course is {{sub}}
    {% else %}
      The course is different
    {% endif %}
     """
made_temp= Template(temp)
output= made_temp.render(sub= sub)

print(output)