FROM python:3.11

# set working diretory
WORKDIR /flaskapp

# copy requirements.txt and install
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Copy Flask application code
COPY . .

# Execute
CMD exec gunicorn --bind 0.0.0.0:8000 app.app:app