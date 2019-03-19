import datetime
from flask_restful import Resource
from appserver import apiRest, auth
from flask_restful.utils import cors
from flask import request, jsonify
from model.call_record_model import call_record
from model.subscriber_bill_model import subscriber_bill
from model.subscriber_model import subscriber
from sqlalchemy.sql import func

class subscriber_bill_Resource(Resource):
    decorators = [cors.crossdomain(origin='*', headers=['Content-Type', 'Authorization'])]

    def get(self):
        """This endpoint return a bill's subscriber by reference period
        This is using docstrings for specifications.
        ---
        parameters:
          - name: number
            type: string
            in: path
          - name: reference_period
            type: integer
            in: path
        responses:
          200:
            description: Return a list of bill
            examples:
              [{"destination":xxxxxxx,"call start date":"YYYY/MM/DD", "call start time":"HH:MM:SS", "call_duration":"HH:MM:SS", "call_price":0.00}]
        """
        number = request.args.get('number')
        competence = request.args.get('reference_period', None)

        subscriber_id = subscriber.query.filter(subscriber.number == number).first()

        query = subscriber_bill.query.join(call_record, call_record.id == subscriber_bill.call_record_id)\
            .add_columns(subscriber_bill.call_record_id).filter(call_record.subscriber_id == subscriber_id.id)
        if competence != None:
            query = query.filter(subscriber_bill.competence == competence)

        result = query.distinct(subscriber_bill.call_record_id)

        list = []
        for item in result:
            call_record_item = call_record.query.filter(call_record.id == item.call_record_id).first()
            duration = call_record_item.end_call - call_record_item.init_call

            query = subscriber_bill.query.join(call_record, call_record.id == subscriber_bill.call_record_id)\
                .add_columns(subscriber_bill.value).filter(call_record.subscriber_id == subscriber_id.id)
            if competence != None:
                query = query.filter(subscriber_bill.competence == competence)

            value_reponse = 0
            for a in query.all():
                value_reponse = value_reponse + a.value

            response = {"destination":call_record_item.destination, "call start date":str(call_record_item.init_call.date()),
                        "call start time":str(call_record_item.init_call.time()), "call duration": str(duration), "call price":value_reponse}
            list.append(response)
        return jsonify(list)



apiRest.add_resource(subscriber_bill_Resource, '/service_call_record/subscriber_bill')
