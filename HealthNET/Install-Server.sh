pip3 install django-appconf --user
pip3 install pillow --user
python3 manage.py makemigrations HNApp
python3 manage.py makemigrations fullcalendar
python3 manage.py makemigrations django_messages
python3 manage.py migrate
python3 manage.py shell < createAdmin.py