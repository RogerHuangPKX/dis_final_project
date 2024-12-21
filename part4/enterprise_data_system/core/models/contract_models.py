from django.db import models

class LineOfBusiness(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True, null=False)

    class Meta:
        db_table = 'lineofbusiness'

    def __str__(self):
        return self.name

class SeriesName(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True, null=False)

    class Meta:
        db_table = 'seriesname'

    def __str__(self):
        return self.name

class PlanName(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True, null=False)

    class Meta:
        db_table = 'planname'

    def __str__(self):
        return self.name

class Contract(models.Model):
    id = models.AutoField(primary_key=True)
    contract_num = models.CharField(max_length=20, unique=True, null=False)
    business = models.ForeignKey(LineOfBusiness, on_delete=models.CASCADE, db_column='business_id', null=False)
    series = models.ForeignKey(SeriesName, on_delete=models.CASCADE, db_column='series_id', null=False)
    plan = models.ForeignKey(PlanName, on_delete=models.CASCADE, db_column='plan_id', null=False)
    status = models.CharField(max_length=1, null=False)
    status_date = models.DateField(null=False)
    coverage = models.CharField(max_length=50, null=False)
    account = models.ForeignKey('Account', on_delete=models.CASCADE, db_column='account_id', null=False)
    in_force = models.CharField(max_length=1, null=False)
    language = models.CharField(max_length=50, null=False)
    duration = models.IntegerField(null=False)

    class Meta:
        db_table = 'contract'
        indexes = [
            models.Index(fields=['contract_num'], name='idx_contract_num'),
            models.Index(fields=['status'], name='idx_contract_status'),
        ]

class ContractPayment(models.Model):
    contract = models.OneToOneField(Contract, primary_key=True, on_delete=models.CASCADE, db_column='contract_id')
    bill_method = models.CharField(max_length=50, null=False)
    premium = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    auto_loan = models.CharField(max_length=1, null=False)
    payment_limit = models.DecimalField(max_digits=10, decimal_places=2, null=False)

    class Meta:
        db_table = 'contractpayment'

class ContractBankAccount(models.Model):
    contract = models.OneToOneField(Contract, primary_key=True, on_delete=models.CASCADE, db_column='contract_id')
    transit_num = models.CharField(max_length=20, null=False)
    account_type = models.CharField(max_length=50, null=False)
    account_num = models.CharField(max_length=20, null=False)

    class Meta:
        db_table = 'contractbankaccount'

class ContractCreditCard(models.Model):
    contract = models.OneToOneField(Contract, primary_key=True, on_delete=models.CASCADE, db_column='contract_id')
    card_num = models.CharField(max_length=20, null=False)
    exp_date = models.DateField(null=False)
    card_type = models.CharField(max_length=50, null=False)

    class Meta:
        db_table = 'contractcreditcard'
