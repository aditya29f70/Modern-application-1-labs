from jinja2 import Template

t= Template("Numbers divisible by 2:{% for n in range(0, 10, 2) %} {{n}}{% endfor %}")

print(t.render())