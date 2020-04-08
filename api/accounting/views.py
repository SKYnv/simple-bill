from accounting.models import Bill
from rest_framework import viewsets
from api.accounting.serializers import BillSerializer
from rest_framework.authentication import SessionAuthentication


class BillViewSet(viewsets.ModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    authentication_classes = (SessionAuthentication, )
    # lookup_field = 'uuid'

    def get_queryset(self):
        print(self.request)
        return super().get_queryset()
