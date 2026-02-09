"""Player scouting utilities for finding and analyzing players."""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity


class PlayerScout:
    """Player scouting and analysis toolkit."""
    
    def __init__(self, team_data=None, player_data=None):
        """Initialize PlayerScout with optional team and player data for defensive stats."""
        self.team_data = team_data
        self.player_data = player_data
        self.defensive_calc = None
        
        # Initialize defensive calculator if data is available
        if team_data is not None and player_data is not None:
            try:
                from defensive_stats import DefensiveStatsCalculator
                self.defensive_calc = DefensiveStatsCalculator(team_data, player_data)
            except Exception as e:
                print(f"Warning: Could not initialize defensive stats calculator: {e}")
        # All available features
        self.all_features_per90 = [
            'goals_per90', 'assists_per90', 'xG_per90', 'xA_per90',
            'shots_per90', 'key_passes_per90', 'xGChain_per90', 'xGBuildup_per90'
        ]
        
        # Position-specific feature weights for similarity analysis
        self.position_groups = {
            'Forward': ['goals_per90', 'xG_per90', 'shots_per90', 'xGChain_per90', 'assists_per90', 'key_passes_per90'],
            'Midfielder': ['assists_per90', 'xA_per90', 'key_passes_per90', 'xGChain_per90', 'xGBuildup_per90', 'goals_per90'],
            'Defender': ['xGBuildup_per90', 'xGChain_per90', 'clean_sheet_rate', 'goals_conceded_per90', 'defensive_performance_per90', 'ppda_allowed'],
            'Goalkeeper': ['save_percentage', 'goals_prevented_per90', 'clean_sheet_rate', 'goals_conceded_per90', 'xGA_per90']
        }
        
        # Position-specific display metrics (what to show in reports)
        self.position_display_metrics = {
            'Forward': {
                'primary': ['goals_per90', 'xG_per90', 'shots_per90', 'assists_per90'],
                'secondary': ['xA_per90', 'key_passes_per90', 'xGChain_per90'],
                'labels': {
                    'goals_per90': 'Goals/90',
                    'xG_per90': 'xG/90',
                    'shots_per90': 'Shots/90',
                    'assists_per90': 'Assists/90',
                    'xA_per90': 'xA/90',
                    'key_passes_per90': 'Key Passes/90',
                    'xGChain_per90': 'xGChain/90'
                }
            },
            'Midfielder': {
                'primary': ['assists_per90', 'key_passes_per90', 'xA_per90', 'xGChain_per90'],
                'secondary': ['goals_per90', 'xG_per90', 'xGBuildup_per90', 'shots_per90'],
                'labels': {
                    'assists_per90': 'Assists/90',
                    'key_passes_per90': 'Key Passes/90',
                    'xA_per90': 'xA/90',
                    'xGChain_per90': 'xGChain/90',
                    'goals_per90': 'Goals/90',
                    'xG_per90': 'xG/90',
                    'xGBuildup_per90': 'xGBuildup/90',
                    'shots_per90': 'Shots/90'
                }
            },
            'Defender': {
                'primary': ['clean_sheet_rate', 'goals_conceded_per90', 'defensive_performance_per90', 'xGBuildup_per90'],
                'secondary': ['xGChain_per90', 'ppda_allowed', 'assists_per90', 'yellow_card'],
                'labels': {
                    'clean_sheet_rate': 'Clean Sheet %',
                    'goals_conceded_per90': 'Goals Conceded/90',
                    'defensive_performance_per90': 'Defensive Performance/90',
                    'xGBuildup_per90': 'xGBuildup/90 (Build-up Play)',
                    'xGChain_per90': 'xGChain/90 (Attack Involvement)',
                    'ppda_allowed': 'PPDA Allowed',
                    'key_passes_per90': 'Key Passes/90',
                    'assists_per90': 'Assists/90',
                    'yellow_card': 'Yellow Cards',
                    'red_card': 'Red Cards',
                    'goals_per90': 'Goals/90'
                }
            },
            'Goalkeeper': {
                'primary': ['save_percentage', 'goals_prevented_per90', 'clean_sheet_rate', 'goals_conceded_per90'],
                'secondary': ['xGA_per90', 'xGBuildup_per90', 'xGChain_per90'],
                'labels': {
                    'save_percentage': 'Save %',
                    'goals_prevented_per90': 'Goals Prevented/90',
                    'clean_sheet_rate': 'Clean Sheet %',
                    'goals_conceded_per90': 'Goals Conceded/90',
                    'xGA_per90': 'xGA/90',
                    'xGBuildup_per90': 'xGBuildup/90 (Distribution)',
                    'xGChain_per90': 'xGChain/90 (Attack Involvement)',
                    'key_passes_per90': 'Key Passes/90',
                    'yellow_card': 'Yellow Cards'
                }
            }
        }
    
    def normalize_position(self, pos):
        """Simplify position to Forward, Midfielder, Defender, or Goalkeeper."""
        pos = str(pos).upper()
        if 'GK' in pos:
            return 'Goalkeeper'
        elif 'FW' in pos or 'ST' in pos or 'CF' in pos:
            return 'Forward'
        elif 'MF' in pos or 'AM' in pos or 'DM' in pos or 'M' in pos:
            return 'Midfielder'
        elif 'DF' in pos or 'CB' in pos or 'FB' in pos or 'WB' in pos or 'D' in pos:
            return 'Defender'
        else:
            return 'Midfielder'
    
    def get_position_relevant_metrics(self, position_group):
        """Get the most relevant metrics for a position."""
        metrics = self.position_display_metrics.get(position_group, self.position_display_metrics['Midfielder'])
        return metrics['primary'] + metrics['secondary']
    
    def get_top_players_by_metric(self, player_profiles, metric, position_filter=None, 
                                   min_minutes=900, n=20):
        """
        Get top N players by a specific metric.
        
        Args:
            player_profiles: DataFrame with player data
            metric: Column name to rank by
            position_filter: Position to filter by (e.g., 'FWD', 'MID', 'DEF')
            min_minutes: Minimum minutes played
            n: Number of players to return
            
        Returns:
            DataFrame with top players
        """
        df = player_profiles.copy()
        
        # Filter by minutes
        df = df[df['minutes'] >= min_minutes]
        
        # Filter by position if specified
        if position_filter:
            # Ensure position_group exists
            if 'position_group' not in df.columns:
                df['position_group'] = df['position'].apply(self.normalize_position)
            
            # Map position filter
            pos_map = {
                'FWD': 'Forward',
                'MID': 'Midfielder', 
                'DEF': 'Defender'
            }
            position_group = pos_map.get(position_filter, position_filter)
            df = df[df['position_group'] == position_group]
        
        # Sort by metric
        if metric in df.columns:
            df = df.nlargest(n, metric)
            return df[['player_name', 'team_name', 'position', 'minutes', metric]].reset_index(drop=True)
        else:
            return pd.DataFrame()
    
    def create_player_report(self, player_profiles, player_name):
        """
        Create a detailed report for a player.
        
        Args:
            player_profiles: DataFrame with player data
            player_name: Name of player
            
        Returns:
            Dictionary with player report data
        """
        player_data = player_profiles[player_profiles['player_name'] == player_name]
        
        if len(player_data) == 0:
            return {'error': f"Player '{player_name}' not found"}
        
        player = player_data.iloc[0]
        
        # Ensure position_group exists
        if 'position_group' not in player.index:
            pos_group = self.normalize_position(player.get('position', ''))
        else:
            pos_group = player['position_group']
        
        # Basic info
        report = {
            'player_name': player['player_name'],
            'team': player.get('team_name', 'Unknown'),
            'position': player.get('position', 'Unknown'),
            'position_group': pos_group,
            'matches': int(player.get('appearances', 0)),
            'minutes': int(player.get('minutes', 0)),
            'minutes_per_match': player.get('minutes', 0) / max(player.get('appearances', 1), 1),
            'goals': int(player.get('goals', 0)),
        }
        
        # Performance metrics (per 90)
        report['goals_per90'] = player.get('goals_per90', 0)
        report['assists_per90'] = player.get('assists_per90', 0)
        report['goal_involvement_per90'] = (
            player.get('goals_per90', 0) + player.get('assists_per90', 0)
        )
        report['key_passes_per90'] = player.get('key_passes_per90', 0)
        
        # Expected stats
        report['xG_per90'] = player.get('xG_per90', 0)
        report['xA_per90'] = player.get('xA_per90', 0)
        report['xG_involvement_per90'] = (
            player.get('xG_per90', 0) + player.get('xA_per90', 0)
        )
        report['shots_per90'] = player.get('shots_per90', 0)
        report['xGChain_per90'] = player.get('xGChain_per90', 0)
        
        # Performance vs expectation
        goals = player.get('goals', 0)
        xG = player.get('xG', 0)
        report['goals_vs_xG'] = goals - xG
        
        shots = player.get('shots', 0)
        report['shot_efficiency'] = goals / shots if shots > 0 else 0
        
        # Percentiles - use position-specific metrics
        percentiles = {}
        relevant_metrics = self.get_position_relevant_metrics(pos_group)
        
        for feature in relevant_metrics:
            pct_col = f'{feature}_pct'
            if pct_col in player.index:
                # Get friendly label
                label = feature
                if pos_group in self.position_display_metrics:
                    label = self.position_display_metrics[pos_group]['labels'].get(feature, feature)
                percentiles[label] = player[pct_col]
        
        if percentiles:
            report['percentiles'] = percentiles
        
        # Add defensive stats for goalkeepers and defenders from DataFrame columns
        # These were pre-calculated in app.py during data loading
        if pos_group in ['Goalkeeper', 'Defender']:
            defensive_stats = {}
            
            if pos_group == 'Goalkeeper':
                # Get goalkeeper-specific defensive metrics from DataFrame columns
                gk_metrics = {
                    'save_percentage': player.get('save_percentage', 0),
                    'goals_prevented': player.get('goals_prevented_per90', 0) * (player.get('minutes', 0) / 90) if player.get('minutes', 0) > 0 else 0,
                    'goals_prevented_per90': player.get('goals_prevented_per90', 0),
                    'clean_sheet_rate': player.get('clean_sheet_rate', 0),
                    'clean_sheets': int(player.get('clean_sheet_rate', 0) / 100 * player.get('appearances', 0)) if player.get('appearances', 0) > 0 else 0,
                    'goals_conceded_per90': player.get('goals_conceded_per90', 0),
                    'goals_conceded': player.get('goals_conceded_per90', 0) * (player.get('minutes', 0) / 90) if player.get('minutes', 0) > 0 else 0,
                    'xGA_per90': player.get('xGA_per90', 0),
                    'minutes': int(player.get('minutes', 0)),
                    'matches': int(player.get('appearances', 0)),
                    'shots_faced_per90': player.get('shots_per90', 0),  # Approximation from general stats
                    'shots_on_target_faced': 0,  # Not available
                    'saves_estimate': int(player.get('save_percentage', 0) / 100 * player.get('shots_per90', 0) * (player.get('minutes', 0) / 90)) if player.get('minutes', 0) > 0 else 0
                }
                
                # Only add if we have meaningful data (at least save_percentage or goals_prevented)
                if gk_metrics['save_percentage'] > 0 or abs(gk_metrics['goals_prevented_per90']) > 0.01:
                    defensive_stats = gk_metrics
                
            elif pos_group == 'Defender':
                # Get defender-specific defensive metrics from DataFrame columns
                def_metrics = {
                    'clean_sheet_rate': player.get('clean_sheet_rate', 0),
                    'clean_sheets': int(player.get('clean_sheet_rate', 0) / 100 * player.get('appearances', 0)) if player.get('appearances', 0) > 0 else 0,
                    'goals_conceded_per90': player.get('goals_conceded_per90', 0),
                    'goals_conceded': player.get('goals_conceded_per90', 0) * (player.get('minutes', 0) / 90) if player.get('minutes', 0) > 0 else 0,
                    'xGA_per90': player.get('xGA_per90', 0),
                    'defensive_performance': player.get('defensive_performance_per90', 0) * (player.get('minutes', 0) / 90) if player.get('minutes', 0) > 0 else 0,
                    'defensive_performance_per90': player.get('defensive_performance_per90', 0),
                    'ppda_allowed': player.get('ppda_allowed', 0),
                    'shots_against_per90': player.get('shots_per90', 0),  # Approximation
                    'deep_allowed_per90': 0,  # Not available
                    'minutes': int(player.get('minutes', 0)),
                    'matches': int(player.get('appearances', 0))
                }
                
                # Only add if we have meaningful data
                if def_metrics['clean_sheet_rate'] > 0 or abs(def_metrics['defensive_performance_per90']) > 0.01:
                    defensive_stats = def_metrics
            
            # Add to report if we have data
            if defensive_stats:
                report['defensive_stats'] = defensive_stats
        
        # Add defensive contribution for midfielders if available
        elif pos_group == 'Midfielder':
            # Check if defensive metrics are available for midfielders
            if player.get('clean_sheet_rate', 0) > 0 or player.get('defensive_performance_per90', 0) != 0:
                defensive_stats = {
                    'clean_sheet_rate': player.get('clean_sheet_rate', 0),
                    'clean_sheets': int(player.get('clean_sheet_rate', 0) / 100 * player.get('appearances', 0)) if player.get('appearances', 0) > 0 else 0,
                    'goals_conceded_per90': player.get('goals_conceded_per90', 0),
                    'defensive_performance_per90': player.get('defensive_performance_per90', 0),
                    'matches': int(player.get('appearances', 0))
                }
                report['defensive_stats'] = defensive_stats
        
        # Add position-specific context
        report['position_context'] = self._get_position_context(pos_group)
        
        return report
    
    def _get_position_context(self, position_group):
        """Get contextual information about what matters for each position."""
        contexts = {
            'Forward': 'Forwards are evaluated primarily on goal-scoring ability, shot volume, and direct goal involvement.',
            'Midfielder': 'Midfielders are assessed on creative output (assists, key passes), build-up play contribution, and goal threat.',
            'Defender': 'Defenders are evaluated on build-up play contribution and discipline. Note: Understat data lacks defensive-specific metrics (tackles, clearances, blocks).',
            'Goalkeeper': 'Limited metrics available - Understat data does not include goalkeeper-specific stats (saves, save %, distribution).'
        }
        return contexts.get(position_group, '')
    
    def find_similar_players(self, player_profiles, player_name, n=5, position_group=None):
        """
        Find players similar to a given player.
        
        Args:
            player_profiles: DataFrame with player data
            player_name: Name of reference player
            n: Number of similar players to return
            position_group: Optional position group filter
            
        Returns:
            DataFrame with similar players
        """
        # Get player data
        player_data = player_profiles[player_profiles['player_name'] == player_name]
        
        if len(player_data) == 0:
            return pd.DataFrame()
        
        player_data = player_data.iloc[0]
        
        # Ensure position_group exists
        if 'position_group' not in player_data.index:
            player_pos = self.normalize_position(player_data.get('position', ''))
        else:
            player_pos = player_data['position_group']
        
        # Ensure all candidates have position_group
        candidates = player_profiles.copy()
        if 'position_group' not in candidates.columns:
            candidates['position_group'] = candidates['position'].apply(self.normalize_position)
        
        # Filter by position group
        if position_group:
            candidates = candidates[candidates['position_group'] == position_group]
        else:
            candidates = candidates[candidates['position_group'] == player_pos]
        
        # Remove the player themselves
        candidates = candidates[candidates['player_name'] != player_name]
        
        if len(candidates) == 0:
            return pd.DataFrame()
        
        # Use position-relevant features based on player's position
        if player_pos in self.position_groups:
            feature_cols = self.position_groups[player_pos]
        else:
            feature_cols = self.all_features_per90
        
        # Check which features are available
        available_features = [f for f in feature_cols if f in candidates.columns]
        if not available_features:
            return pd.DataFrame()
        
        # Prepare data - convert to float to avoid downcasting warnings
        X = candidates[available_features].astype(float).fillna(0.0)
        
        # For player, create a DataFrame to avoid sklearn warning
        player_vals = player_data[available_features].values
        player_vals = np.nan_to_num(player_vals, nan=0.0)
        player_df = pd.DataFrame([player_vals], columns=available_features)
        
        # Standardize
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        player_scaled = scaler.transform(player_df)
        
        # Calculate similarity
        similarities = cosine_similarity(player_scaled, X_scaled)[0]
        candidates = candidates.copy()
        candidates['similarity_score'] = similarities
        
        # Get top matches
        top_matches = candidates.nlargest(n, 'similarity_score')
        
        # Position-specific result columns
        base_cols = ['player_name', 'team_name', 'position', 'minutes']
        
        if player_pos == 'Goalkeeper':
            metric_cols = ['save_percentage', 'goals_prevented_per90', 'clean_sheet_rate', 'goals_conceded_per90']
        elif player_pos == 'Defender':
            metric_cols = ['clean_sheet_rate', 'goals_conceded_per90', 'defensive_performance_per90', 'xGBuildup_per90']
        elif player_pos == 'Midfielder':
            metric_cols = ['assists_per90', 'key_passes_per90', 'xA_per90', 'goals_per90']
        else:  # Forward
            metric_cols = ['goals_per90', 'assists_per90', 'xG_per90', 'shots_per90']
        
        result_cols = base_cols + metric_cols + ['similarity_score']
        
        # Only include columns that exist
        result_cols = [c for c in result_cols if c in top_matches.columns]
        
        return top_matches[result_cols].reset_index(drop=True)
