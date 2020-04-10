from accounting.models import Bill
from rest_framework import serializers
from django.conf import settings


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

    def validate_paid_at(self, paid_at):
        if self.instance and (self.instance.paid_at != paid_at):
            raise serializers.ValidationError('Editing is not allowed.')
        return paid_at

    def create(self, validated_data):
        amount = validated_data.get('amount', 0)
        if amount[0] >= settings.ADD_AMOUNT_LIMIT:
            request = self.context.get("request")
            if request and hasattr(request, "user"):
                user = request.user
                user.note += f'\nAttempt to create bill with amount >= {settings.ADD_AMOUNT_LIMIT}'
                user.save()

            raise serializers.ValidationError({'amount': "Can't create amount bigger or equal 2400"})
        else:
            return super().create(validated_data)
