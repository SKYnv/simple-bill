from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('bills/', include('api.accounting.urls'))
]

if settings.APP_ENVIRONMENT == 'dev':
    from rest_framework_swagger.views import get_swagger_view
    schema_view = get_swagger_view(title='API')

    urlpatterns.append(path('', schema_view))