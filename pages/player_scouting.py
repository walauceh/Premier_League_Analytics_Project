"""Player Scouting page - Find and compare players."""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from player_scout import PlayerScout


def show(data):
    """Display player scouting page."""
    st.title("👤 Player Scouting")
    
    player_profiles = data['player_profiles']
    player_data = data['player_data']
    
    # Initialize scout
    scout = PlayerScout()
    
    # Tab selection
    tab1, tab2, tab3 = st.tabs(["🔍 Find Players", "📊 Player Report", "🔄 Similar Players"])
    
    with tab1:
        st.markdown("### Top Players by Metric")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            metric = st.selectbox(
                "Select Metric:",
                ['goals_per90', 'assists_per90', 'xG_per90', 'xA_per90', 
                 'shots_per90', 'key_passes_per90', 'goal_involvement_per90']
            )
        
        with col2:
            position = st.selectbox(
                "Position Filter:",
                ['All', 'FWD', 'MID', 'DEF', 'GK']
            )
            position_filter = None if position == 'All' else position
        
        with col3:
            min_mins = st.number_input("Min Minutes:", 450, 5000, 900, 450)
        
        # Get top players
        top_players = scout.get_top_players_by_metric(
            player_profiles, metric, position_filter, min_mins, n=20
        )
        
        if len(top_players) > 0:
            # Create bar chart
            fig = px.bar(
                top_players.head(15),
                x=metric,
                y='player_name',
                orientation='h',
                title=f'Top 15 Players by {metric.replace("_", " ").title()}',
                labels={metric: metric.replace('_', ' ').title(), 'player_name': 'Player'},
                color=metric,
                color_continuous_scale='viridis'
            )
            fig.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig, use_container_width=True)
            
            # Display table
            st.dataframe(
                top_players.style.format({metric: '{:.3f}'}),
                hide_index=True,
                height=400
            )
        else:
            st.warning("No players found matching criteria")
    
    with tab2:
        st.markdown("### Player Report")
        
        # Player selector
        players = sorted(player_profiles['player_name'].unique())
        selected_player = st.selectbox("Select Player:", players, key='player_report')
        
        # Get player report
        report = scout.create_player_report(player_profiles, selected_player)
        
        if 'error' not in report:
            # Header
            st.markdown(f"## {report['player_name']}")
            st.markdown(f"**{report['team']}** | {report['position']} | {report['position_group']}")
            
            st.markdown("---")
            
            # Basic stats
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Matches", report['matches'])
            with col2:
                st.metric("Minutes", report['minutes'])
            with col3:
                st.metric("Mins/Match", f"{report['minutes_per_match']:.1f}")
            with col4:
                st.metric("Goals", report['goals'])
            
            st.markdown("---")
            
            # Performance metrics
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📊 Production (per 90)")
                st.metric("Goals", f"{report['goals_per90']:.2f}")
                st.metric("Assists", f"{report['assists_per90']:.2f}")
                st.metric("Goal Involvement", f"{report['goal_involvement_per90']:.2f}")
                st.metric("Key Passes", f"{report['key_passes_per90']:.2f}")
            
            with col2:
                st.markdown("### 🎯 Expected Stats (per 90)")
                st.metric("xG", f"{report['xG_per90']:.2f}")
                st.metric("xA", f"{report['xA_per90']:.2f}")
                st.metric("xG Involvement", f"{report['xG_involvement_per90']:.2f}")
                st.metric("Shots", f"{report['shots_per90']:.2f}")
            
            st.markdown("---")
            
            # Performance vs expectation
            st.markdown("### ⚡ Performance vs Expectation")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                delta = report['goals_vs_xG']
                st.metric("Goals vs xG", f"{delta:+.1f}", f"{'Over' if delta > 0 else 'Under'}performing")
            
            with col2:
                st.metric("Shot Efficiency", f"{report['shot_efficiency']:.1%}")
            
            with col3:
                st.metric("xGChain/90", f"{report['xGChain_per90']:.2f}")
            
            # Percentiles (if available)
            if 'percentiles' in report and report['percentiles']:
                st.markdown("---")
                st.markdown("### 📈 Position Percentiles")
                
                percentiles_df = pd.DataFrame([report['percentiles']]).T
                percentiles_df.columns = ['Percentile']
                percentiles_df.index.name = 'Metric'
                
                fig = px.bar(
                    percentiles_df.reset_index(),
                    x='Percentile',
                    y='Metric',
                    orientation='h',
                    title='Performance vs Position Peers',
                    labels={'Percentile': 'Percentile (%)', 'Metric': ''},
                    color='Percentile',
                    color_continuous_scale='RdYlGn',
                    range_color=[0, 100]
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.error(report['error'])
    
    with tab3:
        st.markdown("### Find Similar Players")
        
        col1, col2 = st.columns(2)
        
        with col1:
            reference_player = st.selectbox("Reference Player:", sorted(player_profiles['player_name'].unique()), key='similar')
        
        with col2:
            n_similar = st.slider("Number of similar players:", 3, 10, 5)
        
        # Find similar players
        similar = scout.find_similar_players(player_profiles, reference_player, n=n_similar)
        
        if len(similar) > 0:
            st.markdown(f"#### Players similar to **{reference_player}**:")
            
            # Display as cards
            for idx, row in similar.iterrows():
                with st.expander(f"**{row['player_name']}** ({row['team_name']}) - Similarity: {row['similarity_score']:.1%}"):
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Goals/90", f"{row['goals_per90']:.2f}")
                    with col2:
                        st.metric("Assists/90", f"{row['assists_per90']:.2f}")
                    with col3:
                        st.metric("xG/90", f"{row['xG_per90']:.2f}")
                    with col4:
                        st.metric("Minutes", int(row['minutes']))
        else:
            st.warning("No similar players found")
