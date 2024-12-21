from django.utils import timezone
from .models.analytics_models import MLModelVersion, MLModelTrainingJob, DataUpdateLog
from .models.customer_models import Customer
from .ml.models.chronic_disease_model import DiseaseModel as ChronicDiseaseModel
from .ml.models.churn_prediction_model import ChurnModel as ChurnPredictionModel
from .ml.models.product_recommendation_model import ProdRecModel as ProductRecommendationModel

def train_model(model_type):
    job = MLModelTrainingJob.objects.create(
        model_type=model_type,
        status='STARTED'
    )
    
    try:
        if model_type == 'DISEASE':
            model = ChronicDiseaseModel()
        elif model_type == 'CHURN':
            model = ChurnPredictionModel()
        elif model_type == 'PRODUCT':
            model = ProductRecommendationModel()
        
        metrics = model.train()
        version = f"{model_type}-{timezone.now().strftime('%Y%m%d-%H%M%S')}"
        model_path = f"models/{version}.pkl"
        model.save(model_path)
        
        MLModelVersion.objects.filter(model_type=model_type, is_active=True).update(is_active=False)
        
        MLModelVersion.objects.create(
            model_type=model_type,
            version=version,
            accuracy=metrics['accuracy'],
            model_path=model_path,
            is_active=True,
            metadata=metrics
        )
        
        job.status = 'COMPLETED'
        job.metrics = metrics
        job.completed_at = timezone.now()
        job.save()
        
        return job
        
    except Exception as e:
        job.status = 'FAILED'
        job.error_message = str(e)
        job.completed_at = timezone.now()
        job.save()
        raise

def update_predictions():
    models = {
        'DISEASE': ChronicDiseaseModel(),
        'CHURN': ChurnPredictionModel(),
        'PRODUCT': ProductRecommendationModel()
    }
    
    for model_type, model in models.items():
        version = MLModelVersion.objects.filter(model_type=model_type, is_active=True).first()
        if version:
            model.load(version.model_path)
            customers = Customer.objects.filter(end_date__isnull=True)
            
            for customer in customers:
                model.predict(customer)

def check_model_retraining():
    updates = DataUpdateLog.objects.filter(requires_retraining=True)
    if updates.exists():
        for model_type in ['DISEASE', 'CHURN', 'PRODUCT']:
            train_model(model_type)  # Direct call instead of .delay()
        updates.update(requires_retraining=False)
