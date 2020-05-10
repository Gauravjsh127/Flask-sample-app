"""
Execute the conditions microservice
"""

from conditions import CONDITIONS

if __name__ == "__main__":
    CONDITIONS.run(port=5002, debug=True)