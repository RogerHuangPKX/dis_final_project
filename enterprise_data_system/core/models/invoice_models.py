from django.db import models
from .billing_models import BillingAccount
from .customer_models import Customer

class Invoice(models.Model):
    id = models.IntegerField(primary_key=True)
    invoice_num = models.CharField(max_length=20, unique=True)
    billing = models.ForeignKey(
        BillingAccount,
        on_delete=models.PROTECT,
        related_name='invoices'
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name='invoices'
    )
    paid_date = models.DateField(blank=True, null=True)
    due_date = models.DateField()
    run_date = models.DateField()

    class Meta:
        db_table = 'invoice'
        indexes = [
            models.Index(fields=['invoice_num']),
            models.Index(fields=['paid_date']),
            models.Index(fields=['due_date']),
            models.Index(fields=['run_date']),
        ]

    def __str__(self):
        return f"Invoice {self.invoice_num}"

    @property
    def is_paid(self):
        return self.paid_date is not None

    @property
    def is_overdue(self):
        from django.utils import timezone
        if self.is_paid:
            return False
        return self.due_date < timezone.now().date()

    def mark_as_paid(self):
        from django.utils import timezone
        self.paid_date = timezone.now().date()
        self.save()
