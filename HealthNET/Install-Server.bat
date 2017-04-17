pip3 install django-appconf --user
pip3 install pillow --user
python manage.py makemigrations HNApp
python manage.py makemigrations fullcalendar
python manage.py makemigrations django_messages
python manage.py migrate
python manage.py shell < createAdmin.py

