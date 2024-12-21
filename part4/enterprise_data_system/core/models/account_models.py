from django.db import models

class Account(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    name2 = models.CharField(max_length=255, null=True)
    company_code = models.IntegerField(null=False)
    tax_id = models.CharField(max_length=20, null=False)
    emp_count = models.IntegerField(null=False)
    status = models.CharField(max_length=1, null=False)
    status_date = models.DateField(null=False)

    class Meta:
        db_table = 'account'
        indexes = [
            models.Index(fields=['status'], name='idx_account_status'),
            models.Index(fields=['company_code'], name='idx_account_company'),
        ]

class AccountLocation(models.Model):
    account = models.OneToOneField(Account, primary_key=True, on_delete=models.CASCADE, db_column='account_id')
    address1 = models.CharField(max_length=255, null=False)
    address2 = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=100, null=False)
    state = models.CharField(max_length=100, null=False)
    zip = models.CharField(max_length=20, null=False)

    class Meta:
        db_table = 'accountlocation'
