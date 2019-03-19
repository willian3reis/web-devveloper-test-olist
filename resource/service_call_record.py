from model.call_record_model import call_record
from model.price_role_model import price_rule
from model.price_rule_subscriber_model import price_rule_subscriber
from model.subscriber_bill_model import subscriber_bill
from model.subscriber_model import subscriber
from flask_restful import Resource
from appserver import apiRest, auth
from flask_restful.utils import cors
from flask import request, jsonify
import pandas as pd
import numpy as np

def count(dt_weights):
    lista = []
    contador=0
    n=0
    for i in dt_weights:
        if i == 1:
            #print i
            ini_conta = True
            n=n+1
        else:
            ini_conta = False
            if contador!= 0:
                lista.append({n:contador})
            contador = 0
            #print i

        if ini_conta:
            contador = contador + 1

    if contador!= 0:
        lista.append({n:contador})

    return lista

def weighted_timedelta_night(start_dt, end_dt,
                       nights_start,
                       nights_end,
                       night_weight = 1):

    # convert dts to pandas date-range series, minute-resolution
    dt_range = pd.date_range(start=start_dt, end=end_dt, freq='min')

    # Assign 'weight' as -night_weight- or 1, for each minute, depeding on day/night
    dt_weights = np.where((dt_range.time >= nights_start) |  (dt_range.time <= nights_end),
                          night_weight, 0)
    # return value as weighted minutes
    return dt_weights.sum() -1, len(count(dt_weights))

def weighted_timedelta_day(start_dt, end_dt,
                       nights_start,
                       nights_end,
                       night_weight = 1):

    # convert dts to pandas date-range series, minute-resolution
    dt_range = pd.date_range(start=start_dt, end=end_dt, freq='min')

    # Assign 'weight' as -night_weight- or 1, for each minute, depeding on day/night
    dt_weights = np.where((dt_range.time >= nights_start) &  (dt_range.time <= nights_end),
                          night_weight, 0)

    # return value as weighted minutes
    return dt_weights.sum()-1, len(count(dt_weights))


def calculate_telephone_bill(ocall_record):
    lista_regras = price_rule_subscriber.query.filter(price_rule_subscriber.subscriber_id == ocall_record.subscriber_id).all()

    for regra in lista_regras:
        value_calculated = 0

        oprice_rule = price_rule.query.filter(price_rule.id == regra.price_rule_id).first()

        if oprice_rule.rule_type.description == 'Standing charge':
            if oprice_rule.end_interval > oprice_rule.init_interval:
                count_fixed = weighted_timedelta_day(ocall_record.init_call, ocall_record.end_call, oprice_rule.init_interval, oprice_rule.end_interval)[1]
            elif oprice_rule.end_interval < oprice_rule.init_interval:
                count_fixed = weighted_timedelta_night(ocall_record.init_call, ocall_record.end_call, oprice_rule.init_interval, oprice_rule.end_interval)[1]
            else:
                count_fixed = 0

            value_calculated = value_calculated + (oprice_rule.price*count_fixed)

        elif oprice_rule.rule_type.description == 'Call charge/minute':
            if oprice_rule.end_interval > oprice_rule.init_interval:
                count_minutes = weighted_timedelta_day(ocall_record.init_call, ocall_record.end_call, oprice_rule.init_interval, oprice_rule.end_interval)[0]
            elif oprice_rule.end_interval < oprice_rule.init_interval:
                count_minutes = weighted_timedelta_night(ocall_record.init_call, ocall_record.end_call, oprice_rule.end_interval, oprice_rule.init_interval)[0]
            else:
                count_minutes = 0

            if count_minutes < 1:
                count_minutes = 0

            value_calculated = value_calculated + (oprice_rule.price * count_minutes)

        osubscriber_bill = subscriber_bill()
        osubscriber_bill.value = value_calculated
        osubscriber_bill.price_rule_id = oprice_rule.id
        osubscriber_bill.call_record_id= ocall_record.id
        osubscriber_bill.competence = str(ocall_record.end_call.month)+'/'+str(ocall_record.end_call.year)
        osubscriber_bill.save()

class call_record_Resource(Resource):
    decorators = [cors.crossdomain(origin='*', headers=['Content-Type', 'Authorization'])]

    def head(self):
        return jsonify({})

    def options(self):
        return jsonify({})

    def post(self):
        """This endpoint is used to send call record
        This is using docstrings for specifications.
        ---
        parameters:
          - name: id
            type: string
            in: path
          - name: type
            type: string
            in: path
          - name: timestamp
            type: datetime
            in: path
          - name: call_id
            type: integer
            in: path
          - name: source
            type: string
            in: path
          - name: destination
            type: string
            in: path
        responses:
          200:
            description: Return is send call record is OK
            examples:
              {"message":"OK"}
        """
        id = request.json.get('id', None)
        type = request.json.get('type')
        timestamp = request.json.get('timestamp')
        call_id = request.json.get('call_id')
        source = request.json.get('source')
        destination = request.json.get('destination')

        try:
            if type == 'start':
                osubscriber = subscriber.query.filter(subscriber.number == source).first()
                ocall_record = call_record()
                ocall_record.subscriber_id = osubscriber.id
                ocall_record.call_id = call_id
                ocall_record.init_call = timestamp
                ocall_record.destination = destination
                ocall_record.save()
            elif type == 'end':
                ocall_record = call_record.query.filter(call_record.call_id == call_id).first()
                if ocall_record == None:
                    return jsonify({"message":"This call_id does not exist."})

                ocall_record.end_call = timestamp
                ocall_record.save()
                calculate_telephone_bill(ocall_record)

            return jsonify({"message":"OK"})
        except:
            return jsonify({"message":"ERROR"})


apiRest.add_resource(call_record_Resource, '/service_call_record/call_record')