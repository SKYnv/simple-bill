from accounting.models import Bill
from rest_framework import serializers


class MoneySerializer(serializers.Serializer):
    amount = serializers.FloatField(required=True, min_value=0)
    currency = serializers.CharField(default='USD', required=False)

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        return data.get('amount', 0), data.get('currency', 'USD')


class BillSerializer(serializers.ModelSerializer):
    amount = MoneySerializer()

    class Meta:
        model = Bill
        fields = '__all__'
        read_only_fields = ('amount',)
