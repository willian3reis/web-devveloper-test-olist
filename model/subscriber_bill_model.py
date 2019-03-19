__author__ = 'willian.reis'

from database import db
from model.price_role_model import price_rule
from model.call_record_model import call_record

class subscriber_bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float)

    price_rule_id = db.Column(db.Integer, db.ForeignKey("price_rule.id"))
    price_rule = db.relationship(price_rule)

    call_record_id = db.Column(db.Integer, db.ForeignKey("call_record.id"))
    call_record = db.relationship(call_record)


    competence = db.Column(db.String)

    def save(self):
        #verifica se eh novo. Se sim adiciona na sessao
        if not self.id:
            db.session.add(self)

        try:
            db.session.commit()
        except :
            db.session.rollback()
            raise

db.create_all()