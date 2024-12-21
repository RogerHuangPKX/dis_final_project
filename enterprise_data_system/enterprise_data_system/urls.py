from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import (
    CustomerViewSet, ContractViewSet, FeedbackViewSet,
    login, ai_analytics, dashboard_analytics
)

# Create router and register viewsets
router = DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'contracts', ContractViewSet, basename='contract')
router.register(r'feedbacks', FeedbackViewSet, basename='feedback')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('auth/login/', login, name='login'),
    path('api/analytics/ai/', ai_analytics, name='ai-analytics'),
    path('api/analytics/dashboard/', dashboard_analytics, name='dashboard-analytics'),
]

# Available API endpoints:
# GET /api/customers/ - List all customers
# POST /api/customers/ - Create a new customer
# GET /api/customers/{id}/ - Get customer details
# PUT /api/customers/{id}/ - Update customer
# DELETE /api/customers/{id}/ - Delete customer
# GET /api/customers/{id}/risk_analysis/ - Get customer risk analysis
# POST /api/customers/{id}/calculate_quote/ - Calculate insurance quote

# GET /api/contracts/ - List all contracts
# POST /api/contracts/ - Create a new contract
# GET /api/contracts/{id}/ - Get contract details
# PUT /api/contracts/{id}/ - Update contract
# DELETE /api/contracts/{id}/ - Delete contract
# GET /api/contracts/analytics/ - Get contract analytics
# GET /api/analytics/ai/ - Get AI analytics data
