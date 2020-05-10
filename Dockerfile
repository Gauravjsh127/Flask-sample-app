# Comments in Dockerfiles
#FROM python:3.5

#RUN apt-get -o Acquire::Check-Valid-Until=false update -y && \
#    apt-get install -y python-pip python-dev
FROM tiangolo/uwsgi-nginx-flask:python3.7

# We copy just the requirements.txt first to leverage Docker cache
COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

# Set environment variables
ENV FLASK_APP=conditions

# Expose the application's port
EXPOSE 5000

# prepopulate DB: optional step
#CMD python alertgenerator-microservice/pre_populate_alertdb.py

# Run the application
CMD ["flask", "run", "--host=0.0.0.0"]