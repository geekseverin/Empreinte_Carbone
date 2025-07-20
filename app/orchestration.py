import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import pandas as pd
import numpy as np
from utils.preprocessing import DataPreprocessor
from utils.scoring_utils import CarbonScorer
from utils.classification import CarbonClassifier
from utils.association_rules import AssociationRulesMiner

class ProjectEvaluationPipeline:
    def __init__(self):
        self.preprocessor = DataPreprocessor()
        self.scorer = CarbonScorer()
        self.classifier = CarbonClassifier()
        self.rules_miner = AssociationRulesMiner()
        self.is_trained = False
        
    def train_models(self, data_filepath):
        """Entraîne tous les modèles"""
        print("Chargement et préparation des données...")
        
        # Préparation des données
        X, y, df_original = self.preprocessor.preprocess_pipeline(data_filepath)
        
        # Division des données
        X_train, X_test, y_train, y_test = self.preprocessor.split_data(X, y)
        
        print("Entraînement du modèle de classification...")
        # Entraînement du classificateur
        feature_names = X.columns.tolist()
        self.classifier.train_model(X_train, y_train, feature_names)
        
        # Évaluation
        evaluation = self.classifier.evaluate_model(X_test, y_test)
        print(f"Précision du modèle: {evaluation['accuracy']:.2f}")
        
        # Sauvegarde du modèle
        os.makedirs('models', exist_ok=True)
        self.classifier.save_model('models/decision_tree_model.pkl')
        
        print("Extraction des règles d'association...")
        # Extraction des règles d'association
        rules = self.rules_miner.mine_association_rules(df_original, min_support=0.15, min_confidence=0.6)
        print(f"Nombre de règles extraites: {len(rules)}")
        
        self.is_trained = True
        return evaluation, rules
    
    def load_trained_models(self):
        """Charge les modèles pré-entraînés"""
        model_loaded = self.classifier.load_model('models/decision_tree_model.pkl')
        if model_loaded:
            self.is_trained = True
            # Recharge les règles d'association si nécessaire
            try:
                df = self.preprocessor.load_data('data/dataset_projets_carbone_complet.csv')
                self.rules_miner.mine_association_rules(df, min_support=0.15, min_confidence=0.6)
            except:
                pass
        return model_loaded
    
    def evaluate_single_project(self, project_data):
        """Évalue un seul projet"""
        if not self.is_trained:
            raise ValueError("Les modèles ne sont pas entraînés ou chargés")
        
        # Calcul du score carbone
        carbon_score = self.scorer.calculate_carbon_score(project_data)
        carbon_category = self.scorer.get_carbon_category(carbon_score)
        
        # Calcul du score ESG
        esg_score = self.scorer.calculate_esg_score(project_data, carbon_score)
        
        # Facteurs d'impact
        impact_factors = self.scorer.get_impact_factors(project_data)
        
        # Prédiction par le modèle de classification
        project_features = self._prepare_project_for_prediction(project_data)
        if project_features is not None:
            ml_prediction = self.classifier.predict(project_features)[0]
            ml_probabilities = self.classifier.predict_proba(project_features)[0]
            decision_path = self.classifier.get_decision_path(project_features.flatten())
        else:
            ml_prediction = carbon_category
            ml_probabilities = [0.33, 0.33, 0.34]
            decision_path = []
        
        # Recommandations basées sur les règles d'association
        recommendations = self.rules_miner.get_recommendations_for_project(project_data)
        
        return {
            'carbon_score': carbon_score,
            'carbon_category': carbon_category,
            'esg_score': esg_score,
            'impact_factors': impact_factors,
            'ml_prediction': ml_prediction,
            'ml_probabilities': dict(zip(['Acceptable', 'Très polluant', 'Vert'], ml_probabilities)),
            'decision_path': decision_path,
            'recommendations': recommendations
        }
    
    def _prepare_project_for_prediction(self, project_data):
        """Prépare les données du projet pour la prédiction"""
        try:
            # Crée un DataFrame avec les données du projet
            project_df = pd.DataFrame([{
                'Secteur': project_data.get('sector', 'Production industrielle'),
                'Énergie utilisée': project_data.get('energie', 'mix'),
                'Type de transport': project_data.get('transport_type', 'routier'),
                'Distance transport (km)': project_data.get('distance', 1000),
                'Fréquence transport': project_data.get('frequency', 'mensuelle'),
                'Matériaux': project_data.get('materials', 'plastique'),
                'Taille de l\'équipe / locaux': project_data.get('team_size', 50),
                'Durée de vie estimée (ans)': project_data.get('duration', 20),
                'Score ESG initial': project_data.get('esg_initial', 50)
            }])
            
            # Encode les variables catégorielles
            project_encoded = self.preprocessor.encode_categorical_variables(project_df, fit=False)
            
            # Prépare les features
            features = self.preprocessor.prepare_features(project_encoded)
            
            return features.values
            
        except Exception as e:
            print(f"Erreur lors de la préparation des données: {e}")
            return None
    
    def get_model_feature_importance(self):
        """Retourne l'importance des features du modèle"""
        if not self.is_trained:
            return None
        return self.classifier.get_feature_importance()
    
    def compare_projects(self, projects_list):
        """Compare plusieurs projets"""
        results = []
        for i, project in enumerate(projects_list):
            project['name'] = project.get('name', f'Projet_{i+1}')
            evaluation = self.evaluate_single_project(project)
            evaluation['project_name'] = project['name']
            results.append(evaluation)
        
        # Trie par score carbone
        results.sort(key=lambda x: x['carbon_score'])
        
        return results