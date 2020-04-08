from simple_billing.settings.base import *

try:
    from simple_billing.settings.local_dev import *
except ImportError:
    pass

APP_ENVIRONMENT = 'dev'

INSTALLED_APPS += [
    'rest_framework_swagger',
]
