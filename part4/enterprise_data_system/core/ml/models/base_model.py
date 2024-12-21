from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib
import logging
import torch

class BaseModel(ABC):
    def __init__(self, model_name):
        self.model_name = model_name
        self.model = None
        self.logger = logging.getLogger(model_name)
        
        if torch.backends.mps.is_available():
            self.device = torch.device("mps")
            self.logger.info("Using MPS device")
        else:
            self.device = torch.device("cpu")
            self.logger.info("MPS not available, using CPU")
    
    @abstractmethod
    def preprocess(self, data):
        pass
    
    @abstractmethod
    def build(self):
        pass
    
    def to_tensor(self, data):
        if isinstance(data, pd.DataFrame):
            return torch.tensor(data.values, dtype=torch.float32, device=self.device)
        elif isinstance(data, pd.Series):
            return torch.tensor(data.values, dtype=torch.float32, device=self.device)
        elif isinstance(data, np.ndarray):
            return torch.tensor(data, dtype=torch.float32, device=self.device)
        return data
    
    def train(self, X, y, test_size=0.2):
        X_processed = self.preprocess(X)
        X_train, X_test, y_train, y_test = train_test_split(
            X_processed, y, test_size=test_size, random_state=42
        )
        
        self.model = self.build()
        
        X_train_tensor = self.to_tensor(X_train)
        y_train_tensor = self.to_tensor(y_train)
        
        if hasattr(self.model, 'to'):
            self.model = self.model.to(self.device)
            self.model.fit(X_train_tensor, y_train_tensor)
        else:
            self.model.fit(X_train, y_train)
        
        train_metrics = self.evaluate(X_train, y_train)
        test_metrics = self.evaluate(X_test, y_test)
        
        return train_metrics, test_metrics
    
    def predict(self, X):
        if not self.model:
            raise ValueError("run fit() first")
        X_processed = self.preprocess(X)
        
        if hasattr(self.model, 'to'):
            X_tensor = self.to_tensor(X_processed)
            return self.model.predict(X_tensor).cpu().numpy()
        return self.model.predict(X_processed)
    
    def evaluate(self, X, y):
        y_pred = self.predict(X)
        return {
            'accuracy': accuracy_score(y, y_pred),
            'precision': precision_score(y, y_pred, average='weighted'),
            'recall': recall_score(y, y_pred, average='weighted'),
            'f1': f1_score(y, y_pred, average='weighted')
        }
    
    def save(self, path):
        if hasattr(self.model, 'to'):
            self.model = self.model.cpu()
        joblib.dump(self, path)
        self.logger.info(f"Model saved to {path}")
    
    @classmethod
    def load(cls, path):
        model = joblib.load(path)
        if hasattr(model.model, 'to'):
            model.model = model.model.to(model.device)
        return model
