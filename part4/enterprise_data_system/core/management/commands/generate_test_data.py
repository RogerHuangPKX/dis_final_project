from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.utils import timezone
from faker import Faker
from core.models import (
    Account, Customer, CustomerIdentity, Contract, CustomerFeedback,
    CallRecord, ChronicDiseaseRisk, ChurnPrediction,
    ProductRecommendation, LineOfBusiness, SeriesName, PlanName
)
import random

fake = Faker()

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        self.create_user_roles()
        self.create_test_data()

    def create_user_roles(self):
        roles = {
            'system_admin': ['Can view analytics', 'Can manage users'],
            'insurance_agent': ['Can view customers', 'Can create quotes'],
            'data_analyst': ['Can view analytics', 'Can view reports'],
            'sales_manager': ['Can approve contracts', 'Can view analytics']
        }

        for role, permissions in roles.items():
            group, _ = Group.objects.get_or_create(name=role)
            if not User.objects.filter(username=role).exists():
                user = User.objects.create_user(
                    username=role,
                    email=f'{role}@example.com',
                    password=role
                )
                group.user_set.add(user)

    def create_test_data(self):
        # Create test businesses
        businesses = ['Life', 'Health', 'Property']
        for business in businesses:
            LineOfBusiness.objects.get_or_create(name=business)

        # Create test series
        series = ['Basic', 'Premium', 'Elite']
        for s in series:
            SeriesName.objects.get_or_create(name=s)

        # Create test plans
        plans = ['Individual', 'Family', 'Corporate']
        for p in plans:
            PlanName.objects.get_or_create(name=p)

        for _ in range(50):
            customer = Customer.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                gender=random.choice(['M', 'F']),
                language='EN',
                start_date=timezone.now()
            )

            CustomerIdentity.objects.create(
                customer=customer,
                dob=fake.date_of_birth(),
                ssn=fake.ssn(),
                ssn_type='S',
                withholding='Y',
                email=fake.email()
            )

            account = Account.objects.create(
                name=f"{customer.first_name} {customer.last_name}",
                company_code=random.randint(1000, 9999),
                tax_id=fake.ein(),
                emp_count=random.randint(1, 1000),
                status='A',
                status_date=timezone.now()
            )

            for _ in range(random.randint(1, 3)):
                contract = Contract.objects.create(
                    contract_num=f"CNT{random.randint(10000, 99999)}",
                    business=LineOfBusiness.objects.order_by('?').first(),
                    series=SeriesName.objects.order_by('?').first(),
                    plan=PlanName.objects.order_by('?').first(),
                    status=random.choice(['A', 'P', 'E']),  # Active, Pending, Expired
                    status_date=timezone.now(),
                    coverage=str(random.randint(50000, 1000000)),
                    duration=random.randint(1, 30),
                    account=account,
                    in_force='Y',
                    language='EN'
                )

            for _ in range(random.randint(2, 5)):
                CustomerFeedback.objects.create(
                    customer=customer,
                    feedback_text=fake.text(),
                    sentiment_score=random.uniform(0, 1),
                    key_topics=['service', 'price', 'coverage']
                )

            CallRecord.objects.create(
                customer=customer,
                call_text=fake.text(),
                duration=random.randint(60, 900),
                call_time=timezone.now(),
                sentiment_score=random.uniform(0, 1),
                key_topics=['inquiry', 'complaint', 'support']
            )

            ChronicDiseaseRisk.objects.create(
                customer=customer,
                risk_score=random.uniform(0, 1),
                risk_factors=['age', 'lifestyle', 'history'],
                prediction_date=timezone.now(),
                confidence_score=random.uniform(0.7, 1)
            )

            ChurnPrediction.objects.create(
                customer=customer,
                churn_probability=random.uniform(0, 1),
                contributing_factors=['contract_duration', 'claims', 'satisfaction'],
                prediction_date=timezone.now()
            )

            ProductRecommendation.objects.create(
                customer=customer,
                plan=PlanName.objects.order_by('?').first(),
                recommendation_score=random.uniform(0.5, 1),
                recommendation_date=timezone.now()
            )

        self.stdout.write(self.style.SUCCESS('Successfully generated test data'))
