from database import db

__author__ = 'willian.reis'

class rule_type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)
