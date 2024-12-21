import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib
from faker import Faker
import random
from datetime import datetime, timedelta
import os

fake = Faker()
MODEL_DIR = os.path.join(os.path.dirname(__file__), 'models')

def generate_training_data(n_samples=1000):
    data = []
    for _ in range(n_samples):
        # Customer features
        age = random.randint(18, 80)
        income = random.randint(30000, 200000)
        years_as_customer = random.randint(1, 20)
        num_products = random.randint(1, 5)
        total_claims = random.randint(0, 10)
        
        # Feedback and interaction features
        avg_sentiment = random.uniform(0, 1)
        num_complaints = random.randint(0, 5)
        response_time = random.randint(1, 48)
        
        # Contract features
        premium = random.randint(1000, 5000)
        coverage = random.randint(50000, 1000000)
        payment_delay = random.randint(0, 30)
        
        # Additional features for product recommendation
        risk_tolerance = random.choice(['low', 'medium', 'high'])
        family_size = random.randint(1, 6)
        employment_status = random.choice(['employed', 'self-employed', 'retired'])
        
        # Target variables with more realistic relationships
        disease_risk = 1 if (age > 50 and total_claims > 5) or random.random() < 0.3 else 0
        churn_risk = 1 if (payment_delay > 15 or num_complaints > 3) or random.random() < 0.2 else 0
        
        # Product score based on multiple factors
        base_score = random.uniform(0.3, 0.7)
        age_factor = min((age - 18) / 62, 1) * 0.2
        income_factor = min(income / 200000, 1) * 0.2
        loyalty_factor = min(years_as_customer / 20, 1) * 0.2
        sentiment_factor = avg_sentiment * 0.2
        risk_factor = {'low': 0.1, 'medium': 0.2, 'high': 0.3}[risk_tolerance]
        
        product_score = (base_score + age_factor + income_factor + 
                        loyalty_factor + sentiment_factor + risk_factor)
        product_score = min(max(product_score, 0), 1)
        
        data.append({
            'age': age,
            'income': income,
            'years_as_customer': years_as_customer,
            'num_products': num_products,
            'total_claims': total_claims,
            'avg_sentiment': avg_sentiment,
            'num_complaints': num_complaints,
            'response_time': response_time,
            'premium': premium,
            'coverage': coverage,
            'payment_delay': payment_delay,
            'risk_tolerance': risk_tolerance,
            'family_size': family_size,
            'employment_status': employment_status,
            'disease_risk': disease_risk,
            'churn_risk': churn_risk,
            'product_score': product_score
        })
    
    return pd.DataFrame(data)

def train_disease_risk_model(df):
    features = ['age', 'total_claims', 'num_products', 'premium', 'coverage']
    X = df[features]
    y = df['disease_risk']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)
    
    accuracy = model.score(X_test_scaled, y_test)
    print(f'Disease Risk Model Accuracy: {accuracy:.2f}')
    
    joblib.dump(model, os.path.join(MODEL_DIR, 'disease_model.pkl'))
    joblib.dump(scaler, os.path.join(MODEL_DIR, 'disease_scaler.pkl'))

def train_churn_model(df):
    features = ['years_as_customer', 'num_complaints', 'avg_sentiment', 'payment_delay', 'premium']
    X = df[features]
    y = df['churn_risk']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)
    
    accuracy = model.score(X_test_scaled, y_test)
    print(f'Churn Model Accuracy: {accuracy:.2f}')
    
    joblib.dump(model, os.path.join(MODEL_DIR, 'churn_model.pkl'))
    joblib.dump(scaler, os.path.join(MODEL_DIR, 'churn_scaler.pkl'))

def train_product_recommendation_model(df):
    numerical_features = ['age', 'income', 'num_products', 'avg_sentiment', 'years_as_customer', 
                         'family_size', 'total_claims', 'premium']
    categorical_features = ['risk_tolerance', 'employment_status']
    
    numeric_transformer = Pipeline(steps=[
        ('scaler', StandardScaler())
    ])
    
    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(drop='first', sparse_output=False))
    ])
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numerical_features),
            ('cat', categorical_transformer, categorical_features)
        ])
    
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=200, 
                                          max_depth=10,
                                          min_samples_split=5,
                                          min_samples_leaf=2,
                                          random_state=42))
    ])
    
    X = df[numerical_features + categorical_features]
    y = df['product_score']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model.fit(X_train, y_train)
    
    r2_score = model.score(X_test, y_test)
    print(f'Product Recommendation Model R2 Score: {r2_score:.2f}')
    
    joblib.dump(model, os.path.join(MODEL_DIR, 'recommendation_model.pkl'))

if __name__ == '__main__':
    os.makedirs(MODEL_DIR, exist_ok=True)
    df = generate_training_data(n_samples=10000)
    
    train_disease_risk_model(df)
    train_churn_model(df)
    train_product_recommendation_model(df)
    
    print(f'Models saved in: {MODEL_DIR}')
