from accounting.models import Bill
from rest_framework import viewsets
from api.accounting.serializers import BillSerializer
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.status import HTTP_405_METHOD_NOT_ALLOWED


class BillViewSet(viewsets.ModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    authentication_classes = (SessionAuthentication, )

    def get_queryset(self):
        return super().get_queryset()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.paid_at:
            return Response(data={'paid_at': 'Deleting is not allowed when paid_at is not null.'},
                            status=HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
