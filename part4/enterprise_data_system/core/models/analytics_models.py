from django.db import models
from django.contrib.postgres.fields import ArrayField

class MLModelVersion(models.Model):
    id = models.AutoField(primary_key=True)
    model_type = models.CharField(max_length=20)
    version = models.CharField(max_length=50)
    accuracy = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    model_path = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    metadata = models.JSONField(null=True)

    class Meta:
        db_table = 'mlmodelversion'
        unique_together = [['model_type', 'version']]

class MLModelTrainingJob(models.Model):
    id = models.AutoField(primary_key=True)
    model_type = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True)
    error_message = models.TextField(null=True)
    metrics = models.JSONField(null=True)

    class Meta:
        db_table = 'mlmodeltrainingjob'

class DataUpdateLog(models.Model):
    id = models.AutoField(primary_key=True)
    table_name = models.CharField(max_length=100)
    operation = models.CharField(max_length=20)
    record_count = models.IntegerField()
    processed_at = models.DateTimeField(auto_now_add=True)
    requires_retraining = models.BooleanField(default=False)

    class Meta:
        db_table = 'dataupdatelog'

class CustomerFeedback(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, db_column='customer_id')
    feedback_text = models.TextField()
    sentiment_score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    key_topics = ArrayField(models.TextField())

    class Meta:
        db_table = 'customerfeedback'
        indexes = [
            models.Index(fields=['sentiment_score'], name='idx_feedback_sentiment'),
            models.Index(fields=['created_at'], name='idx_feedback_created'),
        ]

class CallRecord(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, db_column='customer_id')
    call_text = models.TextField()
    duration = models.IntegerField()
    call_time = models.DateTimeField()
    sentiment_score = models.FloatField()
    key_topics = ArrayField(models.TextField())

    class Meta:
        db_table = 'callrecord'
        indexes = [
            models.Index(fields=['call_time'], name='idx_call_time'),
            models.Index(fields=['sentiment_score'], name='idx_call_sentiment'),
        ]

class ChronicDiseaseRisk(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, db_column='customer_id')
    risk_score = models.FloatField()
    risk_factors = ArrayField(models.TextField())
    prediction_date = models.DateTimeField()
    confidence_score = models.FloatField()

    class Meta:
        db_table = 'chronicdiseaserisk'
        indexes = [
            models.Index(fields=['risk_score'], name='idx_risk_score'),
            models.Index(fields=['prediction_date'], name='idx_disease_prediction'),
        ]

class ChurnPrediction(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, db_column='customer_id')
    churn_probability = models.FloatField()
    contributing_factors = ArrayField(models.TextField())
    prediction_date = models.DateTimeField()

    class Meta:
        db_table = 'churnprediction'
        indexes = [
            models.Index(fields=['churn_probability'], name='idx_churn_prob'),
            models.Index(fields=['prediction_date'], name='idx_churn_prediction'),
        ]

class ProductRecommendation(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, db_column='customer_id')
    plan = models.ForeignKey('PlanName', on_delete=models.CASCADE, db_column='plan_id')
    recommendation_score = models.FloatField()
    recommendation_date = models.DateTimeField()

    class Meta:
        db_table = 'productrecommendation'
        indexes = [
            models.Index(fields=['recommendation_score'], name='idx_recommendation'),
            models.Index(fields=['recommendation_date'], name='idx_recommendation_date'),
        ]
