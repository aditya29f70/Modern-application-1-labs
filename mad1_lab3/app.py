from flask import Flask, render_template, request
import pyhtml as h
import pandas as pd
import matplotlib.pyplot as plt
from jinja2 import Template


app= Flask(__name__)


@app.route("/", methods=["GET"])
def home():
  return render_template("index.html")


@app.route("/", methods=["POST"])
def section():
  id_info=None
  id=None
  id_info= request.form["ID"]
  id= request.form["id_value"]

  df= pd.read_csv("data.csv")
  df.columns= df.columns.str.strip()
  dic= df.to_dict(orient='records')



  def figure(df, id):
    c_df= df[df['Course id']==id]
    fig_df= c_df.groupby('Marks')['Student id'].count().reset_index()

    plt.figure(figsize=(5, 4))
    plt.bar(fig_df["Marks"], fig_df['Student id'], edgecolor='black')
    plt.xlabel("Marks")
    plt.ylabel("frequency")

    fig_path= f"static/fig_{id}.png"
    plt.savefig(fig_path)
    plt.close()
    return f"fig_{id}.png"


  flag=True
  if id.isdigit() and (id is not None) and (id_info is not None):
    id= int(id)
  else:
    flag=False

  if (id_info=="student_id") and (flag) and (id not in df['Course id'].values):
    output= render_template("test.html", dic= dic, id= id)

  elif (id_info=='course_id') and (flag) and (id not in df['Student id'].values):
    output= render_template("test2.html", dic= dic, id= id, figa= figure(df, id))
  else:
    temp3= h.html(
    h.head(
      h.title('Something Wend Wrong')
    ),
    h.body(
      h.h1('Wrong Inputs'),
      h.p('Something went wrong'),
      h.a(href="/")("Go Back")
    )
    )
    output= temp3.render()

  return output

if __name__=="__main__":
  app.run()



