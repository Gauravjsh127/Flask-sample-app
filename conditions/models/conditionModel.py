import datetime
from datetime import datetime
import enum
from . import db, ma
from marshmallow import fields, Schema
from marshmallow_enum import EnumField
from flask_restplus import fields

CONDTION_ITEM_DB = {
    'conditionId': fields.Integer(required=True, description='Condition Id', example=1),
    'name': fields.String(required=True, description='Condition name', example='condition1'),
    'description': fields.String(required=True, description='description', example='this is a harsh condition'),
    'createdTime': fields.DateTime(required=True, description='Created time', example="2018-12-19 09:26:03.478039"),
    'lastUpdatedTime': fields.DateTime(required=True, description='Last updated time', example="2018-12-19 09:26:03.478039")
}

class Conditions(db.Model):
    __tablename__ = 'Conditions'

    conditionId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32),nullable=False)
    description=db.Column(db.String(256), nullable=False)
    createdTime = db.Column(db.DateTime, default=datetime.now())
    lastUpdatedTime = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

class ConditionsSchema(ma.ModelSchema):
    class Meta:
        model = Conditions
        sqla_session = db.session
