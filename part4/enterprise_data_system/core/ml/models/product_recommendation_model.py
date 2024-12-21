from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
from .base_model import BaseModel

class ProdRecModel(BaseModel):
    def __init__(self, k=5):
        super().__init__("prod_rec_model")
        self.scaler = StandardScaler()
        self.k = k
        self.prods = None
        self.cols = None
        
    def preprocess(self, data):
        if self.cols is None:
            self.cols = data.columns
            
        tmp = data.copy()
        num_cols = tmp.select_dtypes(include=['int64', 'float64']).columns
        if len(num_cols) > 0:
            if not hasattr(self.scaler, 'mean_'):
                self.scaler.fit(tmp[num_cols])
            tmp[num_cols] = self.scaler.transform(tmp[num_cols])
        
        return tmp
    
    def build(self):
        return NearestNeighbors(
            n_neighbors=self.k,
            algorithm='ball_tree',
            metric='euclidean'
        )
    
    def fit(self, user_data, prod_data):
        self.prods = prod_data
        X = self.preprocess(user_data)
        self.model = self.build()
        self.model.fit(X)
        return self
    
    def get_recs(self, user_data, n=5):
        if self.model is None or self.prods is None:
            raise ValueError("run fit() first")
            
        X = self.preprocess(user_data)
        dists, idxs = self.model.kneighbors(X)
        
        recs = []
        for user_idx in idxs[0]:
            user_prods = self.prods[user_idx]
            recs.extend(user_prods)
            
        return list(set(recs))[:n]
    
    def get_sim_score(self, user_data):
        if self.model is None:
            raise ValueError("run fit() first")
            
        X = self.preprocess(user_data)
        dists, _ = self.model.kneighbors(X)
        return 1 / (1 + np.mean(dists, axis=1))
