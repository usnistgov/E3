# E3

![GitHub repo size](https://img.shields.io/github/repo-size/usnistgov/E3)
![GitHub contributors](https://img.shields.io/github/contributors/usnistgov/E3)
![GitHub stars](https://img.shields.io/github/stars/usnistgov/E3?style=social)
![GitHub forks](https://img.shields.io/github/forks/usnistgov/E3?style=social)

E3, a project at NIST, is an API that performs complex economic analysis.


### Run with Docker
Ensure that docker and docker-compose are installed on your system.

Run with docker-compose:

    $ docker-compose build
    $ docker-compose up

This will run the django development server at http://localhost:8000/. PostgreSQL 
will be used as the database and RabbitMQ and a worker will be created for API
requests.


Note: If you are _running it for the first time_, you need to create a superuser:

1. Run the following command:
```
docker ps
```
2. From the output list, find your CONTAINER ID for the IMAGE `e3_api`. Then run the following commands:
```
docker exec -it [CONTAINER ID] bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```
3. Enter your email and password when prompted.

4. Go to `localhost:8000/login`, and login with your email and password.


5. Obtain your *unique API key* (Please COPY and store somewhere safe - you will only be shown this once).

6. Finally, navigate to:
```
http://localhost:8000/api/v1/analysis/?key=[YOUR_API_KEY]
```

You can now select 'media type', and paste your inputs in the 'contents' box, to send data to E3.

## Getting Started
Clone the repository from [Github](https://github.com/usnistgov/E3.git).

    $ git clone https://github.com/usnistgov/E3.git
    $ cd e3_django


### Run Locally
Activate the virtualenv for your project.

Install project dependencies:

    $ pip install -r requirements.txt

Then simply apply the migrations:

    $ python manage.py migrate

You can now run the development server:

    $ python manage.py runserver

## Technologies used
Python, Django, PostgreSQL, Docker
