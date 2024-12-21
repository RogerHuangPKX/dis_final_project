from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import (
    Customer, CustomerIdentity, Account, Contract, CustomerFeedback,
    CallRecord, ChronicDiseaseRisk, ChurnPrediction, LineOfBusiness,
    SeriesName, PlanName, ContractPayment
)
import random
from datetime import timedelta
import faker

fake = faker.Faker()

def generate_contract_num(index):
    """Generate a unique contract number"""
    return f"CNT{index:06d}"

def generate_ssn():
    """Generate a valid SSN format: XXX-XX-XXXX"""
    area = random.randint(1, 899)  # Area numbers 900-999 are not valid
    if area == 666:  # Skip 666 as it's not used
        area = 667
    group = random.randint(1, 99)
    serial = random.randint(1, 9999)
    return f"{area:03d}-{group:02d}-{serial:04d}"

def generate_phone():
    """Generate a valid US phone number format: (XXX) XXX-XXXX"""
    area_code = random.randint(200, 999)  # Valid area codes start with 2-9
    prefix = random.randint(200, 999)     # Valid prefix starts with 2-9
    line = random.randint(0, 9999)
    return f"({area_code:03d}) {prefix:03d}-{line:04d}"

def generate_date_in_past_year():
    """Generate a random date within the past year"""
    days_ago = random.randint(0, 364)  # 0 to 364 days ago
    return timezone.now() - timedelta(days=days_ago)

class Command(BaseCommand):
    help = 'Generate test data for the system'

    def handle(self, *args, **kwargs):
        self.stdout.write('Generating test data...')

        # Create business lines
        business_lines = [
            'Life Insurance',
            'Health Insurance',
            'Property Insurance',
            'Auto Insurance',
            'Investment Products'
        ]
        for name in business_lines:
            LineOfBusiness.objects.get_or_create(name=name)

        # Create series
        series_names = [
            'Premium Series',
            'Standard Series',
            'Basic Series',
            'Elite Series',
            'Value Series'
        ]
        for name in series_names:
            SeriesName.objects.get_or_create(name=name)

        # Create plans
        plan_names = [
            'Gold Plan',
            'Silver Plan',
            'Bronze Plan',
            'Platinum Plan',
            'Diamond Plan'
        ]
        for name in plan_names:
            PlanName.objects.get_or_create(name=name)

        # Generate 400 customers with their data
        for i in range(400):
            # Create customer
            start_date = fake.date_between(start_date='-5y', end_date='-1y')
            customer = Customer.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                gender=random.choice(['M', 'F']),
                language=random.choice(['English', 'Spanish', 'French']),
                start_date=start_date,
                status=random.choice(['A', 'P', 'I', 'S']),
                middle_init=random.choice(['A', 'B', 'C', 'D', None]),
                suffix=random.choice(['Jr.', 'Sr.', 'III', None]),
                salutation=random.choice(['Mr.', 'Mrs.', 'Ms.', 'Dr.', None])
            )

            # Create customer identity
            CustomerIdentity.objects.create(
                customer=customer,
                email=fake.email(),
                phone=generate_phone(),
                dob=fake.date_of_birth(minimum_age=18, maximum_age=80),
                ssn=generate_ssn(),
                ssn_type='S',
                withholding='N'
            )

            # Create account
            account = Account.objects.create(
                name=f"{customer.first_name} {customer.last_name} Account",
                company_code=1000 + i,
                tax_id=generate_ssn(),
                emp_count=random.randint(1, 100),
                status='A',
                status_date=timezone.now().date()
            )

            # Create contracts
            num_contracts = random.randint(1, 3)
            for j in range(num_contracts):
                contract_index = i * 3 + j
                contract = Contract.objects.create(
                    contract_num=generate_contract_num(contract_index),
                    account=account,
                    business=LineOfBusiness.objects.order_by('?').first(),
                    series=SeriesName.objects.order_by('?').first(),
                    plan=PlanName.objects.order_by('?').first(),
                    coverage=str(random.randint(50000, 1000000)),
                    duration=random.choice([12, 24, 36, 48, 60]),
                    status=random.choice(['A', 'P', 'E', 'C']),
                    status_date=timezone.now().date(),
                    in_force='Y',
                    language=customer.language
                )

                # Create contract payment
                ContractPayment.objects.create(
                    contract=contract,
                    bill_method=random.choice(['Monthly', 'Quarterly', 'Annually']),
                    premium=random.randint(100, 1000),
                    auto_loan=random.choice(['Y', 'N']),
                    payment_limit=random.randint(5000, 50000)
                )

            # Create feedback throughout the year
            num_feedbacks = random.randint(2, 4)  # 2-4 feedbacks per customer
            for _ in range(num_feedbacks):
                sentiment = random.uniform(0, 1)
                if sentiment > 0.7:
                    feedback_text = random.choice([
                        "Excellent service!",
                        "Very satisfied with the coverage.",
                        "Great customer support!",
                        "The claims process was smooth.",
                    ])
                    topics = ["service", "satisfaction"]
                elif sentiment > 0.3:
                    feedback_text = random.choice([
                        "Service was okay.",
                        "Coverage meets basic needs.",
                        "Response time could be better.",
                        "Reasonable prices but could improve service.",
                    ])
                    topics = ["service", "improvement"]
                else:
                    feedback_text = random.choice([
                        "Poor customer service.",
                        "Coverage is insufficient.",
                        "Claims process takes too long.",
                        "Premium is too high.",
                    ])
                    topics = ["service", "complaint"]

                CustomerFeedback.objects.create(
                    customer=customer,
                    feedback_text=feedback_text,
                    sentiment_score=sentiment,
                    key_topics=topics,
                    created_at=generate_date_in_past_year()
                )

            # Create call records throughout the year
            num_calls = random.randint(2, 5)  # 2-5 calls per customer
            for _ in range(num_calls):
                sentiment = random.uniform(0, 1)
                if sentiment > 0.7:
                    call_text = "Customer inquired about policy details. Very positive interaction."
                    topics = ["policy", "inquiry"]
                elif sentiment > 0.3:
                    call_text = "Customer requested policy modification. Standard interaction."
                    topics = ["policy", "modification"]
                else:
                    call_text = "Customer complained about service. Needs follow-up."
                    topics = ["service", "complaint"]

                CallRecord.objects.create(
                    customer=customer,
                    call_text=call_text,
                    duration=random.randint(60, 900),
                    call_time=generate_date_in_past_year(),
                    sentiment_score=sentiment,
                    key_topics=topics
                )

            # Create risk predictions
            ChronicDiseaseRisk.objects.create(
                customer=customer,
                risk_score=random.uniform(0, 1),
                risk_factors=random.sample(['age', 'lifestyle', 'medical_history', 'family_history'], 2),
                prediction_date=timezone.now(),
                confidence_score=random.uniform(0.7, 0.99)
            )

            ChurnPrediction.objects.create(
                customer=customer,
                churn_probability=random.uniform(0, 1),
                contributing_factors=random.sample([
                    'price_sensitivity',
                    'competitor_offers',
                    'service_satisfaction',
                    'claim_history',
                    'payment_history'
                ], 2),
                prediction_date=timezone.now()
            )

        self.stdout.write(self.style.SUCCESS('Successfully generated test data'))
