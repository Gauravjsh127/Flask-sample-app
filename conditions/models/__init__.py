from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from flask_marshmallow import Marshmallow
import json

# initialize db
db = SQLAlchemy()
# Initialize Marshmallow
ma = Marshmallow()

