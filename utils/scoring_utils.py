import numpy as np
import pandas as pd

class CarbonScorer:
    def __init__(self):
        # Facteurs d'émission (inspirés de la Base Carbone ADEME)
        self.energy_factors = {
            'renouvelable': 0.1,
            'mix': 0.5,
            'fossile': 1.0
        }
        
        self.transport_factors = {
            'ferroviaire': 0.2,
            'routier': 0.8,
            'maritime': 0.6,
            'aérien': 1.2
        }
        
        self.material_factors = {
            'bois': 0.2,
            'recyclé': 0.3,
            'verre': 0.5,
            'plastique': 0.7,
            'acier': 0.9,
            'béton': 1.0
        }
        
        self.sector_factors = {
            'Agriculture durable': 0.3,
            'Projets numériques': 0.4,
            'Construction immobilière': 0.8,
            'Transport / logistique': 0.9,
            'Production industrielle': 1.0
        }
        
        self.frequency_factors = {
            'ponctuelle': 0.2,
            'mensuelle': 0.5,
            'hebdomadaire': 0.8,
            'quotidienne': 1.0
        }
    
    def calculate_carbon_score(self, project_data):
        """Calcule le score carbone d'un projet (0-100)"""
        score = 0
        
        # Facteur énergie (poids: 25%)
        energy_score = self.energy_factors.get(project_data.get('energie', 'mix'), 0.5) * 25
        
        # Facteur transport (poids: 20%)
        transport_type_score = self.transport_factors.get(project_data.get('transport_type', 'routier'), 0.8)
        distance = project_data.get('distance', 1000) / 10000  # Normalise par 10000 km
        frequency_score = self.frequency_factors.get(project_data.get('frequency', 'mensuelle'), 0.5)
        transport_score = (transport_type_score * distance * frequency_score) * 20
        
        # Facteur matériaux (poids: 15%)
        materials = project_data.get('materials', 'plastique').split(', ')
        material_score = np.mean([self.material_factors.get(mat.strip(), 0.5) for mat in materials]) * 15
        
        # Facteur secteur (poids: 20%)
        sector_score = self.sector_factors.get(project_data.get('sector', 'Production industrielle'), 1.0) * 20
        
        # Facteur taille équipe (poids: 10%)
        team_size = project_data.get('team_size', 50) / 500  # Normalise par 500
        team_score = min(team_size, 1.0) * 10
        
        # Facteur durée de vie (poids: 10%)
        duration = project_data.get('duration', 20)
        duration_score = max(0, (1 - duration / 50)) * 10  # Plus c'est long, moins c'est polluant
        
        score = energy_score + transport_score + material_score + sector_score + team_score + duration_score
        
        return min(100, max(0, score))
    
    def get_carbon_category(self, score):
        """Détermine la catégorie basée sur le score"""
        if score <= 30:
            return "Vert"
        elif score <= 60:
            return "Acceptable"
        else:
            return "Très polluant"
    
    def get_impact_factors(self, project_data):
        """Retourne les facteurs d'impact les plus importants"""
        factors = {}
        
        # Calcul des scores individuels
        factors['Énergie'] = self.energy_factors.get(project_data.get('energie', 'mix'), 0.5) * 25
        
        transport_type_score = self.transport_factors.get(project_data.get('transport_type', 'routier'), 0.8)
        distance = project_data.get('distance', 1000) / 10000
        frequency_score = self.frequency_factors.get(project_data.get('frequency', 'mensuelle'), 0.5)
        factors['Transport'] = (transport_type_score * distance * frequency_score) * 20
        
        materials = project_data.get('materials', 'plastique').split(', ')
        factors['Matériaux'] = np.mean([self.material_factors.get(mat.strip(), 0.5) for mat in materials]) * 15
        
        factors['Secteur'] = self.sector_factors.get(project_data.get('sector', 'Production industrielle'), 1.0) * 20
        
        team_size = project_data.get('team_size', 50) / 500
        factors['Équipe'] = min(team_size, 1.0) * 10
        
        duration = project_data.get('duration', 20)
        factors['Durée'] = max(0, (1 - duration / 50)) * 10
        
        return factors
    
    def calculate_esg_score(self, project_data, carbon_score):
        """Calcule un score ESG simplifié"""
        # Score environnemental (basé sur le score carbone inversé)
        env_score = 100 - carbon_score
        
        # Score social (basé sur le secteur et la taille de l'équipe)
        social_factors = {
            'Agriculture durable': 80,
            'Projets numériques': 70,
            'Construction immobilière': 60,
            'Transport / logistique': 50,
            'Production industrielle': 40
        }
        social_score = social_factors.get(project_data.get('sector', 'Production industrielle'), 50)
        
        # Score de gouvernance (score fixe pour simplification)
        governance_score = 70
        
        # Score ESG global (pondéré)
        esg_score = (env_score * 0.4 + social_score * 0.3 + governance_score * 0.3)
        
        return min(100, max(0, esg_score))