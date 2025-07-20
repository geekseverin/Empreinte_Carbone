# 🌱 Projet d'Évaluation Carbone des Projets Bancaires

## Description du Projet

Cette application permet aux institutions financières (banques, fonds verts, etc.) d'évaluer automatiquement l'empreinte carbone des projets soumis pour financement. Elle utilise des techniques de Data Mining avancées pour fournir des analyses précises et des recommandations personnalisées.

## 🎯 Objectifs

- **Évaluation automatique** de l'empreinte carbone des projets
- **Classification** des projets selon leur impact environnemental
- **Score carbone** de 0 (très vert) à 100 (très polluant)
- **Recommandations** basées sur l'analyse de données

## 🛠️ Technologies Utilisées

### Techniques de Data Mining
1. **Arbres de décision** : Classification des projets selon leur impact
2. **Règles d'association** : Découverte de patterns dans les projets émetteurs
3. **Scoring carbone** : Modèle inspiré de l'analyse du cycle de vie (ACV)

### Stack Technique
- **Python 3.8+**
- **Streamlit** : Interface utilisateur web
- **Scikit-learn** : Machine Learning
- **Pandas** : Manipulation de données
- **Plotly** : Visualisations interactives
- **MLxtend** : Règles d'association

## 📁 Structure du Projet

```
projet_carbone_banque/
├── data/
│   └── dataset_projets_carbone_complet.csv
├── models/
│   └── decision_tree_model.pkl
├── utils/
│   ├── preprocessing.py          # Prétraitement des données
│   ├── scoring_utils.py          # Calcul des scores carbone/ESG
│   ├── classification.py         # Modèle d'arbre de décision
│   └── association_rules.py      # Règles d'association
├── app/
│   ├── orchestration.py          # Pipeline d'évaluation
│   └── main.py                   # Interface Streamlit
├── requirements.txt
└── README.md
```

## 🚀 Installation et Exécution

### 1. Cloner le projet
```bash
git clone <votre-repo>
cd projet_carbone_banque
```

### 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 3. Préparer les données
Placez votre fichier `dataset_projets_carbone_complet.csv` dans le dossier `data/`

### 4. Lancer l'application
```bash
streamlit run app/main.py
```

L'application sera accessible à l'adresse : `http://localhost:8501`

## 📊 Fonctionnalités

### Interface Projet
- ✅ Formulaire de soumission de projet
- ✅ Upload de documents descriptifs
- ✅ Sélection des caractéristiques (énergie, transport, matériaux)

### Analyse Interactive
- ✅ Affichage du score carbone calculé
- ✅ Classification : "Très polluant", "Acceptable", "Vert"
- ✅ Visualisation des facteurs les plus impactants
- ✅ Recommandations personnalisées

### Fonctionnalités Avancées
- ✅ Historique des projets soumis
- ✅ Comparaison de plusieurs projets
- ✅ Téléchargement de rapports PDF automatisés
- ✅ Visualisations interactives

## 📈 Métriques d'Évaluation

### Score Carbone (0-100)
- **0-30** : Projet Vert 🟢
- **31-60** : Projet Acceptable 🟡
- **61-100** : Projet Très Polluant 🔴

### Facteurs Considérés
- **Énergie utilisée** (25%) : renouvelable, mix, fossile
- **Transport** (20%) : type, distance, fréquence
- **Matériaux** (15%) : béton, bois, recyclé, etc.
- **Secteur** (20%) : industriel, construction, agriculture, etc.
- **Équipe/Locaux** (10%) : taille de l'équipe
- **Durée de vie** (10%) : durabilité du projet

## 🤖 Modèles de Machine Learning

### Arbre de Décision
- Classifie automatiquement les projets
- Explique les facteurs de décision
- Précision typique : 85-90%

### Règles d'Association
- Découvre des patterns récurrents
- Exemple : "Si énergie fossile + transport international → forte empreinte"
- Génère des recommandations personnalisées

## 📊 Sources de Données

- **Base Carbone ADEME** : Facteurs d'émission officiels
- **ecoinvent** : Base ACV mondiale
- **Project Drawdown** : Solutions à impact positif
- **European Environment Agency** : Datasets environnementaux

## 🎨 Captures d'Écran

### Dashboard Principal
Interface intuitive pour saisir les caractéristiques du projet

### Résultats d'Évaluation
- Score carbone visuel
- Graphiques d'impact
- Recommandations automatiques

### Historique et Comparaisons
Suivi des projets évalués avec visualisations comparatives

## 🔧 Configuration Avancée

### Personnalisation des Facteurs d'Émission
Modifiez les coefficients dans `utils/scoring_utils.py` :

```python
self.energy_factors = {
    'renouvelable': 0.1,
    'mix': 0.5,
    'fossile': 1.0
}
```

### Ajustement des Seuils de Classification
Personnalisez les catégories dans `utils/preprocessing.py`

## 🚦 Tests et Validation

```bash
# Test du pipeline complet
python -m pytest tests/

# Validation des modèles
python utils/model_validation.py
```

## 📝 Livrables

- ✅ Code source complet
- ✅ Application Streamlit déployable
- ✅ Base de données des projets
- ✅ Documentation technique
- ✅ Rapports PDF automatisés

## 👥 Contribution

1. Fork le projet
2. Créer une branche feature
3. Commit les changements
4. Push vers la branche
5. Ouvrir une Pull Request

## 📧 Contact

Pour toute question : kpatchaababa@gmail.com

## 📄 Licence

Ce projet est développé dans le cadre d'un projet académique d'évaluation de l'empreinte carbone des projets bancaires.

---
**Développé avec ❤️ pour un avenir plus vert** 🌱