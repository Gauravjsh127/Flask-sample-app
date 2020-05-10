import os
from flask import Flask, request, abort, jsonify, send_from_directory
from flask_restplus import Api, Namespace, Resource, fields
from werkzeug.utils import secure_filename
from werkzeug import FileStorage
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

from .models import db, ma
from .models.conditionModel import Conditions, ConditionsSchema, CONDTION_ITEM_DB
from .common_libs.common import log

CONDITIONS = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Build the Sqlite ULR for SqlAlchemy
SQLITE_URL = "sqlite:///" + os.path.join(BASE_DIR, "../conditions.db")

# Configure the SqlAlchemy part of the app instance
CONDITIONS.config["SQLALCHEMY_ECHO"] = True
CONDITIONS.config["SQLALCHEMY_DATABASE_URI"] = SQLITE_URL
CONDITIONS.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Create the SqlAlchemy db instance
db.init_app(CONDITIONS)
# Initialize Marshmallow
ma.init_app(CONDITIONS)

REST_APIS = Api(
    app=CONDITIONS,
    title='Sample Conditions Microservice : Rest APIs description',
    version='1.0',
    doc='/docs',
    # All REST_APIS metadatas
)

conditionItem = REST_APIS.model('ConditionItem', CONDTION_ITEM_DB)

CONDITIONS_ITEM_LIST = REST_APIS.model('ConditionsItemList', {
    'conditionId': fields.List(fields.Nested(conditionItem)),
})

CONDITION_PARSER = REST_APIS.parser()
CONDITION_PARSER.add_argument('name', location='form', type=str, required=True)
CONDITION_PARSER.add_argument('description', location='form', type=str, required=True)

conditionsREST_APISs = Namespace('/conditions', description='Endpoints available to manage conditions')

REST_APIS.add_namespace(conditionsREST_APISs, path='/conditions')


@conditionsREST_APISs.route("/")
class ConditionsREST_APIS(Resource):
    def get(self):
        """Endpoint to get all the conditions details"""
        # Query
        condition = Conditions.query.all()
        # Serialize the data for the response
        conditionSchema = ConditionsSchema(many=True)
        data = conditionSchema.dump(condition).data
        log(data)
        return data


    @conditionsREST_APISs.expect(CONDITION_PARSER)
    @conditionsREST_APISs.response(200, 'Condition added successfully', conditionItem)
    @conditionsREST_APISs.response(400, 'Bad request')
    def post(self):
        """Add a new condition"""
        args = CONDITION_PARSER.parse_args()
        # Add to conditions database
        conditionCreated = Conditions(name=args['name'] , description=args['description'])
        db.session.add(conditionCreated)
        db.session.commit()
        conditionQuery = Conditions.query.filter_by(conditionId=conditionCreated.conditionId).first()
        # Serialize the data for the response
        conditionSchema = ConditionsSchema(many=False)
        data = conditionSchema.dump(conditionQuery).data
        log(data)
        return data, 200


@conditionsREST_APISs.route("/<int:id>")
class ConditionREST_APIS(Resource):
    @conditionsREST_APISs.response(200, 'Condition details returned', conditionItem)
    @conditionsREST_APISs.response(400, 'Bad Request')
    def get(self,id):
        """Return the condition details items whose id is passed"""
        # Query
        condition = Conditions.query.filter_by(conditionId=id).first()
        # Serialize the data for the response
        conditionSchema = ConditionsSchema(many=False)
        data = conditionSchema.dump(condition).data
        log(data)
        return data

