import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, accuracy_score
import pickle
import os

class CarbonClassifier:
    def __init__(self):
        self.model = DecisionTreeClassifier(
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42
        )
        self.feature_names = []
        self.is_trained = False
    
    def train_model(self, X_train, y_train, feature_names=None):
        """Entraîne le modèle d'arbre de décision"""
        self.feature_names = feature_names if feature_names else [f"feature_{i}" for i in range(X_train.shape[1])]
        self.model.fit(X_train, y_train)
        self.is_trained = True
        
        return self.model
    
    def predict(self, X):
        """Fait des prédictions"""
        if not self.is_trained:
            raise ValueError("Le modèle n'est pas encore entraîné")
        return self.model.predict(X)
    
    def predict_proba(self, X):
        """Retourne les probabilités de prédiction"""
        if not self.is_trained:
            raise ValueError("Le modèle n'est pas encore entraîné")
        return self.model.predict_proba(X)
    
    def get_feature_importance(self):
        """Retourne l'importance des features"""
        if not self.is_trained:
            raise ValueError("Le modèle n'est pas encore entraîné")
        
        importance_df = pd.DataFrame({
            'feature': self.feature_names,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        return importance_df
    
    def evaluate_model(self, X_test, y_test):
        """Évalue le modèle"""
        if not self.is_trained:
            raise ValueError("Le modèle n'est pas encore entraîné")
        
        predictions = self.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        report = classification_report(y_test, predictions)
        
        return {
            'accuracy': accuracy,
            'classification_report': report,
            'predictions': predictions
        }
    
    def save_model(self, filepath):
        """Sauvegarde le modèle"""
        if not self.is_trained:
            raise ValueError("Le modèle n'est pas encore entraîné")
        
        model_data = {
            'model': self.model,
            'feature_names': self.feature_names,
            'is_trained': self.is_trained
        }
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
    
    def load_model(self, filepath):
        """Charge le modèle"""
        try:
            with open(filepath, 'rb') as f:
                model_data = pickle.load(f)
            
            self.model = model_data['model']
            self.feature_names = model_data['feature_names']
            self.is_trained = model_data['is_trained']
            
            return True
        except FileNotFoundError:
            return False
    
    def get_decision_path(self, X_sample):
        """Retourne le chemin de décision pour un échantillon"""
        if not self.is_trained:
            raise ValueError("Le modèle n'est pas encore entraîné")
        
        # Obtient le chemin de décision
        decision_path = self.model.decision_path(X_sample.reshape(1, -1))
        leaf_id = self.model.apply(X_sample.reshape(1, -1))
        feature = self.model.tree_.feature
        threshold = self.model.tree_.threshold
        
        # Construit le chemin textuel
        path_info = []
        for node_id in decision_path.indices:
            if leaf_id[0] == node_id:
                continue
            
            if X_sample[feature[node_id]] <= threshold[node_id]:
                threshold_sign = "<="
            else:
                threshold_sign = ">"
            
            path_info.append(f"{self.feature_names[feature[node_id]]} {threshold_sign} {threshold[node_id]:.2f}")
        
        return path_info