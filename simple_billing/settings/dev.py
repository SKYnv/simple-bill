from simple_billing.settings.base import *
import dj_database_url

DATABASES['default'] = dj_database_url.parse('postgres://tkhmtkubjgzwen:42713467292853fd0bd359e093a3bb0fa1f2f57b0975171f310f2984e1cfa726@ec2-46-137-177-160.eu-west-1.compute.amazonaws.com:5432/dbee9845q071k')
