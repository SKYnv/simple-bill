# Simple bills application (sample project)

check requirements.txt and runtime.txt

* add host and database to simple_billing.settings.production
* set env DJANGO_SETTINGS_MODULE=simple_billing.settings.production
* run: pip install -r requirements.txt
* run: ./manage.py migrate
* run: ./manage.py collectstatic
* run: ./manage.py runserver
