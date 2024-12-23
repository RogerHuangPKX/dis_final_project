# Generated by Django 4.2.17 on 2024-12-21 04:03

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('name2', models.CharField(max_length=255, null=True)),
                ('company_code', models.IntegerField()),
                ('tax_id', models.CharField(max_length=20)),
                ('emp_count', models.IntegerField()),
                ('status', models.CharField(max_length=1)),
                ('status_date', models.DateField()),
            ],
            options={
                'db_table': 'account',
            },
        ),
        migrations.CreateModel(
            name='BillingAccount',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('name2', models.CharField(max_length=255, null=True)),
                ('group_num', models.CharField(max_length=20)),
                ('tax_id', models.CharField(max_length=20)),
                ('geo_code', models.IntegerField()),
                ('online_billing', models.CharField(max_length=1)),
                ('status', models.CharField(max_length=1)),
                ('status_date', models.DateField()),
            ],
            options={
                'db_table': 'billingaccount',
            },
        ),
        migrations.CreateModel(
            name='CallRecord',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('call_text', models.TextField()),
                ('duration', models.IntegerField()),
                ('call_time', models.DateTimeField()),
                ('sentiment_score', models.FloatField()),
                ('key_topics', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), size=None)),
            ],
            options={
                'db_table': 'callrecord',
            },
        ),
        migrations.CreateModel(
            name='ChronicDiseaseRisk',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('risk_score', models.FloatField()),
                ('risk_factors', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), size=None)),
                ('prediction_date', models.DateTimeField()),
                ('confidence_score', models.FloatField()),
            ],
            options={
                'db_table': 'chronicdiseaserisk',
            },
        ),
        migrations.CreateModel(
            name='ChurnPrediction',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('churn_probability', models.FloatField()),
                ('contributing_factors', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), size=None)),
                ('prediction_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'churnprediction',
            },
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('contract_num', models.CharField(max_length=20, unique=True)),
                ('status', models.CharField(max_length=1)),
                ('status_date', models.DateField()),
                ('coverage', models.CharField(max_length=50)),
                ('in_force', models.CharField(max_length=1)),
                ('language', models.CharField(max_length=50)),
                ('duration', models.IntegerField()),
            ],
            options={
                'db_table': 'contract',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('last_name', models.CharField(max_length=100)),
                ('first_name', models.CharField(max_length=100)),
                ('middle_init', models.CharField(max_length=1, null=True)),
                ('suffix', models.CharField(max_length=10, null=True)),
                ('salutation', models.CharField(max_length=10, null=True)),
                ('gender', models.CharField(max_length=1)),
                ('language', models.CharField(max_length=50)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(null=True)),
            ],
            options={
                'db_table': 'customer',
            },
        ),
        migrations.CreateModel(
            name='DataUpdateLog',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('table_name', models.CharField(max_length=100)),
                ('operation', models.CharField(max_length=20)),
                ('record_count', models.IntegerField()),
                ('processed_at', models.DateTimeField(auto_now_add=True)),
                ('requires_retraining', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'dataupdatelog',
            },
        ),
        migrations.CreateModel(
            name='LineOfBusiness',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'db_table': 'lineofbusiness',
            },
        ),
        migrations.CreateModel(
            name='MLModelTrainingJob',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('model_type', models.CharField(max_length=20)),
                ('status', models.CharField(max_length=20)),
                ('started_at', models.DateTimeField(auto_now_add=True)),
                ('completed_at', models.DateTimeField(null=True)),
                ('error_message', models.TextField(null=True)),
                ('metrics', models.JSONField(null=True)),
            ],
            options={
                'db_table': 'mlmodeltrainingjob',
            },
        ),
        migrations.CreateModel(
            name='PlanName',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'db_table': 'planname',
            },
        ),
        migrations.CreateModel(
            name='SeriesName',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'db_table': 'seriesname',
            },
        ),
        migrations.CreateModel(
            name='AccountLocation',
            fields=[
                ('account', models.OneToOneField(db_column='account_id', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='core.account')),
                ('address1', models.CharField(max_length=255)),
                ('address2', models.CharField(max_length=255, null=True)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('zip', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'accountlocation',
            },
        ),
        migrations.CreateModel(
            name='BillingLocation',
            fields=[
                ('billing', models.OneToOneField(db_column='billing_id', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='core.billingaccount')),
                ('address1', models.CharField(max_length=255)),
                ('address2', models.CharField(max_length=255, null=True)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('zip', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'billinglocation',
            },
        ),
        migrations.CreateModel(
            name='ContractBankAccount',
            fields=[
                ('contract', models.OneToOneField(db_column='contract_id', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='core.contract')),
                ('transit_num', models.CharField(max_length=20)),
                ('account_type', models.CharField(max_length=50)),
                ('account_num', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'contractbankaccount',
            },
        ),
        migrations.CreateModel(
            name='ContractCreditCard',
            fields=[
                ('contract', models.OneToOneField(db_column='contract_id', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='core.contract')),
                ('card_num', models.CharField(max_length=20)),
                ('exp_date', models.DateField()),
                ('card_type', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'contractcreditcard',
            },
        ),
        migrations.CreateModel(
            name='ContractPayment',
            fields=[
                ('contract', models.OneToOneField(db_column='contract_id', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='core.contract')),
                ('bill_method', models.CharField(max_length=50)),
                ('premium', models.DecimalField(decimal_places=2, max_digits=10)),
                ('auto_loan', models.CharField(max_length=1)),
                ('payment_limit', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'db_table': 'contractpayment',
            },
        ),
        migrations.CreateModel(
            name='CustomerIdentity',
            fields=[
                ('customer', models.OneToOneField(db_column='customer_id', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='core.customer')),
                ('dob', models.DateField()),
                ('ssn', models.CharField(max_length=11)),
                ('ssn_type', models.CharField(max_length=1)),
                ('legacy_id', models.CharField(max_length=20, null=True)),
                ('withholding', models.CharField(max_length=1)),
                ('email', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'customeridentity',
            },
        ),
        migrations.CreateModel(
            name='ProductRecommendation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('recommendation_score', models.FloatField()),
                ('recommendation_date', models.DateTimeField()),
                ('customer', models.ForeignKey(db_column='customer_id', on_delete=django.db.models.deletion.CASCADE, to='core.customer')),
                ('plan', models.ForeignKey(db_column='plan_id', on_delete=django.db.models.deletion.CASCADE, to='core.planname')),
            ],
            options={
                'db_table': 'productrecommendation',
            },
        ),
        migrations.CreateModel(
            name='MLModelVersion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('model_type', models.CharField(max_length=20)),
                ('version', models.CharField(max_length=50)),
                ('accuracy', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('model_path', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=False)),
                ('metadata', models.JSONField(null=True)),
            ],
            options={
                'db_table': 'mlmodelversion',
                'unique_together': {('model_type', 'version')},
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('invoice_num', models.CharField(max_length=20, unique=True)),
                ('paid_date', models.DateField(blank=True, null=True)),
                ('due_date', models.DateField()),
                ('run_date', models.DateField()),
                ('billing', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='invoices', to='core.billingaccount')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='invoices', to='core.customer')),
            ],
            options={
                'db_table': 'invoice',
            },
        ),
        migrations.CreateModel(
            name='CustomerFeedback',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('feedback_text', models.TextField()),
                ('sentiment_score', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('key_topics', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), size=None)),
                ('customer', models.ForeignKey(db_column='customer_id', on_delete=django.db.models.deletion.CASCADE, to='core.customer')),
            ],
            options={
                'db_table': 'customerfeedback',
            },
        ),
        migrations.AddIndex(
            model_name='customer',
            index=models.Index(fields=['last_name', 'first_name'], name='idx_customer_name'),
        ),
        migrations.AddIndex(
            model_name='customer',
            index=models.Index(fields=['start_date', 'end_date'], name='idx_customer_dates'),
        ),
        migrations.AddField(
            model_name='contract',
            name='account',
            field=models.ForeignKey(db_column='account_id', on_delete=django.db.models.deletion.CASCADE, to='core.account'),
        ),
        migrations.AddField(
            model_name='contract',
            name='business',
            field=models.ForeignKey(db_column='business_id', on_delete=django.db.models.deletion.CASCADE, to='core.lineofbusiness'),
        ),
        migrations.AddField(
            model_name='contract',
            name='plan',
            field=models.ForeignKey(db_column='plan_id', on_delete=django.db.models.deletion.CASCADE, to='core.planname'),
        ),
        migrations.AddField(
            model_name='contract',
            name='series',
            field=models.ForeignKey(db_column='series_id', on_delete=django.db.models.deletion.CASCADE, to='core.seriesname'),
        ),
        migrations.AddField(
            model_name='churnprediction',
            name='customer',
            field=models.ForeignKey(db_column='customer_id', on_delete=django.db.models.deletion.CASCADE, to='core.customer'),
        ),
        migrations.AddField(
            model_name='chronicdiseaserisk',
            name='customer',
            field=models.ForeignKey(db_column='customer_id', on_delete=django.db.models.deletion.CASCADE, to='core.customer'),
        ),
        migrations.AddField(
            model_name='callrecord',
            name='customer',
            field=models.ForeignKey(db_column='customer_id', on_delete=django.db.models.deletion.CASCADE, to='core.customer'),
        ),
        migrations.AddIndex(
            model_name='billingaccount',
            index=models.Index(fields=['status'], name='idx_billing_status'),
        ),
        migrations.AddIndex(
            model_name='billingaccount',
            index=models.Index(fields=['group_num'], name='idx_billing_group'),
        ),
        migrations.AddIndex(
            model_name='billingaccount',
            index=models.Index(fields=['geo_code'], name='idx_billing_geo_code'),
        ),
        migrations.AddIndex(
            model_name='account',
            index=models.Index(fields=['status'], name='idx_account_status'),
        ),
        migrations.AddIndex(
            model_name='account',
            index=models.Index(fields=['company_code'], name='idx_account_company'),
        ),
        migrations.AddIndex(
            model_name='productrecommendation',
            index=models.Index(fields=['recommendation_score'], name='idx_recommendation'),
        ),
        migrations.AddIndex(
            model_name='productrecommendation',
            index=models.Index(fields=['recommendation_date'], name='idx_recommendation_date'),
        ),
        migrations.AddIndex(
            model_name='invoice',
            index=models.Index(fields=['invoice_num'], name='invoice_invoice_709111_idx'),
        ),
        migrations.AddIndex(
            model_name='invoice',
            index=models.Index(fields=['paid_date'], name='invoice_paid_da_7c8dbe_idx'),
        ),
        migrations.AddIndex(
            model_name='invoice',
            index=models.Index(fields=['due_date'], name='invoice_due_dat_ee8b9c_idx'),
        ),
        migrations.AddIndex(
            model_name='invoice',
            index=models.Index(fields=['run_date'], name='invoice_run_dat_77ecd1_idx'),
        ),
        migrations.AddIndex(
            model_name='customerfeedback',
            index=models.Index(fields=['sentiment_score'], name='idx_feedback_sentiment'),
        ),
        migrations.AddIndex(
            model_name='customerfeedback',
            index=models.Index(fields=['created_at'], name='idx_feedback_created'),
        ),
        migrations.AddIndex(
            model_name='contract',
            index=models.Index(fields=['contract_num'], name='idx_contract_num'),
        ),
        migrations.AddIndex(
            model_name='contract',
            index=models.Index(fields=['status'], name='idx_contract_status'),
        ),
        migrations.AddIndex(
            model_name='churnprediction',
            index=models.Index(fields=['churn_probability'], name='idx_churn_prob'),
        ),
        migrations.AddIndex(
            model_name='churnprediction',
            index=models.Index(fields=['prediction_date'], name='idx_churn_prediction'),
        ),
        migrations.AddIndex(
            model_name='chronicdiseaserisk',
            index=models.Index(fields=['risk_score'], name='idx_risk_score'),
        ),
        migrations.AddIndex(
            model_name='chronicdiseaserisk',
            index=models.Index(fields=['prediction_date'], name='idx_disease_prediction'),
        ),
        migrations.AddIndex(
            model_name='callrecord',
            index=models.Index(fields=['call_time'], name='idx_call_time'),
        ),
        migrations.AddIndex(
            model_name='callrecord',
            index=models.Index(fields=['sentiment_score'], name='idx_call_sentiment'),
        ),
    ]
