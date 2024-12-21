from django.db import models

class BillingAccount(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    name2 = models.CharField(max_length=255, null=True)
    group_num = models.CharField(max_length=20, null=False)
    tax_id = models.CharField(max_length=20, null=False)
    geo_code = models.IntegerField(null=False)
    online_billing = models.CharField(max_length=1, null=False)
    status = models.CharField(max_length=1, null=False)
    status_date = models.DateField(null=False)

    class Meta:
        db_table = 'billingaccount'
        indexes = [
            models.Index(fields=['status'], name='idx_billing_status'),
            models.Index(fields=['group_num'], name='idx_billing_group'),
            models.Index(fields=['geo_code'], name='idx_billing_geo_code'),
        ]

class BillingLocation(models.Model):
    billing = models.OneToOneField(BillingAccount, primary_key=True, on_delete=models.CASCADE, db_column='billing_id')
    address1 = models.CharField(max_length=255, null=False)
    address2 = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=100, null=False)
    state = models.CharField(max_length=100, null=False)
    zip = models.CharField(max_length=20, null=False)

    class Meta:
        db_table = 'billinglocation'
