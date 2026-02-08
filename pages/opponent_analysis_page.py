"""Opponent Analysis page - Match preparation insights."""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from opponent_analysis import OpponentAnalyzer


def show(data):
    """Display opponent analysis page."""
    st.title("⚔️ Opponent Analysis")
    st.markdown("### Match Preparation & Tactical Insights")
    
    team_data = data['team_data']
    
    # Initialize analyzer
    analyzer = OpponentAnalyzer(team_data)
    
    # Tab selection
    tab1, tab2 = st.tabs(["🔍 Opponent Profile", "🎯 Game Plan Generator"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            opponent = st.selectbox("Select Opponent:", sorted(team_data['team_name'].unique()))
        
        with col2:
            last_n = st.slider("Analyze last N matches:", 5, 20, 10)
        
        # Get opponent profile
        profile = analyzer.get_opponent_profile(opponent, last_n_matches=last_n)
        
        if 'error' not in profile:
            st.markdown(f"## {profile['team_name']}")
            st.markdown(f"**Analysis Period:** {profile['date_range'][0]} to {profile['date_range'][1]}")
            st.markdown(f"**Matches Analyzed:** {profile['matches_analyzed']}")
            
            st.markdown("---")
            
            # Form
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Points/Game", f"{profile['form']['ppg']:.2f}")
            with col2:
                st.metric("Wins", profile['form']['wins'])
            with col3:
                st.metric("Draws", profile['form']['draws'])
            with col4:
                st.metric("Losses", profile['form']['losses'])
            
            st.markdown("---")
            
            # Attack & Defense
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### ⚔️ Attack")
                st.metric("Goals/Game", f"{profile['attack']['goals_per_game']:.2f}")
                st.metric("xG/Game", f"{profile['attack']['xG_per_game']:.2f}")
                st.metric("Shots/Game", f"{profile['attack']['shots_per_game']:.1f}")
                st.metric("Shot Accuracy", f"{profile['attack']['shot_accuracy']:.1%}")
                
                delta_attack = profile['attack']['goals_vs_xG']
                st.metric(
                    "Goals vs xG",
                    f"{delta_attack:+.2f}",
                    f"{'Over' if delta_attack > 0 else 'Under'}performing"
                )
            
            with col2:
                st.markdown("### 🛡️ Defense")
                st.metric("Goals Conceded/Game", f"{profile['defense']['goals_conceded_per_game']:.2f}")
                st.metric("xGA/Game", f"{profile['defense']['xGA_per_game']:.2f}")
                st.metric("Shots Conceded/Game", f"{profile['defense']['shots_conceded_per_game']:.1f}")
                st.metric("Clean Sheets", profile['defense']['clean_sheets'])
                
                delta_defense = profile['defense']['goals_conceded_vs_xGA']
                st.metric(
                    "Conceded vs xGA",
                    f"{delta_defense:+.2f}",
                    f"{'Lucky' if delta_defense < 0 else 'Unlucky'}"
                )
            
            st.markdown("---")
            
            # Style
            st.markdown("### 🎨 Playing Style")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Pressing Intensity", f"{profile['style']['pressing_intensity']:.3f}")
            with col2:
                st.metric("Deep Completions", f"{profile['style']['deep_completions']:.1f}")
            with col3:
                st.metric("PPDA", f"{profile['style']['ppda']:.2f}", "Lower = more pressing")
            
            st.markdown("---")
            
            # Venue splits
            st.markdown("### 🏠 Home vs 🛫 Away")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Home PPG", f"{profile['venue_splits']['home_ppg']:.2f}")
            with col2:
                st.metric("Away PPG", f"{profile['venue_splits']['away_ppg']:.2f}")
            with col3:
                st.metric("Home Goals/Game", f"{profile['venue_splits']['home_goals_pg']:.2f}")
            with col4:
                st.metric("Away Goals/Game", f"{profile['venue_splits']['away_goals_pg']:.2f}")
            
            st.markdown("---")
            
            # Strengths & Weaknesses
            st.markdown("### 📋 Tactical Assessment")
            
            sw = analyzer.identify_strengths_weaknesses(profile)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**✅ Strengths:**")
                if sw['strengths']:
                    for strength in sw['strengths']:
                        st.success(f"• {strength}")
                else:
                    st.info("No notable strengths identified")
            
            with col2:
                st.markdown("**⚠️ Weaknesses:**")
                if sw['weaknesses']:
                    for weakness in sw['weaknesses']:
                        st.warning(f"• {weakness}")
                else:
                    st.info("No notable weaknesses identified")
        
        else:
            st.error(profile['error'])
    
    with tab2:
        st.markdown("### Generate Tactical Game Plan")
        
        col1, col2 = st.columns(2)
        
        with col1:
            own_team = st.selectbox("Your Team:", sorted(team_data['team_name'].unique()), key='own')
        
        with col2:
            opponent_team = st.selectbox("Opponent:", sorted(team_data['team_name'].unique()), key='opp')
        
        if st.button("Generate Game Plan", type="primary"):
            game_plan = analyzer.generate_game_plan(own_team, opponent_team, last_n_matches=10)
            
            if 'error' not in game_plan:
                st.markdown(f"## {game_plan['own_team']} vs {game_plan['opponent']}")
                
                st.markdown("---")
                
                # Key matchups
                st.markdown("### 🎯 Key Matchup Areas")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Attack vs Defense**")
                    matchup = game_plan['key_matchup_areas']['attack_vs_defense']
                    st.write(f"Your attack: {matchup['own_attack']:.2f} xG/game")
                    st.write(f"Their defense: {matchup['opp_defense']:.2f} xGA/game")
                    st.success(f"**Advantage: {matchup['advantage']}**")
                
                with col2:
                    st.markdown("**Defense vs Attack**")
                    matchup = game_plan['key_matchup_areas']['defense_vs_attack']
                    st.write(f"Your defense: {matchup['own_defense']:.2f} xGA/game")
                    st.write(f"Their attack: {matchup['opp_attack']:.2f} xG/game")
                    st.success(f"**Advantage: {matchup['advantage']}**")
                
                st.markdown("---")
                
                # Recommendations
                st.markdown("### 📋 Tactical Recommendations")
                
                for rec in game_plan['recommendations']:
                    with st.expander(f"**{rec['area']}**"):
                        st.info(f"📊 **Insight:** {rec['insight']}")
                        st.success(f"💡 **Recommendation:** {rec['recommendation']}")
                
                st.markdown("---")
                
                # Opponent S/W
                st.markdown("### ⚠️ Opponent Analysis")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Opponent Strengths (Be Wary Of):**")
                    for strength in game_plan['opponent_strengths_weaknesses']['strengths'][:3]:
                        st.warning(f"• {strength}")
                
                with col2:
                    st.markdown("**Opponent Weaknesses (Exploit):**")
                    for weakness in game_plan['opponent_strengths_weaknesses']['weaknesses'][:3]:
                        st.success(f"• {weakness}")
            else:
                st.error(game_plan['error'])
