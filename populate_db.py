import os
from datetime import datetime

from conditions.models.conditionModel import Conditions, db   # Database models
from conditions import conditions  # app config

# Initialize Database
conditionsList = [
]

# Delete database file if it exists currently
if os.path.exists("condtions.db"):
    os.remove("condtions.db")


with conditions.test_request_context():
    db.create_all()

    # iterate over the CONDITIONS list and populate the database
    for conditions in conditionsList:
        conditionCreated = Conditions(name=conditions.get("name"), description=conditions.get("description"))
        db.session.add(conditionCreated)
        
    db.session.commit()