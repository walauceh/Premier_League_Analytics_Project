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
    
    # Load team data for defensive stats
    try:
        team_data = pd.read_csv('data/team_features_2023.csv')
    except:
        team_data = None
    
    # Initialize scout with team and player data for defensive stats
    scout = PlayerScout(team_data=team_data, player_data=player_data)
    
    # Tab selection
    tab1, tab2, tab3 = st.tabs(["🔍 Find Players", "📊 Player Report", "🔄 Similar Players"])
    
    with tab1:
        st.markdown("### Top Players by Metric")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Position-specific metric suggestions
            metric_options = {
                'Attacking': ['goals_per90', 'assists_per90', 'xG_per90', 'xA_per90', 'shots_per90'],
                'Creativity': ['key_passes_per90', 'xA_per90', 'assists_per90'],
                'Build-up Play': ['xGChain_per90', 'xGBuildup_per90', 'key_passes_per90'],
                'Discipline': ['yellow_card', 'red_card'],
                'Overall': ['minutes', 'appearances']
            }
            
            metric_category = st.selectbox("Metric Category:", list(metric_options.keys()))
            metric = st.selectbox("Select Metric:", metric_options[metric_category])
        
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
        
        # Single searchable player selector
        players = sorted(player_profiles['player_name'].unique())
        selected_player = st.selectbox(
            "Search and select player (type to filter):",
            players,
            key='player_report',
            help="Start typing to filter the list"
        )
        
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
            
            # Show position context
            if 'position_context' in report:
                st.info(f"**Position Analysis Context:** {report['position_context']}")
                st.markdown("---")
            
            # Position-specific metrics display
            pos_group = report['position_group']
            
            if pos_group == 'Goalkeeper':
                # Goalkeeper comprehensive analysis
                st.markdown("### 🥅 Goalkeeper Performance Analysis")
                
                if 'defensive_stats' in report and report['defensive_stats'] is not None:
                    def_stats = report['defensive_stats']
                    
                    # Main defensive metrics
                    st.markdown("#### Shot Stopping & Save Performance")
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Save %", f"{def_stats.get('save_percentage', 0):.1f}%")
                    with col2:
                        st.metric("Saves (est.)", f"{def_stats.get('saves_estimate', 0):.0f}")
                    with col3:
                        st.metric("Shots Faced/90", f"{def_stats.get('shots_faced_per90', 0):.2f}")
                    with col4:
                        st.metric("Shots on Target/90", f"{def_stats.get('shots_on_target_faced', 0) / (def_stats.get('minutes', 1) / 90):.2f}")
                    
                    st.markdown("---")
                    
                    # Goals & Expected Performance
                    st.markdown("#### Goals Conceded & Expected Performance")
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Goals Conceded", int(def_stats.get('goals_conceded', 0)))
                    with col2:
                        st.metric("Goals Conceded/90", f"{def_stats.get('goals_conceded_per90', 0):.2f}")
                    with col3:
                        st.metric("xGA/90", f"{def_stats.get('xGA_per90', 0):.2f}", help="Expected goals against per 90")
                    with col4:
                        goals_prevented = def_stats.get('goals_prevented', 0)
                        st.metric("Goals Prevented", f"{goals_prevented:+.2f}", 
                                 help="Goals conceded vs xGA (positive = better than expected)",
                                 delta=f"{'Better' if goals_prevented > 0 else 'Worse'} than expected")
                    
                    st.markdown("---")
                    
                    # Clean Sheets
                    st.markdown("#### Clean Sheets & Consistency")
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Clean Sheets", int(def_stats.get('clean_sheets', 0)))
                    with col2:
                        st.metric("Clean Sheet %", f"{def_stats.get('clean_sheet_rate', 0):.1f}%")
                    with col3:
                        st.metric("Total Matches", def_stats.get('matches', 0))
                    
                    # Visualization: Performance metrics
                    st.markdown("---")
                    st.markdown("#### Visual Performance Summary")
                    
                    fig_col1, fig_col2 = st.columns(2)
                    
                    with fig_col1:
                        # Goals prevented chart
                        fig = go.Figure(go.Indicator(
                            mode = "gauge+number+delta",
                            value = def_stats.get('goals_prevented', 0),
                            title = {'text': "Goals Prevented vs xGA"},
                            delta = {'reference': 0},
                            gauge = {
                                'axis': {'range': [-10, 10]},
                                'bar': {'color': "darkblue"},
                                'steps': [
                                    {'range': [-10, -2], 'color': "lightcoral"},
                                    {'range': [-2, 2], 'color': "lightyellow"},
                                    {'range': [2, 10], 'color': "lightgreen"}
                                ],
                                'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 0}
                            }
                        ))
                        fig.update_layout(height=250)
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with fig_col2:
                        # Save percentage gauge
                        fig = go.Figure(go.Indicator(
                            mode = "gauge+number",
                            value = def_stats.get('save_percentage', 0),
                            title = {'text': "Save Percentage"},
                            gauge = {
                                'axis': {'range': [0, 100]},
                                'bar': {'color': "darkgreen"},
                                'steps': [
                                    {'range': [0, 50], 'color': "lightcoral"},
                                    {'range': [50, 70], 'color': "lightyellow"},
                                    {'range': [70, 100], 'color': "lightgreen"}
                                ],
                                'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 70}
                            }
                        ))
                        fig.update_layout(height=250)
                        st.plotly_chart(fig, use_container_width=True)
                    
                    st.markdown("---")
                    st.caption("*Note: Save estimates and defensive stats derived from team performance when player was on field. Individual GK data not available in Understat.*")
                    
                else:
                    st.warning("⚠️ **Limited Data**: Goalkeeper defensive statistics could not be calculated.")
                
            elif pos_group == 'Defender':
                # Defender comprehensive analysis
                st.markdown("### 🛡️ Defender Performance Analysis")
                
                # Defensive Performance Section
                if 'defensive_stats' in report and report['defensive_stats'] is not None:
                    def_stats = report['defensive_stats']
                    
                    st.markdown("#### Defensive Metrics & Clean Sheets")
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Clean Sheets", int(def_stats.get('clean_sheets', 0)))
                    with col2:
                        st.metric("Clean Sheet %", f"{def_stats.get('clean_sheet_rate', 0):.1f}%")
                    with col3:
                        st.metric("Goals Conceded/90", f"{def_stats.get('goals_conceded_per90', 0):.2f}")
                    with col4:
                        st.metric("xGA/90", f"{def_stats.get('xGA_per90', 0):.2f}")
                    
                    st.markdown("---")
                    st.markdown("#### Defensive Quality & Pressing")
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        def_perf = def_stats.get('defensive_performance', 0)
                        st.metric("Defensive Performance", f"{def_perf:+.2f}", 
                                 help="Goals conceded vs xGA (negative = better than expected)")
                    with col2:
                        st.metric("Shots Against/90", f"{def_stats.get('shots_against_per90', 0):.2f}")
                    with col3:
                        st.metric("Deep Allowed/90", f"{def_stats.get('deep_allowed_per90', 0):.2f}", 
                                 help="Opponent passes into final third per 90")
                    with col4:
                        st.metric("PPDA Allowed", f"{def_stats.get('ppda_allowed', 0):.2f}", 
                                 help="Passes per defensive action allowed (lower = more pressing)")
                    
                    # Defensive visualization
                    st.markdown("---")
                    st.markdown("#### Defensive Performance Visualization")
                    
                    # Defensive performance gauge
                    fig = go.Figure(go.Indicator(
                        mode = "gauge+number+delta",
                        value = def_stats.get('defensive_performance', 0),
                        title = {'text': "Defensive Performance vs Expected<br>(negative = better)"},
                        delta = {'reference': 0},
                        gauge = {
                            'axis': {'range': [-15, 15]},
                            'bar': {'color': "darkblue"},
                            'steps': [
                                {'range': [-15, -3], 'color': "lightgreen"},
                                {'range': [-3, 3], 'color': "lightyellow"},
                                {'range': [3, 15], 'color': "lightcoral"}
                            ],
                            'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 0}
                        }
                    ))
                    fig.update_layout(height=300)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.markdown("---")
                    st.caption("*Note: Defensive stats derived from team performance when player was on field.*")
                
                # Attacking contribution
                st.markdown("#### Build-up Play & Attacking Contribution")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("xGBuildup/90", f"{report.get('xGBuildup_per90', 0):.3f}", help="Build-up play contribution")
                with col2:
                    st.metric("xGChain/90", f"{report['xGChain_per90']:.3f}", help="Attacking sequence involvement")
                with col3:
                    st.metric("Key Passes/90", f"{report['key_passes_per90']:.2f}")
                with col4:
                    st.metric("Assists/90", f"{report['assists_per90']:.2f}")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Goals", report['goals'])
                with col2:
                    st.metric("Goals/90", f"{report['goals_per90']:.2f}")
                
                # Discipline
                st.markdown("---")
                st.markdown("#### Discipline")
                if 'yellow_card' in player_profiles.columns:
                    player_data = player_profiles[player_profiles['player_name'] == selected_player].iloc[0]
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Yellow Cards", int(player_data.get('yellow_card', 0)))
                    with col2:
                        st.metric("Red Cards", int(player_data.get('red_card', 0)))
                
            elif pos_group == 'Midfielder':
                st.markdown("### ⚙️ Midfielder Performance Analysis")
                
                # Creative output
                st.markdown("#### Creative Output & Playmaking")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Assists/90", f"{report['assists_per90']:.2f}")
                with col2:
                    st.metric("xA/90", f"{report['xA_per90']:.3f}")
                with col3:
                    st.metric("Key Passes/90", f"{report['key_passes_per90']:.2f}")
                with col4:
                    st.metric("xGChain/90", f"{report['xGChain_per90']:.3f}")
                
                st.markdown("---")
                
                # Goal threat  
                st.markdown("#### Goal Threat & Shooting")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Goals/90", f"{report['goals_per90']:.2f}")
                with col2:
                    st.metric("xG/90", f"{report['xG_per90']:.3f}")
                with col3:
                    st.metric("Shots/90", f"{report['shots_per90']:.2f}")
                with col4:
                    st.metric("xGBuildup/90", f"{report.get('xGBuildup_per90', 0):.3f}")
                
                st.markdown("---")
                
                # Defensive contribution (if available)
                if 'defensive_stats' in report and report['defensive_stats'] is not None:
                    def_stats = report['defensive_stats']
                    st.markdown("#### Defensive Contribution")
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Clean Sheets", int(def_stats.get('clean_sheets', 0)))
                    with col2:
                        st.metric("Clean Sheet %", f"{def_stats.get('clean_sheet_rate', 0):.1f}%")
                    with col3:
                        st.metric("Goals Conceded/90", f"{def_stats.get('goals_conceded_per90', 0):.2f}")
                    
                    st.markdown("---")
                
                # Performance visualization
                st.markdown("#### Attack vs Creativity Balance")
                
                # Radar-style comparison
                fig = go.Figure()
                
                categories = ['Assists/90', 'xA/90', 'Key Passes/90', 'Goals/90', 'xG/90', 'Shots/90']
                values = [
                    report['assists_per90'] * 10,  # Scale for visibility
                    report['xA_per90'] * 10,
                    report['key_passes_per90'],
                    report['goals_per90'] * 10,
                    report['xG_per90'] * 10,
                    report['shots_per90']
                ]
                
                fig.add_trace(go.Scatterpolar(
                    r=values,
                    theta=categories,
                    fill='toself',
                    name=report['player_name']
                ))
                
                fig.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, max(values) * 1.2])),
                    showlegend=False,
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
                
            else:  # Forward
                st.markdown("### ⚽ Forward Performance Analysis")
                
                # Scoring metrics
                st.markdown("#### Scoring & Shot Efficiency")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Goals/90", f"{report['goals_per90']:.2f}")
                with col2:
                    st.metric("xG/90", f"{report['xG_per90']:.3f}")
                with col3:
                    st.metric("Shots/90", f"{report['shots_per90']:.2f}")
                with col4:
                    st.metric("Shot Efficiency", f"{report['shot_efficiency']:.1%}")
                
                st.markdown("---")
                
                # Playmaking
                st.markdown("#### Playmaking & Chance Creation")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Assists/90", f"{report['assists_per90']:.2f}")
                with col2:
                    st.metric("xA/90", f"{report['xA_per90']:.3f}")
                with col3:
                    st.metric("Key Passes/90", f"{report['key_passes_per90']:.2f}")
                with col4:
                    st.metric("xGChain/90", f"{report['xGChain_per90']:.3f}")
                
                st.markdown("---")
                
                # Performance visualization
                st.markdown("#### Scoring Performance Visualization")
                
                # Goals vs xG comparison
                fig = go.Figure()
                
                fig.add_trace(go.Bar(
                    x=['Goals', 'xG'],
                    y=[report['goals'], report.get('xG_per90', 0) * (report['minutes'] / 90)],
                    marker_color=['darkblue', 'lightblue'],
                    text=[f"{report['goals']:.0f}", f"{report.get('xG_per90', 0) * (report['minutes'] / 90):.1f}"],
                    textposition='auto',
                ))
                
                fig.update_layout(
                    title="Goals vs Expected Goals (Total)",
                    yaxis_title="Count",
                    showlegend=False,
                    height=300
                )
                st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("---")
            
            # Performance vs expectation (for attacking players)
            if pos_group in ['Forward', 'Midfielder']:
                st.markdown("### ⚡ Performance vs Expectation")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    delta = report['goals_vs_xG']
                    st.metric("Goals vs xG", f"{delta:+.1f}", f"{'Over' if delta > 0 else 'Under'}performing")
                
                with col2:
                    st.metric("Shot Efficiency", f"{report['shot_efficiency']:.1%}")
                
                with col3:
                    st.metric("Goal Involvement/90", f"{report['goal_involvement_per90']:.2f}")
                
                st.markdown("---")
            
            # Percentiles (if available)
            if 'percentiles' in report and report['percentiles']:
                st.markdown("---")
                st.markdown("### 📈 Position-Specific Percentiles")
                st.markdown(f"*Percentile rankings among all {pos_group}s in the league*")
                
                percentiles_df = pd.DataFrame([report['percentiles']]).T
                percentiles_df.columns = ['Percentile']
                percentiles_df.index.name = 'Metric'
                percentiles_df = percentiles_df.sort_values('Percentile', ascending=False)
                
                # Two columns: bar chart and table
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    fig = px.bar(
                        percentiles_df.reset_index(),
                        x='Percentile',
                        y='Metric',
                        orientation='h',
                        title=f'{report["player_name"]} vs Other {pos_group}s',
                        labels={'Percentile': 'Percentile (%)', 'Metric': ''},
                        color='Percentile',
                        color_continuous_scale='RdYlGn',
                        range_color=[0, 100],
                        height=400
                    )
                    fig.update_layout(yaxis={'categoryorder':'total ascending'})
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.markdown("#### Percentile Summary")
                    for metric, pct in percentiles_df.iterrows():
                        if pct['Percentile'] >= 80:
                            emoji = "🟢"
                        elif pct['Percentile'] >= 50:
                            emoji = "🟡"
                        else:
                            emoji = "🔴"
                        st.markdown(f"{emoji} **{metric}**: {pct['Percentile']:.0f}th")
            
            # Overall assessment summary
            st.markdown("---")
            st.markdown("### 📊 Overall Summary")
            
            summary_col1, summary_col2, summary_col3 = st.columns(3)
            
            with summary_col1:
                st.metric("Total Matches", report['matches'])
                st.metric("Total Minutes", report['minutes'])
            
            with summary_col2:
                st.metric("Minutes per Match", f"{report['minutes_per_match']:.0f}")
                if pos_group in ['Forward', 'Midfielder']:
                    st.metric("Goal Involvement", f"{report.get('goal_involvement_per90', 0) * (report['minutes'] / 90):.0f}")
            
            with summary_col3:
                st.metric("Team", report['team'])
                st.metric("Position", f"{report['position']} ({pos_group})")
        else:
            st.error(report['error'])
    
    with tab3:
        st.markdown("### Find Similar Players")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Single searchable player selector
            players_list = sorted(player_profiles['player_name'].unique())
            reference_player = st.selectbox(
                "Search and select reference player (type to filter):",
                players_list,
                key='similar',
                help="Start typing to filter the list"
            )
        
        with col2:
            n_similar = st.slider("Number of similar players:", 3, 10, 5)
        
        # Find similar players
        similar = scout.find_similar_players(player_profiles, reference_player, n=n_similar)
        
        if len(similar) > 0:
            st.markdown(f"#### Players similar to **{reference_player}**:")
            
            # Display as cards
            for idx, row in similar.iterrows():
                with st.expander(f"**{row['player_name']}** ({row['team_name']}) - Similarity: {row['similarity_score']:.1%}"):
                    # Get available metric columns (exclude base columns)
                    exclude_cols = ['player_name', 'team_name', 'position', 'minutes', 'similarity_score']
                    metric_cols = [col for col in similar.columns if col not in exclude_cols and col.endswith('_per90')]
                    
                    # Create columns dynamically based on available metrics
                    if metric_cols:
                        cols = st.columns(len(metric_cols) + 1)
                        
                        # Display metrics
                        for i, col_name in enumerate(metric_cols):
                            with cols[i]:
                                # Format metric name for display
                                display_name = col_name.replace('_per90', '/90').replace('_', ' ').title()
                                if 'Xg' in display_name:
                                    display_name = display_name.replace('Xg', 'xG')
                                if 'Xa' in display_name:
                                    display_name = display_name.replace('Xa', 'xA')
                                st.metric(display_name, f"{row[col_name]:.2f}")
                        
                        # Minutes in last column
                        with cols[-1]:
                            st.metric("Minutes", int(row['minutes']))
        else:
            st.warning("No similar players found")
