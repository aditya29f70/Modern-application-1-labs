import sys
import pyhtml as h
import pandas as pd
import matplotlib.pyplot as plt
from jinja2 import Template

info= sys.argv
df= pd.read_csv("data.csv")
df.columns= df.columns.str.strip()
dic= df.to_dict(orient='records')


def figure(df, id):
  c_df= df[df['Course id']==id]
  fig_df= c_df.groupby('Marks')['Student id'].count().reset_index()

  plt.bar(fig_df["Marks"], fig_df['Student id'], edgecolor='black')
  plt.xlabel("Marks")
  plt.ylabel("frequency")

  fig_path= f"fig_{id}.png"
  plt.savefig(fig_path)
  plt.close()
  return fig_path


flag=True
if info[2].isdigit():
  id= int(info[2])
else:
  flag=False

if (info[1]=='-s') and (flag) and (id not in df['Course id'].values):
  with open('test.html', 'r') as f:
    temp= f.read()
  made_temp= Template(temp)
  output= made_temp.render(dic= dic, id= id)

elif (info[1]=='-c') and (flag) and (id not in df['Student id'].values):
  with open('test2.html', 'r') as g:
    temp2= g.read()
  made_temp= Template(temp2)
  output= made_temp.render(dic= dic, id= id, figa= figure(df, id))
else:
  temp3= h.html(
  h.head(
    h.title('Something Wend Wrong')
  ),
  h.body(
    h.h1('Wrong Inputs'),
    h.p('Something went wrong')
  )
  )
  output= temp3.render()

with open('output.html', 'w') as o:
  o.write(output)





