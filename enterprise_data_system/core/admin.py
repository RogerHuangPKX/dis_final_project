from django.contrib import admin
from .models import (
    Account, AccountLocation,
    BillingAccount, BillingLocation,
    Customer, CustomerIdentity,
    LineOfBusiness, SeriesName, PlanName,
    Contract, ContractPayment, ContractBankAccount, ContractCreditCard,
    Invoice,
    CustomerFeedback, CallRecord,
    ChronicDiseaseRisk, ChurnPrediction, ProductRecommendation,
    MLModelVersion, MLModelTrainingJob, DataUpdateLog
)

admin.site.register(Account)
admin.site.register(AccountLocation)
admin.site.register(BillingAccount)
admin.site.register(BillingLocation)
admin.site.register(Customer)
admin.site.register(CustomerIdentity)
admin.site.register(LineOfBusiness)
admin.site.register(SeriesName)
admin.site.register(PlanName)
admin.site.register(Contract)
admin.site.register(ContractPayment)
admin.site.register(ContractBankAccount)
admin.site.register(ContractCreditCard)
admin.site.register(Invoice)
admin.site.register(CustomerFeedback)
admin.site.register(CallRecord)
admin.site.register(ChronicDiseaseRisk)
admin.site.register(ChurnPrediction)
admin.site.register(ProductRecommendation)
admin.site.register(MLModelVersion)
admin.site.register(MLModelTrainingJob)
admin.site.register(DataUpdateLog)
