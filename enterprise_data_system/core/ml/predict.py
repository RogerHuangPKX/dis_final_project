import os
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

MODEL_DIR = os.path.join(os.path.dirname(__file__), 'models')

class PredictionService:
    def __init__(self):
        # Load disease risk model
        self.disease_model = joblib.load(os.path.join(MODEL_DIR, 'disease_model.pkl'))
        self.disease_scaler = joblib.load(os.path.join(MODEL_DIR, 'disease_scaler.pkl'))
        
        # Load churn model
        self.churn_model = joblib.load(os.path.join(MODEL_DIR, 'churn_model.pkl'))
        self.churn_scaler = joblib.load(os.path.join(MODEL_DIR, 'churn_scaler.pkl'))
        
        # Load recommendation model (includes preprocessing pipeline)
        self.recommendation_model = joblib.load(os.path.join(MODEL_DIR, 'recommendation_model.pkl'))

    def predict_disease_risk(self, customer_data):
        """
        Predict disease risk for a customer
        customer_data: dict with keys ['age', 'total_claims', 'num_products', 'premium', 'coverage']
        """
        features = ['age', 'total_claims', 'num_products', 'premium', 'coverage']
        X = pd.DataFrame([customer_data])[features]
        X_scaled = self.disease_scaler.transform(X)
        risk_prob = self.disease_model.predict_proba(X_scaled)[0][1]
        
        return {
            'risk_score': float(risk_prob),
            'risk_level': 'High' if risk_prob > 0.7 else 'Medium' if risk_prob > 0.3 else 'Low',
            'prediction_date': pd.Timestamp.now().isoformat()
        }

    def predict_churn_risk(self, customer_data):
        """
        Predict churn risk for a customer
        customer_data: dict with keys ['years_as_customer', 'num_complaints', 'avg_sentiment', 
                                     'payment_delay', 'premium']
        """
        features = ['years_as_customer', 'num_complaints', 'avg_sentiment', 'payment_delay', 'premium']
        X = pd.DataFrame([customer_data])[features]
        X_scaled = self.churn_scaler.transform(X)
        churn_prob = self.churn_model.predict_proba(X_scaled)[0][1]
        
        return {
            'churn_probability': float(churn_prob),
            'risk_level': 'High' if churn_prob > 0.7 else 'Medium' if churn_prob > 0.3 else 'Low',
            'prediction_date': pd.Timestamp.now().isoformat()
        }

    def get_product_recommendations(self, customer_data):
        """
        Get product recommendations for a customer
        customer_data: dict with keys ['age', 'income', 'num_products', 'avg_sentiment', 
                                     'years_as_customer', 'family_size', 'total_claims', 'premium',
                                     'risk_tolerance', 'employment_status']
        """
        features = ['age', 'income', 'num_products', 'avg_sentiment', 'years_as_customer',
                   'family_size', 'total_claims', 'premium', 'risk_tolerance', 'employment_status']
        X = pd.DataFrame([customer_data])[features]
        recommendation_score = self.recommendation_model.predict(X)[0]
        
        # Map score to product recommendations
        recommendations = []
        if recommendation_score > 0.7:
            recommendations.extend(['Premium Life Insurance', 'Comprehensive Health Coverage'])
        elif recommendation_score > 0.4:
            recommendations.extend(['Standard Life Insurance', 'Basic Health Coverage'])
        else:
            recommendations.extend(['Term Life Insurance', 'Accident Coverage'])
            
        return {
            'recommendation_score': float(recommendation_score),
            'recommended_products': recommendations,
            'recommendation_date': pd.Timestamp.now().isoformat()
        }

# Example usage:
if __name__ == '__main__':
    service = PredictionService()
    
    # Test customer data
    customer = {
        'age': 45,
        'income': 80000,
        'years_as_customer': 5,
        'num_products': 2,
        'total_claims': 3,
        'avg_sentiment': 0.8,
        'num_complaints': 1,
        'payment_delay': 0,
        'premium': 2000,
        'coverage': 100000,
        'risk_tolerance': 'medium',
        'family_size': 4,
        'employment_status': 'employed'
    }
    
    # Get predictions
    disease_risk = service.predict_disease_risk(customer)
    churn_risk = service.predict_churn_risk(customer)
    recommendations = service.get_product_recommendations(customer)
    
    print("\nDisease Risk:", disease_risk)
    print("\nChurn Risk:", churn_risk)
    print("\nProduct Recommendations:", recommendations)
