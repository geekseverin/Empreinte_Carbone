import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

class AssociationRulesMiner:
    def __init__(self):
        self.rules = None
        self.frequent_itemsets = None
        
    def prepare_data_for_mining(self, df):
        """Prépare les données pour l'extraction de règles d'association"""
        # Convertit les données en format transactionnel
        transactions = []
        
        for _, row in df.iterrows():
            transaction = []
            
            # Catégorises les variables
            if row['Budget carbone estimé (tCO2e)'] > 200:
                transaction.append('Haute_Emission')
            elif row['Budget carbone estimé (tCO2e)'] > 50:
                transaction.append('Moyenne_Emission')
            else:
                transaction.append('Faible_Emission')
            
            # Ajoute les caractéristiques
            transaction.extend([
                f"Secteur_{row['Secteur']}",
                f"Energie_{row['Énergie utilisée']}",
                f"Transport_{row['Type de transport']}",
                f"Frequence_{row['Fréquence transport']}",
                f"Materiaux_{row['Matériaux'].split(',')[0].strip()}"
            ])
            
            # Catégories de distance
            if row['Distance transport (km)'] > 2000:
                transaction.append('Longue_Distance')
            elif row['Distance transport (km)'] > 500:
                transaction.append('Moyenne_Distance')
            else:
                transaction.append('Courte_Distance')
            
            # Catégories d'équipe
            if row['Taille de l\'équipe / locaux'] > 100:
                transaction.append('Grande_Equipe')
            elif row['Taille de l\'équipe / locaux'] > 20:
                transaction.append('Moyenne_Equipe')
            else:
                transaction.append('Petite_Equipe')
            
            transactions.append(transaction)
        
        return transactions
    
    def mine_association_rules(self, df, min_support=0.1, min_confidence=0.6):
        """Extrait les règles d'association"""
        # Prépare les données
        transactions = self.prepare_data_for_mining(df)
        
        # Encode les transactions
        te = TransactionEncoder()
        te_array = te.fit(transactions).transform(transactions)
        df_encoded = pd.DataFrame(te_array, columns=te.columns_)
        
        # Trouve les itemsets fréquents
        self.frequent_itemsets = apriori(df_encoded, min_support=min_support, use_colnames=True)
        
        if len(self.frequent_itemsets) == 0:
            return pd.DataFrame()
        
        # Extrait les règles d'association
        self.rules = association_rules(
            self.frequent_itemsets, 
            metric="confidence", 
            min_threshold=min_confidence
        )
        
        return self.rules
    
    def get_recommendations_for_project(self, project_data, top_n=5):
        """Génère des recommandations basées sur les règles d'association"""
        if self.rules is None or len(self.rules) == 0:
            return ["Aucune recommandation disponible basée sur les règles d'association"]
        
        recommendations = []
        
        # Identifie les caractéristiques du projet
        project_characteristics = set()
        
        # Catégorise l'émission estimée
        carbon_budget = project_data.get('carbon_budget', 100)
        if carbon_budget > 200:
            project_characteristics.add('Haute_Emission')
        elif carbon_budget > 50:
            project_characteristics.add('Moyenne_Emission')
        else:
            project_characteristics.add('Faible_Emission')
        
        project_characteristics.add(f"Secteur_{project_data.get('sector', 'Production industrielle')}")
        project_characteristics.add(f"Energie_{project_data.get('energie', 'mix')}")
        project_characteristics.add(f"Transport_{project_data.get('transport_type', 'routier')}")
        project_characteristics.add(f"Frequence_{project_data.get('frequency', 'mensuelle')}")
        
        # Trouve les règles applicables
        applicable_rules = []
        for _, rule in self.rules.iterrows():
            antecedents = set(rule['antecedents'])
            if antecedents.issubset(project_characteristics):
                applicable_rules.append(rule)
        
        # Génère des recommandations basées sur les règles
        if applicable_rules:
            # Trie par confiance décroissante
            applicable_rules = sorted(applicable_rules, key=lambda x: x['confidence'], reverse=True)
            
            for rule in applicable_rules[:top_n]:
                consequents = list(rule['consequents'])
                confidence = rule['confidence']
                
                if 'Haute_Emission' in consequents:
                    recommendations.append(
                        f"Attention: Configuration à haut risque d'émissions élevées (confiance: {confidence:.2f})"
                    )
                elif 'Faible_Emission' in consequents:
                    recommendations.append(
                        f"Bonne configuration pour réduire les émissions (confiance: {confidence:.2f})"
                    )
        
        # Ajoute des recommandations génériques
        if len(recommendations) < 3:
            if project_data.get('energie') == 'fossile':
                recommendations.append("Recommandation: Privilégier les énergies renouvelables")
            
            if project_data.get('transport_type') == 'aérien':
                recommendations.append("Recommandation: Réduire le transport aérien au minimum")
            
            if 'plastique' in project_data.get('materials', ''):
                recommendations.append("Recommandation: Considérer des matériaux recyclés ou durables")
        
        return recommendations[:top_n] if recommendations else ["Projet avec profil environnemental acceptable"]
    
    def get_high_emission_patterns(self):
        """Retourne les patterns associés aux hautes émissions"""
        if self.rules is None or len(self.rules) == 0:
            return []
        
        high_emission_rules = self.rules[
            self.rules['consequents'].apply(lambda x: 'Haute_Emission' in x)
        ].sort_values('confidence', ascending=False)
        
        patterns = []
        for _, rule in high_emission_rules.head(5).iterrows():
            antecedents = list(rule['antecedents'])
            confidence = rule['confidence']
            patterns.append({
                'pattern': antecedents,
                'confidence': confidence
            })
        
        return patterns