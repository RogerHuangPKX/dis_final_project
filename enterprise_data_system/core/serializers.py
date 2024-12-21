from django.utils import timezone
from rest_framework import serializers
from .models import (
    Customer, Account, Contract, CustomerFeedback,
    CallRecord, ChronicDiseaseRisk, ChurnPrediction,
    ProductRecommendation, LineOfBusiness, CustomerIdentity,
    Invoice, BillingAccount, ContractPayment
)

class CustomerIdentitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerIdentity
        fields = ['email', 'phone', 'dob']

class CustomerSerializer(serializers.ModelSerializer):
    identity = CustomerIdentitySerializer(source='customeridentity', read_only=True)
    name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'phone', 'identity', 'gender', 'language', 'start_date', 'status']

    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def get_email(self, obj):
        return obj.customeridentity.email if hasattr(obj, 'customeridentity') else None

    def get_phone(self, obj):
        return obj.customeridentity.phone if hasattr(obj, 'customeridentity') else None

    def get_status(self, obj):
        status_map = {
            'A': 'Active',
            'P': 'Pending',
            'I': 'Inactive',
            'S': 'Suspended'
        }
        return status_map.get(obj.status, 'Unknown')

class LineOfBusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = LineOfBusiness
        fields = '__all__'

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

class ContractPaymentSerializer(serializers.Serializer):
    bill_method = serializers.CharField()
    premium = serializers.FloatField()
    auto_loan = serializers.CharField()

class ContractSerializer(serializers.ModelSerializer):
    customer = serializers.SerializerMethodField()
    business = LineOfBusinessSerializer(read_only=True)
    premium = serializers.SerializerMethodField()
    customer_id = serializers.IntegerField(write_only=True)
    payment = ContractPaymentSerializer(write_only=True)

    class Meta:
        model = Contract
        fields = ['id', 'contract_num', 'customer', 'customer_id', 'business', 'coverage', 
                 'duration', 'status', 'status_date', 'premium', 'payment']

    def get_premium(self, obj):
        try:
            return float(obj.contractpayment.premium)
        except (AttributeError, Contract.contractpayment.RelatedObjectDoesNotExist):
            return 0.0

    def get_customer(self, obj):
        return obj.account.name if obj.account else "Unknown Account"

    def create(self, validated_data):
        customer_id = validated_data.pop('customer_id')
        payment_data = validated_data.pop('payment')
        
        # Get or create account for customer
        customer = Customer.objects.get(id=customer_id)
        account, _ = Account.objects.get_or_create(
            name=f"{customer.first_name} {customer.last_name} Account",
            defaults={
                'company_code': customer_id + 1000,
                'tax_id': '000-00-0000',
                'emp_count': 1,
                'status': 'A',
                'status_date': timezone.now().date()
            }
        )
        
        # Create contract
        contract = Contract.objects.create(
            account=account,
            **validated_data
        )
        
        # Create contract payment
        ContractPayment.objects.create(
            contract=contract,
            **payment_data
        )
        
        return contract

class CustomerFeedbackSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()
    customer_email = serializers.SerializerMethodField()

    class Meta:
        model = CustomerFeedback
        fields = ['id', 'customer', 'customer_name', 'customer_email', 'feedback_text', 
                 'sentiment_score', 'key_topics', 'created_at']

    def get_customer_name(self, obj):
        return f"{obj.customer.first_name} {obj.customer.last_name}"

    def get_customer_email(self, obj):
        return obj.customer.customeridentity.email if hasattr(obj.customer, 'customeridentity') else None

class CallRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallRecord
        fields = '__all__'

class ChronicDiseaseRiskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChronicDiseaseRisk
        fields = '__all__'

class ChurnPredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChurnPrediction
        fields = '__all__'

class ProductRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductRecommendation
        fields = '__all__'

class CustomerDetailSerializer(serializers.ModelSerializer):
    identity = CustomerIdentitySerializer(source='customeridentity', read_only=True)
    feedback = CustomerFeedbackSerializer(many=True, read_only=True)
    calls = CallRecordSerializer(many=True, read_only=True)
    disease_risks = ChronicDiseaseRiskSerializer(many=True, read_only=True)
    churn_predictions = ChurnPredictionSerializer(many=True, read_only=True)
    recommendations = ProductRecommendationSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = '__all__'
