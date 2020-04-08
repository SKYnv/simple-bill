from api.accounting.views import BillViewSet
from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()
router.register('', BillViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
