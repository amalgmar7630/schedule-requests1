# schedule-requests

# Please Follow these steps to setup the project:  

- Create a Virtual Environnment with Python 3

- Install PostgreSQL

- Install the backend requirements by rununing pip install -r requirememts.txt

- Set some customized environnement variables in setting.py file
       
       PASSWORD: 'postgres'
       USER: 'postgres'


- Run python manage.py makemigrations to create new migrations based on the changes you have made to your models

- Run python manage.py migrate to apply migrations

- Create Super User to affect specific features for him by running python manage.py createsuperuser
