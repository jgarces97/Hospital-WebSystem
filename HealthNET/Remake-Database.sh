cd ~/Programs/HealthNet/HealthNET
rm db.sqlite3
cd HNApp 
rm -rf migrations
cd ../django_messages
rm -rf migrations
cd ../fullcalendar
rm -rf migrations
cd ..
python3 manage.py makemigrations HNApp
python3 manage.py makemigrations fullcalendar
python3 manage.py makemigrations django_messages
python3 manage.py migrate
python3 createAdmin.py

exit
