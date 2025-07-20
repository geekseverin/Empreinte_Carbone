import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split

class DataPreprocessor:
    def __init__(self):
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.categorical_columns = ['Secteur', 'Énergie utilisée', 'Type de transport', 'Fréquence transport', 'Matériaux']
        
    def load_data(self, filepath):
        """Charge les données depuis un fichier CSV"""
        return pd.read_csv(filepath)
    
    def clean_data(self, df):
        """Nettoie les données"""
        # Supprime les doublons
        df = df.drop_duplicates()
        
      # Gère les valeurs manquantes
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].fillna('Unknown')  # Réassignation pour les colonnes de type 'object'
            else:
                df[col] = df[col].fillna(df[col].median())  # Réassignation pour les colonnes numériques

        return df
    
    def encode_categorical_variables(self, df, fit=True):
        """Encode les variables catégorielles"""
        df_encoded = df.copy()
        
        for col in self.categorical_columns:
            if col in df_encoded.columns:
                if fit:
                    self.label_encoders[col] = LabelEncoder()
                    df_encoded[col] = self.label_encoders[col].fit_transform(df_encoded[col])
                else:
                    if col in self.label_encoders:
                        try:
                            df_encoded[col] = self.label_encoders[col].transform(df_encoded[col])
                        except ValueError:
                            # Gère les nouvelles catégories non vues pendant l'entraînement
                            df_encoded[col] = 0
        
        return df_encoded
    
    def create_carbon_category(self, df):
        """Crée une catégorie basée sur le budget carbone"""
        conditions = [
            df['Budget carbone estimé (tCO2e)'] <= 50,
            (df['Budget carbone estimé (tCO2e)'] > 50) & (df['Budget carbone estimé (tCO2e)'] <= 200),
            df['Budget carbone estimé (tCO2e)'] > 200
        ]
        choices = ['Vert', 'Acceptable', 'Très polluant']
        df['Catégorie_Carbone'] = np.select(conditions, choices, default='Acceptable')
        return df
    
    def prepare_features(self, df):
        """Prépare les features pour le modèle"""
        feature_columns = [
            'Secteur', 'Énergie utilisée', 'Type de transport', 
            'Distance transport (km)', 'Fréquence transport', 'Matériaux',
            'Taille de l\'équipe / locaux', 'Durée de vie estimée (ans)', 'Score ESG initial'
        ]
        
        return df[feature_columns]
    
    def split_data(self, X, y, test_size=0.2, random_state=42):
        """Divise les données en ensembles d'entraînement et de test"""
        return train_test_split(X, y, test_size=test_size, random_state=random_state)
    
    def preprocess_pipeline(self, filepath):
        """Pipeline complet de preprocessing"""
        # Charge les données
        df = self.load_data(filepath)
        
        # Nettoie les données
        df = self.clean_data(df)
        
        # Crée la catégorie carbone
        df = self.create_carbon_category(df)
        
        # Encode les variables catégorielles
        df_encoded = self.encode_categorical_variables(df, fit=True)
        
        # Prépare les features
        X = self.prepare_features(df_encoded)
        y = df_encoded['Catégorie_Carbone']
        
        return X, y, df