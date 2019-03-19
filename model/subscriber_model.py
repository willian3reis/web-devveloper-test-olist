from database import db

__author__ = 'willian.reis'

class subscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String)


db.create_all()

