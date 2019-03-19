from database import db
from model.rule_type_model import rule_type
__author__ = 'willian.reis'

class price_rule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)
    init_interval = db.Column(db.Time)
    end_interval = db.Column(db.Time)
    price = db.Column(db.Float)

    rule_type_id = db.Column(db.Integer, db.ForeignKey("rule_type.id"))
    rule_type = db.relationship(rule_type)

db.create_all()

