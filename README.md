# Simple bills application

check requirements.txt and runtime.txt

* set env DJANGO_SETTINGS_MODULE=simple_billing.settings.production
* run: pip install -r requirements.txt
* run: ./manage.py migrate
* run: ./manage.py collectstatic
* run: ./manage.py runserver
