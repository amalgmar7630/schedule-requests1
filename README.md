# schedule-requests

# Please Follow these steps to setup the project:  

- Create a Virtual Environnment with Python 3.9.1

- Install PostgreSQL

- Install the backend requirements by rununing pip install -r requirememts.txt

- Set some customized environnement variables in setting.py file
       
       PASSWORD: 'postgres'
       USER: 'postgres'


- Run python manage.py makemigrations to create new migrations based on the changes you have made to your models

- Run python manage.py migrate to apply migrations

- Create Super User to affect specific features for him by running python manage.py createsuperuser

# Setup Celery

Install Redis as a Celery “Broker”:

First, install Redis from the official download page or via brew (brew install redis) and then turn to your terminal, in a new terminal window, fire up the server:

       $ redis-server

You can test that Redis is working properly by typing this into your terminal:

       $ redis-cli ping
       
Starting The Worker Process:

       celery worker -A config -l info -P threads
       
 # Run server
 
  python manage.py runserver
       

