# Boiler Plate Flask SQLAlchemy Marshmellog-Flask Flask-Migrate

## **Installation**

#### **Option 1. Using virtual env**
- After clone the repository and create virtual env

- Install dependency
    - ```sh
      pip install -r requirements.txt
        ```
- Run the flask app
    - ```sh
      flask --app app/app run --reload
        ```

#### **Option 2. Using Docker Container**
- Create Docker image base on provided Dockerfile
    - ```sh
      docker build -t <image tag> .
        ```
- Run Docker container
    - ```sh
      docker run -p 5000:5000 <image name, tag or id>
        ```

## **Usage**


- When Flask App running explore and interact with the API Docs in swagger using the route:
    - "http://0.0.0.0:5000/docs"# bp_python-flask-sqlalchemy-marshmellow-migrate
