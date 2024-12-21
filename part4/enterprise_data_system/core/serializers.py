from rest_framework import serializers
from .models import (
    Customer, Account, Contract, CustomerFeedback,
    CallRecord, ChronicDiseaseRisk, ChurnPrediction,
    ProductRecommendation, LineOfBusiness
)

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = '__all__'

class CustomerFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerFeedback
        fields = '__all__'

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

class LineOfBusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = LineOfBusiness
        fields = '__all__'

class CustomerDetailSerializer(serializers.ModelSerializer):
    feedback = CustomerFeedbackSerializer(many=True, read_only=True)
    calls = CallRecordSerializer(many=True, read_only=True)
    disease_risks = ChronicDiseaseRiskSerializer(many=True, read_only=True)
    churn_predictions = ChurnPredictionSerializer(many=True, read_only=True)
    recommendations = ProductRecommendationSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = '__all__'
