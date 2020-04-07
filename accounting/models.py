from django.db import models
from django.contrib.postgres.fields.jsonb import JSONField
from concurrency.fields import IntegerVersionField
from simple_history.models import HistoricalRecords
from launchlab_django_utils.models import UUIDTimestampedModel
from djmoney.models.fields import MoneyField
from accounting.managers import BillManager


class Bill(UUIDTimestampedModel):
    amount = MoneyField(decimal_places=4, max_digits=4)  # numeric 8,4
    due = models.DateTimeField()  # TODO set
    version = IntegerVersionField()
    user = models.ForeignKey('core.User', on_delete=models.DO_NOTHING)
    paid_at = models.DateTimeField(null=True)
    metadata = JSONField(default=dict)
    history = HistoricalRecords()

    objects = BillManager()

    class Meta:
        ordering = ('create_timestamp',)
