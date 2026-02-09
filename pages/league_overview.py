"""League Overview page - Season standings and trends."""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def show(data):
    """Display league overview page."""
    st.title("📈 League Overview")
    
    team_data = data['team_data']
    
    # Season selector
    seasons = sorted(team_data['season'].unique(), reverse=True)
    selected_season = st.selectbox("Select Season:", seasons)
    
    # Filter data for selected season
    season_data = team_data[team_data['season'] == selected_season].copy()
    
    # Create league table
    st.markdown("### League Table")
    
    league_table = season_data.groupby('team_name').agg({
        'points': 'sum',
        'goals_for': 'sum',
        'goals_against': 'sum',
        'result': 'count',  # matches played
        'xG': 'sum',
        'xGA': 'sum'
    }).reset_index()
    
    league_table.columns = ['Team', 'Points', 'Goals For', 'Goals Against', 'Matches', 'xG', 'xGA']
    league_table['GD'] = league_table['Goals For'] - league_table['Goals Against']
    league_table['xGD'] = league_table['xG'] - league_table['xGA']
    league_table['PPG'] = league_table['Points'] / league_table['Matches']
    
    # Sort by points, then goal difference
    league_table = league_table.sort_values(['Points', 'GD'], ascending=False).reset_index(drop=True)
    league_table.index += 1  # Start from 1
    league_table.index.name = 'Pos'
    
    # Display table
    st.dataframe(
        league_table[['Team', 'Matches', 'Points', 'PPG', 'Goals For', 'Goals Against', 'GD', 'xG', 'xGA', 'xGD']].style.format({
            'PPG': '{:.2f}',
            'xG': '{:.1f}',
            'xGA': '{:.1f}',
            'xGD': '{:.1f}'
        }),
        height=600
    )
    
    st.markdown("---")
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Points vs Expected Points")
        
        # Calculate expected points based on xG difference
        league_table['xPoints'] = league_table.apply(
            lambda row: row['Matches'] * (1 + (row['xGD'] / row['Matches'])),
            axis=1
        )
        
        fig = px.scatter(
            league_table,
            x='xPoints',
            y='Points',
            text='Team',
            labels={'xPoints': 'Expected Points (based on xG)', 'Points': 'Actual Points'},
            title='Performance vs Expectation'
        )
        
        # Add diagonal line
        min_val = min(league_table['xPoints'].min(), league_table['Points'].min())
        max_val = max(league_table['xPoints'].max(), league_table['Points'].max())
        fig.add_trace(go.Scatter(
            x=[min_val, max_val],
            y=[min_val, max_val],
            mode='lines',
            name='Expected',
            line=dict(dash='dash', color='gray')
        ))
        
        fig.update_traces(textposition='top center')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Attack vs Defense")
        
        fig = px.scatter(
            league_table,
            x='Goals Against',
            y='Goals For',
            text='Team',
            size='Points',
            color='Points',
            labels={'Goals Against': 'Goals Conceded', 'Goals For': 'Goals Scored'},
            title='Attack vs Defense Profile',
            color_continuous_scale='RdYlGn'
        )
        
        fig.update_traces(textposition='top center')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Top/Bottom performers
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🏆 Top Scorers (Teams)")
        top_scorers = league_table.nlargest(5, 'Goals For')[['Team', 'Goals For', 'xG']]
        st.dataframe(top_scorers, hide_index=True)
    
    with col2:
        st.markdown("### 🛡️ Best Defenses")
        best_defense = league_table.nsmallest(5, 'Goals Against')[['Team', 'Goals Against', 'xGA']]
        st.dataframe(best_defense, hide_index=True)
    
    with col3:
        st.markdown("### 📈 Overperformers")
        league_table['Performance'] = league_table['Points'] - league_table['xPoints']
        overperformers = league_table.nlargest(5, 'Performance')[['Team', 'Points', 'Performance']]
        st.dataframe(overperformers.style.format({'Performance': '{:+.1f}'}), hide_index=True)
