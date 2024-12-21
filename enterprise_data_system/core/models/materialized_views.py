from django.db import models

class CustomerRiskSummary(models.Model):
    id = models.IntegerField(primary_key=True)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    disease_risk = models.FloatField(null=True)
    churn_probability = models.FloatField(null=True)
    recommendation_count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'customer_risk_summary'

class CustomerInteractionSummary(models.Model):
    id = models.IntegerField(primary_key=True)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    feedback_count = models.IntegerField()
    avg_feedback_sentiment = models.FloatField(null=True)
    call_count = models.IntegerField()
    avg_call_sentiment = models.FloatField(null=True)

    class Meta:
        managed = False
        db_table = 'customer_interaction_summary'

# SQL Functions for refreshing materialized views
REFRESH_ANALYTICS_VIEWS_SQL = """
CREATE OR REPLACE FUNCTION refresh_analytics_views()
RETURNS void AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY customer_risk_summary;
    REFRESH MATERIALIZED VIEW CONCURRENTLY customer_interaction_summary;
END;
$$ LANGUAGE plpgsql;
"""

# SQL Function and Triggers for logging data updates
LOG_DATA_UPDATE_SQL = """
CREATE OR REPLACE FUNCTION log_data_update()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO DataUpdateLog (table_name, operation, record_count, requires_retraining)
    VALUES (TG_TABLE_NAME, TG_OP, 1, true);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER log_customer_feedback_update
AFTER INSERT OR UPDATE ON CustomerFeedback
FOR EACH ROW EXECUTE FUNCTION log_data_update();

CREATE TRIGGER log_call_record_update
AFTER INSERT OR UPDATE ON CallRecord
FOR EACH ROW EXECUTE FUNCTION log_data_update();
"""
