FROM python:3.9.5

WORKDIR /usr/src/app

RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic

EXPOSE 8000

CMD ["gunicorn", "-b 0.0.0.0:8000", "e3_django.wsgi"]
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]