from django.db import models

class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=100, null=False)
    first_name = models.CharField(max_length=100, null=False)
    middle_init = models.CharField(max_length=1, null=True)
    suffix = models.CharField(max_length=10, null=True)
    salutation = models.CharField(max_length=10, null=True)
    gender = models.CharField(max_length=1, null=False)
    language = models.CharField(max_length=50, null=False)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=True)

    class Meta:
        db_table = 'customer'
        indexes = [
            models.Index(fields=['last_name', 'first_name'], name='idx_customer_name'),
            models.Index(fields=['start_date', 'end_date'], name='idx_customer_dates'),
        ]

class CustomerIdentity(models.Model):
    customer = models.OneToOneField(Customer, primary_key=True, on_delete=models.CASCADE, db_column='customer_id')
    dob = models.DateField(null=False)
    ssn = models.CharField(max_length=11, null=False)
    ssn_type = models.CharField(max_length=1, null=False)
    legacy_id = models.CharField(max_length=20, null=True)
    withholding = models.CharField(max_length=1, null=False)
    email = models.CharField(max_length=255, null=False)

    class Meta:
        db_table = 'customeridentity'
