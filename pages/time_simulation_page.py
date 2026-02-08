"""Time Simulation page - Historical data viewer."""

import streamlit as st
import pandas as pd
import plotly.express as px
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from time_simulation import TimeSimulator


def show(data):
    """Display time simulation page."""
    st.title("📅 Time Simulation")
    st.markdown("### View Data as of Any Historical Date")
    
    st.markdown("""
    This tool lets you analyze data as if you were viewing it at any point in history.
    It ensures **no future data leakage** - only showing data available up to the selected date.
    """)
    
    team_data = data['team_data']
    player_data = data['player_data']
    
    # Initialize simulator
    sim = TimeSimulator(team_data, player_data)
    
    st.markdown("---")
    
    # Current state info
    info = sim.get_current_info()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Current Simulation Date", info['simulation_date'].strftime('%Y-%m-%d'))
    with col2:
        st.metric("Team Matches Available", f"{info['team_matches_available']:,}")
    with col3:
        st.metric("Player Matches Available", f"{info['player_matches_available']:,}")
    
    st.markdown("---")
    
    # Date selector
    st.markdown("### Set Simulation Date")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Season-based selection
        available_seasons = sim.get_available_seasons()
        selected_season = st.selectbox("Select Season:", available_seasons)
        
        # Get matchweeks for season
        matchweeks = sim.get_matchweek_dates(selected_season)
        
        if len(matchweeks) > 0:
            matchweek = st.slider(
                "Select Matchweek:",
                1,
                int(matchweeks['matchweek'].max()),
                int(matchweeks['matchweek'].max())
            )
            
            if st.button("Jump to Matchweek", type="primary"):
                sim.advance_to_matchweek(selected_season, matchweek)
                st.success(f"Simulation date set to end of matchweek {matchweek}")
                st.rerun()
    
    with col2:
        # Direct date selection
        st.markdown("**Or select specific date:**")
        
        min_date = info['data_range'][0].date()
        max_date = info['data_range'][1].date()
        
        selected_date = st.date_input(
            "Select Date:",
            value=max_date,
            min_value=min_date,
            max_value=max_date
        )
        
        if st.button("Set Date", type="secondary"):
            sim.set_simulation_date(selected_date)
            st.success(f"Simulation date set to {selected_date}")
            st.rerun()
    
    st.markdown("---")
    
    # Show what data is available
    st.markdown("### Data Available as of Simulation Date")
    
    current_data = sim.get_data_as_of()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Team Data")
        st.metric("Matches", len(current_data['team_data']))
        st.metric("Unique Teams", current_data['team_data']['team_name'].nunique())
        
        # Latest matches
        st.markdown("**Latest Matches:**")
        latest_team = (current_data['team_data']
                      .sort_values('date', ascending=False)
                      .head(5)[['date', 'team_name', 'opponent', 'goals_for', 'goals_against']])
        latest_team['date'] = latest_team['date'].dt.strftime('%Y-%m-%d')
        st.dataframe(latest_team, hide_index=True)
    
    with col2:
        st.markdown("#### 👤 Player Data")
        st.metric("Matches", len(current_data['player_data']))
        st.metric("Unique Players", current_data['player_data']['player_name'].nunique())
        
        # Top scorers as of date
        st.markdown("**Top Scorers (as of date):**")
        scorers = (current_data['player_data']
                  .groupby('player_name')
                  .agg({'goals': 'sum', 'minutes': 'sum'})
                  .query('minutes >= 450')
                  .nlargest(5, 'goals')
                  .reset_index())
        st.dataframe(scorers, hide_index=True)
    
    st.markdown("---")
    
    # Validation
    st.markdown("### 🔒 Data Integrity Validation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Validate Team Data"):
            is_valid = sim.validate_no_future_data(current_data['team_data'])
            if is_valid:
                st.success("✅ PASS: No future data leakage detected in team data")
            else:
                st.error("❌ FAIL: Future data detected!")
    
    with col2:
        if st.button("Validate Player Data"):
            is_valid = sim.validate_no_future_data(current_data['player_data'])
            if is_valid:
                st.success("✅ PASS: No future data leakage detected in player data")
            else:
                st.error("❌ FAIL: Future data detected!")
    
    st.markdown("---")
    
    # Time series visualization
    st.markdown("### 📈 Data Growth Over Time")
    
    # Sample different dates
    date_range = pd.date_range(start=min_date, end=max_date, periods=20)
    data_points = []
    
    for date in date_range:
        date_data = sim.get_data_as_of(date)
        data_points.append({
            'date': date,
            'team_matches': len(date_data['team_data']),
            'player_matches': len(date_data['player_data'])
        })
    
    timeline_df = pd.DataFrame(data_points)
    
    fig = px.line(
        timeline_df,
        x='date',
        y=['team_matches', 'player_matches'],
        title='Data Availability Over Time',
        labels={'date': 'Date', 'value': 'Number of Matches', 'variable': 'Data Type'}
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    st.info("""
    **💡 Use Case:** This simulation allows you to test your analysis and models 
    as if you were at any point in history, ensuring realistic backtesting without 
    looking ahead at future data.
    """)
