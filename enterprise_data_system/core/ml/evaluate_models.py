import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, r2_score
from sklearn.model_selection import train_test_split
from train_models import generate_training_data
import joblib
import os

MODEL_DIR = os.path.join(os.path.dirname(__file__), 'models')

def evaluate_models():
    print("Generating test data...")
    df = generate_training_data(n_samples=2000)
    
    # Evaluate Disease Risk Model
    print("\nEvaluating Disease Risk Model...")
    disease_model = joblib.load(os.path.join(MODEL_DIR, 'disease_model.pkl'))
    disease_scaler = joblib.load(os.path.join(MODEL_DIR, 'disease_scaler.pkl'))
    
    features = ['age', 'total_claims', 'num_products', 'premium', 'coverage']
    X = df[features]
    y = df['disease_risk']
    
    X_test_scaled = disease_scaler.transform(X)
    y_pred = disease_model.predict(X_test_scaled)
    
    print("\nDisease Risk Model Metrics:")
    print(f"Accuracy: {accuracy_score(y, y_pred):.4f}")
    print(f"Precision: {precision_score(y, y_pred):.4f}")
    print(f"Recall: {recall_score(y, y_pred):.4f}")
    print(f"F1 Score: {f1_score(y, y_pred):.4f}")
    
    # Evaluate Churn Model
    print("\nEvaluating Churn Model...")
    churn_model = joblib.load(os.path.join(MODEL_DIR, 'churn_model.pkl'))
    churn_scaler = joblib.load(os.path.join(MODEL_DIR, 'churn_scaler.pkl'))
    
    features = ['years_as_customer', 'num_complaints', 'avg_sentiment', 'payment_delay', 'premium']
    X = df[features]
    y = df['churn_risk']
    
    X_test_scaled = churn_scaler.transform(X)
    y_pred = churn_model.predict(X_test_scaled)
    
    print("\nChurn Model Metrics:")
    print(f"Accuracy: {accuracy_score(y, y_pred):.4f}")
    print(f"Precision: {precision_score(y, y_pred):.4f}")
    print(f"Recall: {recall_score(y, y_pred):.4f}")
    print(f"F1 Score: {f1_score(y, y_pred):.4f}")
    
    # Evaluate Product Recommendation Model
    print("\nEvaluating Product Recommendation Model...")
    rec_model = joblib.load(os.path.join(MODEL_DIR, 'recommendation_model.pkl'))
    
    numerical_features = ['age', 'income', 'num_products', 'avg_sentiment', 'years_as_customer', 
                         'family_size', 'total_claims', 'premium']
    categorical_features = ['risk_tolerance', 'employment_status']
    
    X = df[numerical_features + categorical_features]
    y = df['product_score']
    
    y_pred = rec_model.predict(X)
    r2 = r2_score(y, y_pred)
    
    print("\nProduct Recommendation Model Metrics:")
    print(f"R2 Score: {r2:.4f}")

if __name__ == '__main__':
    evaluate_models()