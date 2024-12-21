from django.db.models import Avg, Sum
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import (
    Customer, Contract, CustomerFeedback, CallRecord,
    ChronicDiseaseRisk, ChurnPrediction, ProductRecommendation
)
from .serializers import (
    CustomerSerializer, ContractSerializer,
    CustomerFeedbackSerializer, CallRecordSerializer
)
from .ml.predict import PredictionService
from .permissions import RoleBasedPermission, role_required

prediction_service = PredictionService()

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [RoleBasedPermission]
    required_roles = {
        'list': ['admin', 'analyst', 'agent'],
        'create': ['admin', 'agent'],
        'retrieve': ['admin', 'analyst', 'agent'],
        'update': ['admin', 'agent'],
        'destroy': ['admin'],
        'risk_analysis': ['admin', 'analyst'],
        'calculate_quote': ['agent']
    }

    def get_customer_stats(self, customer):
        """Get aggregated customer statistics"""
        contracts = Contract.objects.filter(account__customer=customer)
        feedback = CustomerFeedback.objects.filter(customer=customer)
        calls = CallRecord.objects.filter(customer=customer)
        
        avg_sentiment = feedback.aggregate(Avg('sentiment_score'))['sentiment_score__avg']
        total_premium = contracts.aggregate(Sum('premium'))['premium__sum']
        total_coverage = contracts.aggregate(Sum('coverage'))['coverage__sum']
        
        return {
            'contracts_count': contracts.count(),
            'claims_count': contracts.filter(status='claimed').count(),
            'avg_sentiment': avg_sentiment if avg_sentiment is not None else 0.5,
            'complaints_count': feedback.filter(sentiment_score__lt=0.3).count(),
            'delayed_payments': contracts.filter(status='delayed').count(),
            'avg_premium': total_premium / contracts.count() if contracts.count() > 0 else 0,
            'total_coverage': total_coverage if total_coverage is not None else 0
        }

    @action(detail=True, methods=['get'])
    def risk_analysis(self, request, pk=None):
        """Get comprehensive risk analysis for a customer"""
        customer = self.get_object()
        stats = self.get_customer_stats(customer)
        
        customer_data = {
            'age': customer.age,
            'income': customer.income,
            'years_as_customer': (timezone.now().date() - customer.start_date).days / 365,
            'num_products': stats['contracts_count'],
            'total_claims': stats['claims_count'],
            'avg_sentiment': stats['avg_sentiment'],
            'num_complaints': stats['complaints_count'],
            'payment_delay': stats['delayed_payments'],
            'premium': stats['avg_premium'],
            'coverage': stats['total_coverage'],
            'risk_tolerance': customer.risk_profile,
            'family_size': customer.family_size,
            'employment_status': customer.employment_status
        }
        
        disease_risk = prediction_service.predict_disease_risk(customer_data)
        churn_risk = prediction_service.predict_churn_risk(customer_data)
        recommendations = prediction_service.get_product_recommendations(customer_data)
        
        return Response({
            'customer_id': customer.id,
            'customer_stats': stats,
            'disease_risk': disease_risk,
            'churn_risk': churn_risk,
            'recommendations': recommendations
        })

    @action(detail=True, methods=['post'])
    def calculate_quote(self, request, pk=None):
        """Calculate insurance quote based on customer risk profile"""
        customer = self.get_object()
        stats = self.get_customer_stats(customer)
        
        customer_data = {
            'age': customer.age,
            'income': customer.income,
            'years_as_customer': (timezone.now().date() - customer.start_date).days / 365,
            'num_products': stats['contracts_count'],
            'total_claims': stats['claims_count'],
            'premium': request.data.get('base_premium', 1000),
            'coverage': request.data.get('coverage', 100000)
        }
        
        disease_risk = prediction_service.predict_disease_risk(customer_data)
        churn_risk = prediction_service.predict_churn_risk(customer_data)
        
        base_premium = float(request.data.get('base_premium', 1000))
        risk_factor = 1 + (disease_risk['risk_score'] * 0.5)  # Up to 50% increase for high risk
        loyalty_discount = 0.1 if churn_risk['churn_probability'] < 0.3 else 0  # 10% loyalty discount
        
        final_premium = base_premium * risk_factor * (1 - loyalty_discount)
        
        return Response({
            'customer_id': customer.id,
            'base_premium': base_premium,
            'risk_factor': risk_factor,
            'loyalty_discount': loyalty_discount,
            'final_premium': final_premium,
            'risk_assessment': {
                'disease_risk': disease_risk,
                'churn_risk': churn_risk
            }
        })

class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [RoleBasedPermission]
    required_roles = {
        'list': ['admin', 'analyst', 'agent'],
        'create': ['admin', 'agent'],
        'retrieve': ['admin', 'analyst', 'agent'],
        'update': ['admin', 'agent'],
        'destroy': ['admin'],
        'analytics': ['admin', 'analyst']
    }

    @action(detail=False, methods=['get'])
    def analytics(self, request):
        """Get contract analytics and insights"""
        total_contracts = Contract.objects.count()
        active_contracts = Contract.objects.filter(status='active').count()
        total_premium = Contract.objects.filter(status='active').aggregate(Sum('premium'))['premium__sum']
        avg_duration = Contract.objects.aggregate(Avg('duration'))['duration__avg']
        
        return Response({
            'total_contracts': total_contracts,
            'active_contracts': active_contracts,
            'total_premium': total_premium,
            'average_duration': avg_duration,
            'contract_distribution': {
                'active': active_contracts / total_contracts if total_contracts > 0 else 0,
                'pending': Contract.objects.filter(status='pending').count() / total_contracts if total_contracts > 0 else 0,
                'expired': Contract.objects.filter(status='expired').count() / total_contracts if total_contracts > 0 else 0
            }
        })
