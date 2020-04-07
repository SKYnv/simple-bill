from django.db import models
from django.utils import timezone


class BillManager(models.Manager):
    """
        paid() - все Bill, с не пустым paid_at
        paid_by_cash() - то же, что и выше, но поле metadata должно содержать ключ/значение - “type”: “cash”
        paid_online() - то же, что и выше, но ключ/значение - “type”: “card”
        unpaid() - наоборот от paid()
        must_be_paid_today() - все неоплаченные (paid_at = NULL) Bill с due в сегодняшний день.
    """
    def get_queryset(self):
        return super().get_queryset()

    def paid(self):
        return self.get_queryset().filter(paid_at__isnull=False)

    def paid_by_cash(self):
        return self.paid().filter(metadata__contains={"type": "cash"})

    def paid_online(self):
        return self.paid().filter(metadata__contains={"type": "card"})

    def unpaid(self):
        return self.get_queryset().filter(paid_at__isnull=True)

    def must_be_paid_today(self):
        return self.unpaid().filter(due__day=timezone.now().day)
