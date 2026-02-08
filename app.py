"""
Premier League Analytics Dashboard - Main Application
Interactive Streamlit dashboard for tactical and scouting analysis.
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add src directory to path
sys.path.append(str(Path(__file__).parent / 'src'))

# Page configuration
st.set_page_config(
    page_title="Premier League Analytics",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with theme-aware colors
st.markdown("""
    <style>
    /* Light theme (default) */
    @media (prefers-color-scheme: light) {
        .main-header {
            font-size: 3rem;
            font-weight: bold;
            color: #1f1f1f;
            text-align: center;
            padding: 1rem 0;
        }
        .sub-header {
            font-size: 1.5rem;
            color: #0066cc;
            margin-top: 1rem;
        }
        .metric-card {
            background-color: rgba(240, 242, 246, 0.5);
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 0.5rem 0;
        }
    }
    
    /* Dark theme */
    @media (prefers-color-scheme: dark) {
        .main-header {
            font-size: 3rem;
            font-weight: bold;
            color: #ffffff;
            text-align: center;
            padding: 1rem 0;
        }
        .sub-header {
            font-size: 1.5rem;
            color: #4da6ff;
            margin-top: 1rem;
        }
        .metric-card {
            background-color: rgba(38, 39, 48, 0.5);
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 0.5rem 0;
        }
    }
    
    /* Universal styles */
    .stMetric {
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Ensure text readability in both themes */
    div[data-testid="stMetricValue"] {
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Title
st.markdown('<div class="main-header">⚽ Premier League Analytics</div>', unsafe_allow_html=True)
st.markdown(f"### Tactical & Scouting Decision Support System")
if data:
    st.markdown(f"**Current Season Focus: {data.get('season_focus', 'N/A')}**")

# Sidebar navigation
st.sidebar.title("📊 Navigation")
page = st.sidebar.radio(
    "Select Analysis Type:",
    [
        "🏠 Home",
        "📈 League Overview",
        "🔍 Team Analysis",
        "👤 Player Scouting",
        "🎨 Tactical Styles",
        "⚔️ Opponent Analysis",
        "📅 Time Simulation"
    ]
)

# Data loading with caching
@st.cache_data
def load_data():
    """Load all datasets for 2024/25 season."""
    try:
        # Try to load 2024 season data first
        try:
            team_data = pd.read_csv("data/team_features_2024.csv")
            player_data = pd.read_csv("data/player_features_2024.csv")
            team_styles = pd.read_csv("data/team_tactical_styles_2024.csv")
            player_profiles = pd.read_csv("data/player_profiles_enhanced_2024.csv")
            season_focus = "2024/25"
        except FileNotFoundError:
            # Fallback to complete data if 2024 files not yet generated
            team_data = pd.read_csv("data/team_features_complete.csv")
            player_data = pd.read_csv("data/player_features_complete.csv")
            team_styles = pd.read_csv("data/team_tactical_styles.csv")
            player_profiles = pd.read_csv("data/player_profiles.csv")
            # Filter to most recent season
            latest_season = team_data['season'].max()
            team_data = team_data[team_data['season'] == latest_season]
            player_data = player_data[player_data['season'] == latest_season]
            season_focus = f"{latest_season}/{int(str(latest_season)[2:4])+1}"
        
        team_data['date'] = pd.to_datetime(team_data['date'])
        player_data['date'] = pd.to_datetime(player_data['date'])
        
        return {
            'team_data': team_data,
            'player_data': player_data,
            'team_styles': team_styles,
            'player_profiles': player_profiles,
            'season_focus': season_focus
        }
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Load data
data = load_data()

if data is None:
    st.error("Failed to load data. Please ensure all data files are present in the 'data' directory.")
    st.stop()

# Home Page
if page == "🏠 Home":
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📊 Dataset Overview")
        st.metric("Total Matches", f"{len(data['team_data']) // 2:,}")
        st.metric("Unique Teams", data['team_data']['team_name'].nunique())
        st.metric("Unique Players", data['player_data']['player_name'].nunique())
    
    with col2:
        st.markdown("### 📅 Data Period")
        st.metric("From", data['team_data']['date'].min().strftime('%Y-%m-%d'))
        st.metric("To", data['team_data']['date'].max().strftime('%Y-%m-%d'))
        seasons = sorted(data['team_data']['season'].unique())
        st.metric("Seasons", f"{len(seasons)} ({seasons[0]} - {seasons[-1]})")
    
    with col3:
        st.markdown("### 🎯 Features")
        st.metric("Team Features", len(data['team_data'].columns))
        st.metric("Player Features", len(data['player_data'].columns))
        st.metric("Tactical Clusters", data['team_styles']['cluster'].nunique())
    
    st.markdown("---")
    st.markdown("## 🚀 Getting Started")
    
    st.markdown("""
    This dashboard provides comprehensive analytics for Premier League teams and players:
    
    - **📈 League Overview**: Season standings, trends, and performance analysis
    - **🔍 Team Analysis**: Deep dive into team performance, form, and metrics
    - **👤 Player Scouting**: Find and compare players, identify similar profiles
    - **🎨 Tactical Styles**: Understand how teams play and cluster analysis
    - **⚔️ Opponent Analysis**: Match preparation and tactical recommendations
    - **📅 Time Simulation**: Analyze data as of any historical date
    
    **Navigate using the sidebar to explore different analysis types.**
    """)
    
    st.markdown("---")
    st.markdown("### 📌 Key Concepts")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Expected Goals (xG)**
        - Measures quality of chances created
        - Higher xG = better scoring opportunities
        - Compare with actual goals to assess finishing
        
        **PPDA (Passes Allowed Per Defensive Action)**
        - Measures defensive pressing intensity
        - Lower PPDA = more aggressive pressing
        - Higher PPDA = sitting deeper
        """)
    
    with col2:
        st.markdown("""
        **Per 90 Metrics**
        - Normalized statistics per 90 minutes
        - Enables fair comparison between players
        - Accounts for different playing time
        
        **Rolling Averages**
        - Average over last N matches
        - Shows recent form and trends
        - More relevant than season totals
        """)

# Import and run page modules
elif page == "📈 League Overview":
    from pages import league_overview
    league_overview.show(data)

elif page == "🔍 Team Analysis":
    from pages import team_analysis
    team_analysis.show(data)

elif page == "👤 Player Scouting":
    from pages import player_scouting
    player_scouting.show(data)

elif page == "🎨 Tactical Styles":
    from pages import tactical_styles
    tactical_styles.show(data)

elif page == "⚔️ Opponent Analysis":
    from pages import opponent_analysis_page
    opponent_analysis_page.show(data)

elif page == "📅 Time Simulation":
    from pages import time_simulation_page
    time_simulation_page.show(data)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; opacity: 0.6; padding: 2rem 0;'>
    <p>Premier League Analytics Dashboard | Built with Streamlit</p>
    <p style='font-size: 0.8rem;'>Data from Understat & FBref (2024/25 Season)</p>
</div>
""", unsafe_allow_html=True)
