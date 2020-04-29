from simple_billing.settings.base import *


APP_ENVIRONMENT = 'prod'

DEBUG = False

# fix it on prod environment
ALLOWED_HOSTS = ['*']
