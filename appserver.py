from flask import Flask
from flask_restful import Api
from flask_httpauth import HTTPBasicAuth
from flask_mail import Mail
from flasgger import Swagger

app = Flask(__name__)
app.config.from_object('settings')
swagger = Swagger(app)

apiRest = Api(app)
auth = HTTPBasicAuth()
mail = Mail(app)
