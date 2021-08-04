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
