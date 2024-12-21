from django.db.models import Avg, Sum, Count
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import authenticate
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .models import (
    Customer, Contract, CustomerFeedback, CallRecord,
    ChronicDiseaseRisk, ChurnPrediction, ProductRecommendation,
    ContractPayment
)
from .serializers import (
    CustomerSerializer, ContractSerializer,
    CustomerFeedbackSerializer, CallRecordSerializer
)
from .ml.predict import PredictionService
from .permissions import RoleBasedPermission, role_required

prediction_service = PredictionService()

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    try:
        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'token': str(refresh.access_token),
                'refresh': str(refresh),
                'username': user.username,
                'is_staff': user.is_staff,
            })
        else:
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        print(f"Login error: {str(e)}")
        return Response({'error': 'An error occurred during login'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = []  # Temporarily disable permissions for testing

    def get_customer_stats(self, customer):
        """Get aggregated customer statistics"""
        contracts = Contract.objects.filter(account__customer=customer)
        feedback = CustomerFeedback.objects.filter(customer=customer)
        calls = CallRecord.objects.filter(customer=customer)
        
        avg_sentiment = feedback.aggregate(Avg('sentiment_score'))['sentiment_score__avg']
        total_premium = ContractPayment.objects.filter(contract__account__customer=customer).aggregate(Sum('premium'))['premium__sum'] or 0
        total_coverage = contracts.aggregate(Sum('coverage'))['coverage__sum'] or 0
        
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

@api_view(['GET'])
@permission_classes([AllowAny])
def dashboard_analytics(request):
    """Get dashboard analytics data"""
    try:
        # Get customer analytics
        customers = Customer.objects.all()
        total_customers = customers.count()
        active_customers = customers.filter(status='A').count()

        # Get contract analytics
        contracts = Contract.objects.all()
        total_contracts = contracts.count()
        active_contracts = contracts.filter(status='A').count()

        # Get business distribution
        business_distribution = {
            'insurance': Contract.objects.filter(business__name__icontains='insurance').count(),
            'investment': Contract.objects.filter(business__name__icontains='investment').count(),
            'banking': Contract.objects.filter(business__name__icontains='banking').count(),
            'loan': Contract.objects.filter(business__name__icontains='loan').count()
        }

        # Get duration distribution
        duration_distribution = {
            '1': Contract.objects.filter(duration=12).count(),
            '2': Contract.objects.filter(duration=24).count(),
            '3': Contract.objects.filter(duration=36).count(),
            '5': Contract.objects.filter(duration=60).count(),
            '10': Contract.objects.filter(duration=120).count()
        }

        # Get status distribution
        status_distribution = {
            'active': Contract.objects.filter(status='A').count(),
            'pending': Contract.objects.filter(status='P').count(),
            'expired': Contract.objects.filter(status='E').count(),
            'suspended': Contract.objects.filter(status='C').count()
        }

        # Calculate average contract value
        total_premium = ContractPayment.objects.aggregate(
            total=Sum('premium')
        )['total'] or 0
        average_value = total_premium / total_contracts if total_contracts > 0 else 0

        return Response({
            'total_customers': total_customers,
            'active_customers': active_customers,
            'total_contracts': total_contracts,
            'active_contracts': active_contracts,
            'average_contract_value': average_value,
            'retention_rate': 95,  # 示例数据
            'business_distribution': business_distribution,
            'duration_distribution': duration_distribution,
            'status_distribution': status_distribution,
            'risk_distribution': {
                'low': 30,
                'medium': 50,
                'high': 20
            },
            'growth_trend': [100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320]  # 示例数据
        })
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def ai_analytics(request):
    """Get AI-powered analytics data"""
    try:
        # Get feedback analytics
        feedbacks = CustomerFeedback.objects.all()
        feedback_count = feedbacks.count()
        avg_sentiment = feedbacks.aggregate(Avg('sentiment_score'))['sentiment_score__avg'] or 0

        # Get call record analytics
        calls = CallRecord.objects.all()
        call_count = calls.count()
        avg_call_sentiment = calls.aggregate(Avg('sentiment_score'))['sentiment_score__avg'] or 0

        # Get disease risk analytics
        disease_risks = ChronicDiseaseRisk.objects.all()
        avg_risk_score = disease_risks.aggregate(Avg('risk_score'))['risk_score__avg'] or 0
        risk_distribution = {
            'high': disease_risks.filter(risk_score__gte=0.7).count(),
            'medium': disease_risks.filter(risk_score__gte=0.3, risk_score__lt=0.7).count(),
            'low': disease_risks.filter(risk_score__lt=0.3).count()
        }

        # Get churn prediction analytics
        churn_predictions = ChurnPrediction.objects.all()
        avg_churn_prob = churn_predictions.aggregate(Avg('churn_probability'))['churn_probability__avg'] or 0
        churn_distribution = {
            'high': churn_predictions.filter(churn_probability__gte=0.7).count(),
            'medium': churn_predictions.filter(churn_probability__gte=0.3, churn_probability__lt=0.7).count(),
            'low': churn_predictions.filter(churn_probability__lt=0.3).count()
        }

        # Get sentiment trend (last 7 days)
        today = timezone.now().date()
        sentiment_trend = []
        for i in range(7):
            date = today - timedelta(days=i)
            daily_feedbacks = feedbacks.filter(created_at__date=date)
            if daily_feedbacks.exists():
                daily_sentiment = daily_feedbacks.aggregate(Avg('sentiment_score'))['sentiment_score__avg']
                sentiment_trend.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'score': round(daily_sentiment, 2)
                })
            else:
                sentiment_trend.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'score': None
                })

        # Calculate risk distribution percentages
        total_risks = sum(risk_distribution.values())
        risk_distribution_percent = {
            'high': round(risk_distribution['high'] / total_risks * 100 if total_risks > 0 else 0),
            'medium': round(risk_distribution['medium'] / total_risks * 100 if total_risks > 0 else 0),
            'low': round(risk_distribution['low'] / total_risks * 100 if total_risks > 0 else 0)
        }

        # Calculate churn distribution percentages
        total_churns = sum(churn_distribution.values())
        churn_distribution_percent = {
            'high': round(churn_distribution['high'] / total_churns * 100 if total_churns > 0 else 0),
            'medium': round(churn_distribution['medium'] / total_churns * 100 if total_churns > 0 else 0),
            'low': round(churn_distribution['low'] / total_churns * 100 if total_churns > 0 else 0)
        }

        return Response({
            'feedback_analytics': {
                'total_feedbacks': feedback_count,
                'average_sentiment': round(avg_sentiment, 2),
                'sentiment_trend': [x for x in sentiment_trend if x['score'] is not None]
            },
            'call_analytics': {
                'total_calls': call_count,
                'average_sentiment': round(avg_call_sentiment, 2)
            },
            'risk_analytics': {
                'average_risk_score': round(avg_risk_score, 2),
                'risk_distribution': risk_distribution_percent
            },
            'churn_analytics': {
                'average_churn_probability': round(avg_churn_prob, 2),
                'churn_distribution': churn_distribution_percent
            }
        })
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class FeedbackViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerFeedbackSerializer
    permission_classes = []  # Temporarily disable permissions for testing

    def get_queryset(self):
        return CustomerFeedback.objects.select_related('customer').all()

class ContractViewSet(viewsets.ModelViewSet):
    serializer_class = ContractSerializer
    permission_classes = []  # Temporarily disable permissions for testing

    def get_queryset(self):
        return Contract.objects.select_related(
            'account', 
            'business',
            'contractpayment'
        ).all()

    @action(detail=False, methods=['get'])
    def analytics(self, request):
        """Get contract analytics and insights"""
        try:
            total_contracts = Contract.objects.count()
            active_contracts = Contract.objects.filter(status='A').count()
            total_premium = ContractPayment.objects.filter(contract__status='A').aggregate(Sum('premium'))['premium__sum'] or 0
            avg_duration = Contract.objects.aggregate(Avg('duration'))['duration__avg'] or 0
            
            return Response({
                'total_contracts': total_contracts,
                'active_contracts': active_contracts,
                'total_premium': float(total_premium),  # Convert Decimal to float
                'average_duration': float(avg_duration) if avg_duration else 0,
                'contract_distribution': {
                    'active': round(active_contracts / total_contracts * 100, 1) if total_contracts > 0 else 0,
                    'pending': round(Contract.objects.filter(status='P').count() / total_contracts * 100, 1) if total_contracts > 0 else 0,
                    'expired': round(Contract.objects.filter(status='E').count() / total_contracts * 100, 1) if total_contracts > 0 else 0
                }
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
