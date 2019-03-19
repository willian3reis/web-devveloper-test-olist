__author__ = 'willian.reis'

from database import db
from model.subscriber_model import subscriber
from model.price_role_model import price_rule

class price_rule_subscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    subscriber_id = db.Column(db.Integer, db.ForeignKey("subscriber.id"))
    subscriber = db.relationship(subscriber)

    price_rule_id = db.Column(db.Integer, db.ForeignKey("price_rule.id"))
    price_rule = db.relationship(price_rule)

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