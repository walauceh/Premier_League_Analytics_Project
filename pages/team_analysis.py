"""Team Analysis page - Deep dive into individual teams."""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / 'src'))


def show(data):
    """Display team analysis page."""
    st.title("🔍 Team Analysis")
    
    team_data = data['team_data']
    
    # Team selector
    teams = sorted(team_data['team_name'].unique())
    selected_team = st.selectbox("Select Team:", teams)
    
    # Time range
    col1, col2 = st.columns(2)
    with col1:
        last_n = st.slider("Last N matches to analyze:", 5, 38, 10)
    with col2:
        season_filter = st.selectbox("Season (optional):", ['All'] + sorted(team_data['season'].unique(), reverse=True))
    
    # Filter data
    team_matches = team_data[team_data['team_name'] == selected_team].copy()
    if season_filter != 'All':
        team_matches = team_matches[team_matches['season'] == season_filter]
    
    team_matches = team_matches.sort_values('date', ascending=False).head(last_n)
    
    if len(team_matches) == 0:
        st.warning("No data available for selected filters")
        return
    
    st.markdown("---")
    
    # Key metrics
    st.markdown(f"### {selected_team} - Last {len(team_matches)} Matches")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        ppg = team_matches['points'].mean()
        st.metric("Points/Game", f"{ppg:.2f}")
    
    with col2:
        wins = (team_matches['result'] == 'W').sum()
        st.metric("Wins", wins)
    
    with col3:
        goals_pg = team_matches['goals_for'].mean()
        st.metric("Goals/Game", f"{goals_pg:.2f}")
    
    with col4:
        xg_pg = team_matches['xG'].mean()
        st.metric("xG/Game", f"{xg_pg:.2f}")
    
    with col5:
        clean_sheets = team_matches['clean_sheet'].sum() if 'clean_sheet' in team_matches.columns else 0
        st.metric("Clean Sheets", clean_sheets)
    
    st.markdown("---")
    
    # Match results timeline
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Match Results Timeline")
        
        team_matches_sorted = team_matches.sort_values('date')
        fig = px.line(
            team_matches_sorted,
            x='date',
            y='points_rolling5' if 'points_rolling5' in team_matches_sorted.columns else 'points',
            title='Form (Rolling Average)',
            labels={'points_rolling5': 'Points (5-match avg)', 'date': 'Date'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Goals vs xG")
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=team_matches_sorted['date'],
            y=team_matches_sorted['goals_for'],
            name='Actual Goals',
            marker_color='#3d195b'
        ))
        fig.add_trace(go.Scatter(
            x=team_matches_sorted['date'],
            y=team_matches_sorted['xG'],
            name='xG',
            mode='lines+markers',
            line=dict(color='#00ff87', width=2)
        ))
        fig.update_layout(title='Scoring Performance', xaxis_title='Date', yaxis_title='Goals')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Recent matches table
    st.markdown("### Recent Matches")
    
    recent_display = team_matches_sorted[['date', 'opponent', 'venue', 'goals_for', 'goals_against', 'result', 'xG', 'xGA']].copy()
    recent_display.columns = ['Date', 'Opponent', 'Venue', 'GF', 'GA', 'Result', 'xG', 'xGA']
    recent_display['Date'] = recent_display['Date'].dt.strftime('%Y-%m-%d')
    
    st.dataframe(
        recent_display.style.format({'xG': '{:.2f}', 'xGA': '{:.2f}'}),
        hide_index=True,
        height=400
    )
    
    st.markdown("---")
    
    # Performance metrics
    st.markdown("### Performance Breakdown")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Attack")
        st.metric("Goals/Game", f"{team_matches['goals_for'].mean():.2f}")
        st.metric("xG/Game", f"{team_matches['xG'].mean():.2f}")
        st.metric("Shots/Game", f"{team_matches['shots'].mean():.1f}")
        st.metric("Shot Accuracy", f"{team_matches['shot_accuracy'].mean():.1%}" if 'shot_accuracy' in team_matches.columns else "N/A")
    
    with col2:
        st.markdown("#### Defense")
        st.metric("Goals Conceded/Game", f"{team_matches['goals_against'].mean():.2f}")
        st.metric("xGA/Game", f"{team_matches['xGA'].mean():.2f}")
        st.metric("Shots Conceded/Game", f"{team_matches['shots_against'].mean():.1f}")
        st.metric("Clean Sheet %", f"{(clean_sheets / len(team_matches)):.1%}")
