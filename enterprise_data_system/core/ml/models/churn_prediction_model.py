from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
import pandas as pd
from .base_model import BaseModel

class ChurnModel(BaseModel):
    def __init__(self):
        super().__init__("churn_model")
        self.scaler = StandardScaler()
        self.encoders = {}
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
        
        cat_cols = tmp.select_dtypes(include=['object']).columns
        for col in cat_cols:
            if col not in self.encoders:
                self.encoders[col] = LabelEncoder()
                self.encoders[col].fit(tmp[col].fillna('NA'))
            tmp[col] = self.encoders[col].transform(tmp[col].fillna('NA'))
        
        return tmp
    
    def build(self):
        return RandomForestClassifier(
            n_estimators=100,
            max_depth=8,
            min_samples_split=30,
            class_weight='balanced',
            random_state=42
        )
    
    def get_proba(self, X):
        if self.model is None:
            raise ValueError("run fit() first")
        X_tmp = self.preprocess(X)
        return self.model.predict_proba(X_tmp)
    
    def get_churn_prob(self, X):
        proba = self.get_proba(X)
        return proba[:, 1]
    
    def get_factors(self, thresh=0.1):
        if self.model is None:
            raise ValueError("run fit() first")
            
        imp = pd.DataFrame({
            'feat': self.cols,
            'imp': self.model.feature_importances_
        })
        
        top_feats = imp[imp['imp'] > thresh]
        return {
            'feats': top_feats['feat'].tolist(),
            'imps': top_feats['imp'].tolist()
        }
