__author__ = 'willian.reis'

from database import db
from model.subscriber_model import subscriber

class call_record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.String)
    call_id = db.Column(db.Integer)
    init_call = db.Column(db.DateTime)
    end_call = db.Column(db.DateTime)
    destination = db.Column(db.String)

    subscriber_id = db.Column(db.Integer, db.ForeignKey("subscriber.id"))
    subscriber = db.relationship(subscriber)

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