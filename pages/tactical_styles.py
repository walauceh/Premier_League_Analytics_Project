"""Tactical Styles page - Team playing style analysis."""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / 'src'))


def show(data):
    """Display tactical styles page."""
    st.title("🎨 Tactical Styles")
    
    team_styles = data['team_styles']
    team_data = data['team_data']
    
    st.markdown("### Team Style Clusters")
    st.markdown("Teams clustered by playing style based on recent performance metrics")
    
    # Show cluster distribution
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # PCA visualization
        fig = px.scatter(
            team_styles,
            x='pca1',
            y='pca2',
            color='cluster_label',
            text='team_name',
            title='Team Style Clusters (PCA Projection)',
            labels={'pca1': 'Style Component 1', 'pca2': 'Style Component 2'},
            color_discrete_sequence=px.colors.qualitative.Set1
        )
        fig.update_traces(textposition='top center', textfont_size=8)
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Cluster Distribution")
        cluster_counts = team_styles['cluster_label'].value_counts()
        
        for style, count in cluster_counts.items():
            st.metric(style, count)
    
    st.markdown("---")
    
    # Detailed cluster analysis
    st.markdown("### Cluster Profiles")
    
    selected_cluster = st.selectbox("Select Style:", sorted(team_styles['cluster_label'].unique()))
    
    cluster_teams = team_styles[team_styles['cluster_label'] == selected_cluster]
    
    st.markdown(f"#### {selected_cluster}")
    st.markdown(f"**Teams ({len(cluster_teams)}):** {', '.join(sorted(cluster_teams['team_name'].tolist()))}")
    
    st.markdown("---")
    
    # Average characteristics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**⚔️ Attack**")
        st.metric("xG/game", f"{cluster_teams['xG'].mean():.2f}")
        st.metric("Shots/game", f"{cluster_teams['shots'].mean():.1f}")
        st.metric("Shot Quality", f"{cluster_teams['shot_quality'].mean():.3f}")
    
    with col2:
        st.markdown("**🛡️ Defense**")
        st.metric("xGA/game", f"{cluster_teams['xGA'].mean():.2f}")
        st.metric("Goals Conceded", f"{cluster_teams['avg_goals_against'].mean():.2f}")
    
    with col3:
        st.markdown("**🎯 Style**")
        st.metric("Pressing Intensity", f"{cluster_teams['pressing_intensity'].mean():.3f}")
        st.metric("Deep Completions", f"{cluster_teams['deep'].mean():.1f}")
        st.metric("Points/game", f"{cluster_teams['ppg'].mean():.2f}")
    
    st.markdown("---")
    
    # Radar chart comparison
    st.markdown("### Style Comparison")
    
    compare_styles = st.multiselect(
        "Select styles to compare:",
        sorted(team_styles['cluster_label'].unique()),
        default=sorted(team_styles['cluster_label'].unique())[:2] if len(team_styles['cluster_label'].unique()) >= 2 else []
    )
    
    if len(compare_styles) > 0:
        metrics = ['xG', 'xGA', 'shots', 'shot_quality', 'pressing_intensity', 'deep']
        
        fig = go.Figure()
        
        for style in compare_styles:
            style_data = team_styles[team_styles['cluster_label'] == style]
            values = [style_data[m].mean() for m in metrics]
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=metrics,
                fill='toself',
                name=style
            ))
        
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True)),
            showlegend=True,
            title='Average Characteristics by Style'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Individual team styles
    st.markdown("### Team Style Lookup")
    
    team_to_lookup = st.selectbox("Select Team:", sorted(team_styles['team_name'].unique()))
    
    team_info = team_styles[team_styles['team_name'] == team_to_lookup].iloc[0]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**📊 {team_info['team_name']}**")
        st.markdown(f"**Style:** {team_info['cluster_label']}")
        st.markdown(f"**Cluster:** {int(team_info['cluster'])}")
        
        st.markdown("**Key Metrics:**")
        st.write(f"- xG/game: {team_info['xG']:.2f}")
        st.write(f"- xGA/game: {team_info['xGA']:.2f}")
        st.write(f"- Shots/game: {team_info['shots']:.1f}")
        st.write(f"- Points/game: {team_info['ppg']:.2f}")
    
    with col2:
        # Find similar teams
        st.markdown("**🔄 Similar Teams:**")
        
        # Calculate distances in PCA space
        team_styles['distance_from_selected'] = (
            (team_styles['pca1'] - team_info['pca1'])**2 + 
            (team_styles['pca2'] - team_info['pca2'])**2
        )**0.5
        
        similar = team_styles[team_styles['team_name'] != team_to_lookup].nsmallest(3, 'distance_from_selected')
        
        for idx, row in similar.iterrows():
            st.write(f"- {row['team_name']} ({row['cluster_label']})")
