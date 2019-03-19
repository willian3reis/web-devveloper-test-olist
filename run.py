from appserver import app
import os

import model.subscriber_model
import model.rule_type_model
import model.price_role_model
import model.call_record_model
import model.subscriber_bill_model
import model.price_rule_subscriber_model

import resource.service_call_record
import resource.service_subscriber_bill

port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port, debug=True, use_reloader=True)

