from simple_billing.settings.base import *

try:
    from simple_billing.settings.local_dev import *
except ImportError:
    pass
