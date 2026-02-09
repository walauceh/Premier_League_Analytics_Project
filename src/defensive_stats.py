"""
Defensive statistics module - derives goalkeeper and defender metrics from team data.
"""

import pandas as pd
import numpy as np


class DefensiveStatsCalculator:
    """Calculate defensive metrics for defenders and goalkeepers from team-level data."""
    
    def __init__(self, team_data, player_data):
        """
        Initialize with team and player data.
        
        Args:
            team_data: Team features DataFrame
            player_data: Player features DataFrame
        """
        self.team_data = team_data.copy()
        self.player_data = player_data.copy()
    
    def calculate_goalkeeper_stats(self, player_name, season=None):
        """
        Calculate goalkeeper-specific statistics.
        
        Args:
            player_name: Name of the goalkeeper
            season: Optional season filter
            
        Returns:
            Dictionary with goalkeeper metrics
        """
        # Get player's matches
        player_matches = self.player_data[self.player_data['player_name'] == player_name].copy()
        
        if season:
            player_matches = player_matches[player_matches['season'] == season]
        
        if len(player_matches) == 0:
            return {'error': 'No matches found'}
        
        # Get team for this player
        team_name = player_matches['team_name'].iloc[0]
        
        # Get corresponding team defensive stats
        team_defensive = self.team_data[
            (self.team_data['team_name'] == team_name) & 
            (self.team_data['date'].isin(player_matches['date']))
        ].copy()
        
        if len(team_defensive) == 0:
            return {'error': 'No team data found'}
        
        # Calculate goalkeeper metrics
        total_matches = len(team_defensive)
        total_minutes = player_matches['minutes'].sum()
        
        # Basic defensive stats
        goals_conceded = team_defensive['goals_against'].sum()
        xGA_total = team_defensive['xGA'].sum()
        shots_on_target_faced = team_defensive['shots_on_target_against'].sum()
        shots_faced = team_defensive['shots_against'].sum()
        
        # Derived goalkeeper stats
        saves = max(0, shots_on_target_faced - goals_conceded)  # Approximation
        save_percentage = (saves / shots_on_target_faced * 100) if shots_on_target_faced > 0 else 0
        
        # Performance vs expectation
        goals_prevented = xGA_total - goals_conceded  # Positive = better than expected
        
        # Clean sheets
        clean_sheets = (team_defensive['goals_against'] == 0).sum()
        clean_sheet_rate = (clean_sheets / total_matches * 100) if total_matches > 0 else 0
        
        # Per 90 stats
        minutes_factor = total_minutes / 90 if total_minutes > 0 else 1
        
        return {
            'player_name': player_name,
            'team': team_name,
            'matches': total_matches,
            'minutes': int(total_minutes),
            
            # Conceding stats
            'goals_conceded': int(goals_conceded),
            'goals_conceded_per90': goals_conceded / minutes_factor,
            'xGA': xGA_total,
            'xGA_per90': xGA_total / minutes_factor,
            
            # Save stats (approximated from team data)
            'shots_faced': int(shots_faced),
            'shots_faced_per90': shots_faced / minutes_factor,
            'shots_on_target_faced': int(shots_on_target_faced),
            'saves_estimate': int(saves),
            'save_percentage': save_percentage,
            
            # Performance metrics
            'goals_prevented': goals_prevented,
            'goals_prevented_per90': goals_prevented / minutes_factor,
            'clean_sheets': int(clean_sheets),
            'clean_sheet_rate': clean_sheet_rate,
            
            # Context
            'note': 'Saves estimated from shots on target - goals conceded. Individual GK data not available in Understat.'
        }
    
    def calculate_defender_stats(self, player_name, season=None):
        """
        Calculate defender-specific statistics.
        
        Args:
            player_name: Name of the defender
            season: Optional season filter
            
        Returns:
            Dictionary with defender metrics
        """
        # Get player's matches
        player_matches = self.player_data[self.player_data['player_name'] == player_name].copy()
        
        if season:
            player_matches = player_matches[player_matches['season'] == season]
        
        if len(player_matches) == 0:
            return {'error': 'No matches found'}
        
        # Get team for this player
        team_name = player_matches['team_name'].iloc[0]
        
        # Get corresponding team defensive stats
        team_defensive = self.team_data[
            (self.team_data['team_name'] == team_name) & 
            (self.team_data['date'].isin(player_matches['date']))
        ].copy()
        
        if len(team_defensive) == 0:
            return {'error': 'No team data found'}
        
        # Calculate defender metrics
        total_matches = len(team_defensive)
        total_minutes = player_matches['minutes'].sum()
        
        # Defensive stats
        goals_conceded = team_defensive['goals_against'].sum()
        xGA_total = team_defensive['xGA'].sum()
        shots_against = team_defensive['shots_against'].sum()
        
        # Pressing/positioning
        ppda_allowed = team_defensive['ppda_allowed'].mean()  # Lower = team presses more
        deep_allowed = team_defensive['deep_allowed'].sum()
        
        # Clean sheets
        clean_sheets = (team_defensive['goals_against'] == 0).sum()
        clean_sheet_rate = (clean_sheets / total_matches * 100) if total_matches > 0 else 0
        
        # Defensive performance
        defensive_performance = goals_conceded - xGA_total  # Negative = better than expected
        
        # Per 90 stats
        minutes_factor = total_minutes / 90 if total_minutes > 0 else 1
        
        # Add attacking contribution from player data
        goals = player_matches['goals'].sum()
        assists = player_matches['assists'].sum()
        xGBuildup = player_matches['xGBuildup'].sum()
        xGChain = player_matches['xGChain'].sum()
        
        return {
            'player_name': player_name,
            'team': team_name,
            'matches': total_matches,
            'minutes': int(total_minutes),
            
            # Defensive stats (team-level)
            'goals_conceded': int(goals_conceded),
            'goals_conceded_per90': goals_conceded / minutes_factor,
            'xGA': xGA_total,
            'xGA_per90': xGA_total / minutes_factor,
            'defensive_performance': defensive_performance,
            'defensive_performance_per90': defensive_performance / minutes_factor,
            
            'shots_against': int(shots_against),
            'shots_against_per90': shots_against / minutes_factor,
            'deep_allowed': int(deep_allowed),
            'deep_allowed_per90': deep_allowed / minutes_factor,
            
            # Pressing
            'ppda_allowed': ppda_allowed,
            
            # Clean sheets
            'clean_sheets': int(clean_sheets),
            'clean_sheet_rate': clean_sheet_rate,
            
            # Attacking contribution (player-level)
            'goals': int(goals),
            'goals_per90': goals / minutes_factor,
            'assists': int(assists),
            'assists_per90': assists / minutes_factor,
            'xGBuildup': xGBuildup,
            'xGBuildup_per90': xGBuildup / minutes_factor,
            'xGChain': xGChain,
            'xGChain_per90': xGChain / minutes_factor,
            
            'note': 'Defensive stats derived from team performance when player was on field.'
        }
    
    def get_league_defensive_rankings(self, position_group, metric, season=None, min_minutes=900):
        """
        Get defensive rankings for a specific metric.
        
        Args:
            position_group: 'Goalkeeper' or 'Defender'
            metric: Metric to rank by
            season: Optional season filter
            min_minutes: Minimum minutes threshold
            
        Returns:
            DataFrame with rankings
        """
        # Filter players by position
        players = self.player_data[self.player_data['position'].str.contains('GK|DF|D', regex=True, na=False)]
        
        if season:
            players = players[players['season'] == season]
        
        # Group by player and calculate total minutes
        player_totals = players.groupby('player_name').agg({
            'minutes': 'sum',
            'team_name': 'first'
        }).reset_index()
        
        # Filter by minimum minutes
        qualified_players = player_totals[player_totals['minutes'] >= min_minutes]
        
        # Calculate stats for each player
        results = []
        for _, player in qualified_players.iterrows():
            if position_group == 'Goalkeeper':
                stats = self.calculate_goalkeeper_stats(player['player_name'], season)
            else:
                stats = self.calculate_defender_stats(player['player_name'], season)
            
            if 'error' not in stats and metric in stats:
                results.append(stats)
        
        if not results:
            return pd.DataFrame()
        
        df = pd.DataFrame(results)
        
        # Sort by metric (descending for positive metrics, ascending for negative)
        ascending = metric in ['goals_conceded_per90', 'xGA_per90', 'shots_against_per90', 
                               'deep_allowed_per90', 'ppda_allowed']
        
        return df.sort_values(metric, ascending=ascending).reset_index(drop=True)
