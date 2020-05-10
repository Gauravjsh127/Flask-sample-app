"""
 This is a library covers the common methods.
"""

import datetime


def log(message):
    """
    Naive debug printer
    """
    print(str(datetime.datetime.now()) + ": " + str(message))