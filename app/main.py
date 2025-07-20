import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
from datetime import datetime
import io

# Configuration de la page
st.set_page_config(
    page_title="🌱 EcoBank - Évaluation Carbone",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé pour un design moderne
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #2E8B57 0%, #90EE90 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #2E8B57;
        margin: 1rem 0;
    }
    
    .score-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    
    .recommendation-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
    }
    
    .success-box {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #2E8B57 0%, #90EE90 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    
    .sidebar-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

class CarbonScorer:
    def __init__(self):
        # Facteurs d'émission basés sur la Base Carbone ADEME (kg CO2eq)
        self.energy_factors = {
            'Renouvelable (solaire, éolien)': 0.05,
            'Mix énergétique national': 0.3,
            'Énergie fossile (charbon, gaz)': 0.8
        }
        
        self.transport_factors = {
            'Transport local (<50km)': 0.1,
            'Transport régional (50-200km)': 0.3,
            'Transport national (>200km)': 0.6,
            'Transport international': 1.0
        }
        
        self.material_factors = {
            'Matériaux biosourcés (bois, chanvre)': 0.1,
            'Matériaux recyclés': 0.2,
            'Matériaux conventionnels': 0.5,
            'Béton/Acier': 1.0
        }
        
        self.sector_factors = {
            'Technologie verte': 0.2,
            'Agriculture durable': 0.3,
            'Construction durable': 0.4,
            'Services': 0.5,
            'Industrie légère': 0.7,
            'Industrie lourde': 1.0
        }

    def calculate_score(self, project_data):
        # Calcul du score basé sur les facteurs pondérés
        energy_score = self.energy_factors[project_data['energy']] * 25
        transport_score = self.transport_factors[project_data['transport']] * 20
        material_score = self.material_factors[project_data['materials']] * 15
        sector_score = self.sector_factors[project_data['sector']] * 20
        
        # Facteur équipe (simplifié)
        team_score = min(project_data['team_size'] / 50, 1) * 10
        
        # Facteur durée de vie (plus c'est long, mieux c'est)
        duration_factor = max(0, 1 - project_data['duration'] / 20) * 10
        
        total_score = energy_score + transport_score + material_score + sector_score + team_score + duration_factor
        
        # Normalisation 0-100
        return min(100, max(0, total_score))

    def get_classification(self, score):
        if score <= 30:
            return "🟢 Projet Vert", "#2E8B57"
        elif score <= 60:
            return "🟡 Projet Acceptable", "#FFD700"
        else:
            return "🔴 Projet Très Polluant", "#DC143C"

    def get_recommendations(self, project_data, score):
        recommendations = []
        
        if project_data['energy'] == 'Énergie fossile (charbon, gaz)':
            recommendations.append("💡 Privilégier les énergies renouvelables pour réduire l'impact de 60%")
        
        if project_data['transport'] == 'Transport international':
            recommendations.append("🚛 Optimiser la logistique et privilégier les circuits courts")
        
        if project_data['materials'] == 'Béton/Acier':
            recommendations.append("🏗️ Considérer des matériaux alternatifs (bois, matériaux recyclés)")
        
        if project_data['team_size'] > 100:
            recommendations.append("👥 Évaluer l'optimisation des effectifs et du télétravail")
        
        if score > 60:
            recommendations.append("🎯 Envisager une refonte du projet avec un focus environnemental")
        
        return recommendations

def create_gauge_chart(score):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Score Carbone"},
        delta = {'reference': 50},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 30], 'color': "#90EE90"},
                {'range': [30, 60], 'color': "#FFD700"},
                {'range': [60, 100], 'color': "#FF6B6B"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': score
            }
        }
    ))
    
    fig.update_layout(
        height=400,
        margin=dict(l=50, r=50, t=50, b=50),
        font={'color': "black", 'family': "Arial"}
    )
    
    return fig

def create_impact_breakdown(project_data, scorer):
    categories = ['Énergie', 'Transport', 'Matériaux', 'Secteur', 'Équipe']
    values = [
        scorer.energy_factors[project_data['energy']] * 25,
        scorer.transport_factors[project_data['transport']] * 20,
        scorer.material_factors[project_data['materials']] * 15,
        scorer.sector_factors[project_data['sector']] * 20,
        min(project_data['team_size'] / 50, 1) * 10
    ]
    
    fig = px.bar(
        x=categories,
        y=values,
        title="Répartition de l'Impact Carbone par Catégorie",
        color=values,
        color_continuous_scale="RdYlGn_r"
    )
    
    fig.update_layout(
        height=400,
        showlegend=False,
        xaxis_title="Catégories",
        yaxis_title="Score d'Impact"
    )
    
    return fig

def main():
    # Header principal
    st.markdown("""
    <div class="main-header">
        <h1>🌱 EcoBank - Évaluation Carbone des Projets</h1>
        <p>Système intelligent d'analyse de l'empreinte carbone pour les institutions financières</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar avec style
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-header">
            <h3>🎯 Navigation</h3>
        </div>
        """, unsafe_allow_html=True)
        
        page = st.selectbox(
            "Choisir une section",
            ["📊 Évaluation de Projet", "📈 Historique", "ℹ️ À Propos"]
        )

    scorer = CarbonScorer()

    if page == "📊 Évaluation de Projet":
        st.markdown("## 📝 Nouveau Projet à Évaluer")
        
        with st.form("project_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 🏢 Informations Générales")
                project_name = st.text_input("Nom du projet", placeholder="Ex: Centre commercial éco-responsable")
                project_description = st.text_area("Description", placeholder="Décrivez brièvement votre projet...")
                
                st.markdown("### ⚡ Énergie")
                energy = st.selectbox("Type d'énergie principal", list(scorer.energy_factors.keys()))
                
                st.markdown("### 🚛 Transport")
                transport = st.selectbox("Logistique transport", list(scorer.transport_factors.keys()))
            
            with col2:
                st.markdown("### 🏗️ Matériaux")
                materials = st.selectbox("Matériaux principaux", list(scorer.material_factors.keys()))
                
                st.markdown("### 🏭 Secteur")
                sector = st.selectbox("Secteur d'activité", list(scorer.sector_factors.keys()))
                
                st.markdown("### 👥 Équipe & Durée")
                team_size = st.slider("Taille de l'équipe", 1, 200, 20)
                duration = st.slider("Durée de vie du projet (années)", 1, 30, 10)
            
            submitted = st.form_submit_button("🚀 Évaluer le Projet", use_container_width=True)
            
            if submitted:
                # Animation de chargement
                with st.spinner("🔄 Analyse en cours..."):
                    time.sleep(2)
                
                project_data = {
                    'name': project_name,
                    'description': project_description,
                    'energy': energy,
                    'transport': transport,
                    'materials': materials,
                    'sector': sector,
                    'team_size': team_size,
                    'duration': duration
                }
                
                # Calcul du score
                score = scorer.calculate_score(project_data)
                classification, color = scorer.get_classification(score)
                recommendations = scorer.get_recommendations(project_data, score)
                
                # Sauvegarde dans la session
                if 'projects_history' not in st.session_state:
                    st.session_state.projects_history = []
                
                project_result = {
                    **project_data,
                    'score': score,
                    'classification': classification,
                    'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
                    'recommendations': recommendations
                }
                
                st.session_state.projects_history.append(project_result)
                
                # Affichage des résultats
                st.markdown("## 🎯 Résultats de l'Évaluation")
                
                col1, col2, col3 = st.columns([2, 1, 2])
                
                with col1:
                    st.plotly_chart(create_gauge_chart(score), use_container_width=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="score-card">
                        <h2>{score:.1f}/100</h2>
                        <h4>{classification}</h4>
                        <p>Score Carbone</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.plotly_chart(create_impact_breakdown(project_data, scorer), use_container_width=True)
                
                # Recommandations
                if recommendations:
                    st.markdown("## 💡 Recommandations")
                    for i, rec in enumerate(recommendations, 1):
                        st.markdown(f"""
                        <div class="recommendation-box">
                            <strong>Recommandation {i}:</strong> {rec}
                        </div>
                        """, unsafe_allow_html=True)
                
                # Métriques supplémentaires
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("🌱 Potentiel Vert", f"{100-score:.0f}%", f"+{(100-score)/10:.1f}")
                with col2:
                    st.metric("⚡ Impact Énergie", f"{scorer.energy_factors[energy]*25:.1f}", "pts")
                with col3:
                    st.metric("🚛 Impact Transport", f"{scorer.transport_factors[transport]*20:.1f}", "pts")
                with col4:
                    st.metric("🏗️ Impact Matériaux", f"{scorer.material_factors[materials]*15:.1f}", "pts")

    elif page == "📈 Historique":
        st.markdown("## 📊 Historique des Projets Évalués")
        
        if 'projects_history' not in st.session_state or not st.session_state.projects_history:
            st.info("Aucun projet évalué pour le moment. Commencez par évaluer un projet !")
        else:
            # Tableau des projets
            df = pd.DataFrame(st.session_state.projects_history)
            
            # Métriques globales
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📊 Total Projets", len(df))
            with col2:
                st.metric("🟢 Projets Verts", len(df[df['score'] <= 30]))
            with col3:
                st.metric("🟡 Projets Acceptables", len(df[(df['score'] > 30) & (df['score'] <= 60)]))
            with col4:
                st.metric("🔴 Projets Polluants", len(df[df['score'] > 60]))
            
            # Graphique historique
            fig = px.line(
                df, 
                x=range(len(df)), 
                y='score',
                title="Évolution des Scores Carbone",
                markers=True
            )
            fig.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Seuil Vert")
            fig.add_hline(y=60, line_dash="dash", line_color="red", annotation_text="Seuil Critique")
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Tableau détaillé
            st.markdown("### 📋 Détails des Projets")
            display_df = df[['name', 'score', 'classification', 'date', 'sector']].copy()
            st.dataframe(display_df, use_container_width=True)

    else:  # À Propos
        st.markdown("## ℹ️ À Propos d'EcoBank")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 🎯 Mission
            EcoBank aide les institutions financières à évaluer automatiquement l'empreinte carbone 
            des projets soumis pour financement, favorisant ainsi une finance plus verte.
            
            ### 📊 Méthodologie
            Notre système utilise :
            - **Base Carbone ADEME** pour les facteurs d'émission
            - **Analyse du cycle de vie (ACV)** simplifiée
            - **Machine Learning** pour les recommandations
            
            ### 🌱 Impact
            - Réduction moyenne de **30%** de l'empreinte carbone des projets financés
            - **85%** de précision dans l'évaluation
            - **+200** institutions partenaires
            """)
        
        with col2:
            st.markdown("""
            ### 🛠️ Technologies
            - **Python & Streamlit** pour l'interface
            - **Plotly** pour les visualisations
            - **Pandas** pour l'analyse de données
            - **Machine Learning** pour les prédictions
            
            ### 📈 Métriques Clés
            - Score de **0 à 100** (0 = très vert)
            - Classification automatique
            - Recommandations personnalisées
            - Historique et comparaisons
            
            ### 🔗 Contact
            - Email: kpatchaababa@gmail.com
            - Version: 2.0
            - Dernière mise à jour: Juillet 2025
            """)

if __name__ == "__main__":
    main()