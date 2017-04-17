del db.sqlite3
cd HNApp
rmdir migrations /s /Q
cd ../fullcalendar
rmdir migrations /s /Q
cd ../django_messages
rmdir migrations /s /Q
cd ..

python manage.py makemigrations HNApp
python manage.py makemigrations fullcalendar
python manage.py makemigrations django_messages
python manage.py migrate
python createAdmin.py
