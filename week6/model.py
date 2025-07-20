from flask_sqlalchemy import SQLAlchemy

db= SQLAlchemy()

class Material(db.Model):
  id= db.Column(db.Integer, primary_key=True)
  name= db.Column(db.String(), nullable= False, unique=True)
  items= db.relationship('Item', backref='madeof', cascade= 'all, delete')

class Item(db.Model):
  id= db.Column(db.Integer, primary_key=True)
  name= db.Column(db.String(), nullable=False)
  quantity= db.Column(db.Integer())
  build= db.Column(db.Integer(), db.ForeignKey('material.id'))