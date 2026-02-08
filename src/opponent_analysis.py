"""
Opponent analysis module for match preparation.
Provides tactical insights and recommendations for upcoming matches.
"""

import pandas as pd
import numpy as np
from typing import Dict, List
import warnings
warnings.filterwarnings('ignore')


class OpponentAnalyzer:
    """Analyzes opponents and provides match preparation insights."""
    
    def __init__(self, team_data: pd.DataFrame, player_data: pd.DataFrame = None):
        """
        Initialize with team and optional player data.
        
        Args:
            team_data: Team features DataFrame
            player_data: Optional player features DataFrame
        """
        self.team_data = team_data.copy()
        self.player_data = player_data
        self.team_data['date'] = pd.to_datetime(self.team_data['date'])
        
    def get_opponent_profile(self, opponent_name: str, 
                            last_n_matches: int = 10) -> Dict:
        """
        Create comprehensive opponent profile.
        
        Args:
            opponent_name: Name of opponent team
            last_n_matches: Number of recent matches to analyze
            
        Returns:
            Dictionary with opponent analysis
        """
        opponent_data = (self.team_data[self.team_data['team_name'] == opponent_name]
                        .sort_values('date')
                        .tail(last_n_matches))
        
        if len(opponent_data) == 0:
            return {"error": "Opponent not found"}
        
        profile = {
            'team_name': opponent_name,
            'matches_analyzed': len(opponent_data),
            'date_range': (
                opponent_data['date'].min().strftime('%Y-%m-%d'),
                opponent_data['date'].max().strftime('%Y-%m-%d')
            ),
            
            # Overall form
            'form': {
                'ppg': float(opponent_data['points'].mean()),
                'wins': int((opponent_data['result'] == 'W').sum()),
                'draws': int((opponent_data['result'] == 'D').sum()),
                'losses': int((opponent_data['result'] == 'L').sum()),
                'form_trend': float(opponent_data['form_trend'].mean()) if 'form_trend' in opponent_data.columns else 0,
            },
            
            # Attack
            'attack': {
                'goals_per_game': float(opponent_data['goals_for'].mean()),
                'xG_per_game': float(opponent_data['xG'].mean()),
                'shots_per_game': float(opponent_data['shots'].mean()),
                'shot_accuracy': float(opponent_data['shot_accuracy'].mean()),
                'shot_quality': float(opponent_data['shot_quality'].mean()),
                'goals_vs_xG': float((opponent_data['goals_for'] - opponent_data['xG']).mean()),
            },
            
            # Defense
            'defense': {
                'goals_conceded_per_game': float(opponent_data['goals_against'].mean()),
                'xGA_per_game': float(opponent_data['xGA'].mean()),
                'shots_conceded_per_game': float(opponent_data['shots_against'].mean()),
                'clean_sheets': int(opponent_data['clean_sheet'].sum()) if 'clean_sheet' in opponent_data.columns else 0,
                'goals_conceded_vs_xGA': float((opponent_data['goals_against'] - opponent_data['xGA']).mean()),
            },
            
            # Style
            'style': {
                'pressing_intensity': float(opponent_data['pressing_intensity'].mean()) if 'pressing_intensity' in opponent_data.columns else 0,
                'deep_completions': float(opponent_data['deep'].mean()),
                'ppda': float(opponent_data['ppda'].mean()),
                'attacking_intensity': float(opponent_data['attacking_intensity'].mean()) if 'attacking_intensity' in opponent_data.columns else 0,
            },
            
            # Home vs Away
            'venue_splits': {
                'home_ppg': float(opponent_data[opponent_data['venue'] == 'Home']['points'].mean()) if (opponent_data['venue'] == 'Home').any() else 0,
                'away_ppg': float(opponent_data[opponent_data['venue'] == 'Away']['points'].mean()) if (opponent_data['venue'] == 'Away').any() else 0,
                'home_goals_pg': float(opponent_data[opponent_data['venue'] == 'Home']['goals_for'].mean()) if (opponent_data['venue'] == 'Home').any() else 0,
                'away_goals_pg': float(opponent_data[opponent_data['venue'] == 'Away']['goals_for'].mean()) if (opponent_data['venue'] == 'Away').any() else 0,
            },
        }
        
        return profile
    
    def identify_strengths_weaknesses(self, profile: Dict) -> Dict:
        """
        Identify key strengths and weaknesses from opponent profile.
        
        Args:
            profile: Opponent profile dictionary
            
        Returns:
            Dictionary with strengths and weaknesses
        """
        if 'error' in profile:
            return profile
        
        strengths = []
        weaknesses = []
        
        # Attack analysis
        if profile['attack']['goals_per_game'] > 1.5:
            strengths.append(f"Strong attack ({profile['attack']['goals_per_game']:.1f} goals/game)")
        elif profile['attack']['goals_per_game'] < 1.0:
            weaknesses.append(f"Weak attack ({profile['attack']['goals_per_game']:.1f} goals/game)")
        
        if profile['attack']['shot_accuracy'] > 0.40:
            strengths.append(f"High shot accuracy ({profile['attack']['shot_accuracy']:.0%})")
        elif profile['attack']['shot_accuracy'] < 0.30:
            weaknesses.append(f"Low shot accuracy ({profile['attack']['shot_accuracy']:.0%})")
        
        # Defense analysis
        if profile['defense']['goals_conceded_per_game'] < 1.0:
            strengths.append(f"Solid defense ({profile['defense']['goals_conceded_per_game']:.1f} conceded/game)")
        elif profile['defense']['goals_conceded_per_game'] > 1.5:
            weaknesses.append(f"Vulnerable defense ({profile['defense']['goals_conceded_per_game']:.1f} conceded/game)")
        
        if profile['defense']['clean_sheets'] >= 3:
            strengths.append(f"Good at keeping clean sheets ({profile['defense']['clean_sheets']} in last {profile['matches_analyzed']})")
        
        # Style analysis
        if profile['style']['pressing_intensity'] > 0.10:
            strengths.append("High pressing intensity")
        elif profile['style']['pressing_intensity'] < 0.08:
            weaknesses.append("Low pressing intensity - sits deep")
        
        # Form analysis
        if profile['form']['ppg'] >= 2.0:
            strengths.append(f"Excellent form ({profile['form']['ppg']:.2f} PPG)")
        elif profile['form']['ppg'] < 1.0:
            weaknesses.append(f"Poor form ({profile['form']['ppg']:.2f} PPG)")
        
        # Performance vs expectation
        if profile['attack']['goals_vs_xG'] > 0.2:
            strengths.append(f"Overperforming xG (+{profile['attack']['goals_vs_xG']:.1f})")
        elif profile['attack']['goals_vs_xG'] < -0.2:
            weaknesses.append(f"Underperforming xG ({profile['attack']['goals_vs_xG']:.1f})")
        
        return {
            'strengths': strengths,
            'weaknesses': weaknesses
        }
    
    def generate_game_plan(self, own_team: str, opponent: str,
                          last_n_matches: int = 10) -> Dict:
        """
        Generate tactical game plan for facing an opponent.
        
        Args:
            own_team: Your team name
            opponent: Opponent team name
            last_n_matches: Number of recent matches to analyze
            
        Returns:
            Dictionary with game plan recommendations
        """
        # Get profiles
        own_profile = self.get_opponent_profile(own_team, last_n_matches)
        opp_profile = self.get_opponent_profile(opponent, last_n_matches)
        
        if 'error' in own_profile or 'error' in opp_profile:
            return {"error": "Team not found"}
        
        # Identify strengths/weaknesses
        own_sw = self.identify_strengths_weaknesses(own_profile)
        opp_sw = self.identify_strengths_weaknesses(opp_profile)
        
        recommendations = []
        
        # Attacking recommendations
        if opp_profile['defense']['goals_conceded_per_game'] > 1.3:
            recommendations.append({
                'area': 'Attack',
                'insight': f"Opponent concedes {opp_profile['defense']['goals_conceded_per_game']:.1f} goals/game",
                'recommendation': 'Press high and attack with intensity. Exploit defensive vulnerabilities.'
            })
        
        if opp_profile['style']['pressing_intensity'] < 0.08:
            recommendations.append({
                'area': 'Build-up',
                'insight': 'Opponent sits deep with low pressing',
                'recommendation': 'Patient build-up play. Use possession to draw them out.'
            })
        
        # Defensive recommendations
        if opp_profile['attack']['goals_per_game'] > 1.5:
            recommendations.append({
                'area': 'Defense',
                'insight': f"Opponent scores {opp_profile['attack']['goals_per_game']:.1f} goals/game",
                'recommendation': 'Stay compact defensively. Avoid leaving spaces in behind.'
            })
        
        if opp_profile['attack']['shot_quality'] > 0.15:
            recommendations.append({
                'area': 'Defense',
                'insight': 'Opponent creates high-quality chances',
                'recommendation': 'Block passing lanes to prevent dangerous chances.'
            })
        
        # Style matchup
        if own_profile['style']['pressing_intensity'] > opp_profile['style']['pressing_intensity']:
            recommendations.append({
                'area': 'Style Matchup',
                'insight': 'You have higher pressing intensity',
                'recommendation': 'Use your pressing advantage to force errors and win the ball high.'
            })
        
        # Form consideration
        if opp_profile['form']['ppg'] < 1.0:
            recommendations.append({
                'area': 'Form',
                'insight': f"Opponent in poor form ({opp_profile['form']['ppg']:.2f} PPG)",
                'recommendation': 'Take advantage of low confidence. Play with aggression.'
            })
        
        game_plan = {
            'own_team': own_team,
            'opponent': opponent,
            'own_profile': own_profile,
            'opponent_profile': opp_profile,
            'own_strengths_weaknesses': own_sw,
            'opponent_strengths_weaknesses': opp_sw,
            'recommendations': recommendations,
            'key_matchup_areas': {
                'attack_vs_defense': {
                    'own_attack': own_profile['attack']['xG_per_game'],
                    'opp_defense': opp_profile['defense']['xGA_per_game'],
                    'advantage': own_team if own_profile['attack']['xG_per_game'] > opp_profile['defense']['xGA_per_game'] else opponent
                },
                'defense_vs_attack': {
                    'own_defense': own_profile['defense']['xGA_per_game'],
                    'opp_attack': opp_profile['attack']['xG_per_game'],
                    'advantage': own_team if own_profile['defense']['xGA_per_game'] < opp_profile['attack']['xG_per_game'] else opponent
                }
            }
        }
        
        return game_plan
    
    def get_head_to_head_history(self, team1: str, team2: str) -> pd.DataFrame:
        """
        Get head-to-head match history between two teams.
        
        Args:
            team1: First team name
            team2: Second team name
            
        Returns:
            DataFrame with head-to-head matches
        """
        # Get matches where both teams played against each other
        h2h = self.team_data[
            ((self.team_data['team_name'] == team1) & (self.team_data['opponent'] == team2)) |
            ((self.team_data['team_name'] == team2) & (self.team_data['opponent'] == team1))
        ].sort_values('date')
        
        # Get team1 perspective
        team1_matches = h2h[h2h['team_name'] == team1][
            ['date', 'venue', 'goals_for', 'goals_against', 'result', 'xG', 'xGA']
        ].copy()
        
        return team1_matches


def main():
    """Demonstrate opponent analysis functionality."""
    print("="*60)
    print("OPPONENT ANALYSIS")
    print("="*60)
    
    # Load team features
    print("\n📂 Loading team features...")
    team_df = pd.read_csv("./data/team_features_complete.csv")
    team_df['date'] = pd.to_datetime(team_df['date'])
    
    # Initialize analyzer
    analyzer = OpponentAnalyzer(team_df)
    
    # Get opponent profile
    print("\n🔍 Analyzing opponent: Liverpool")
    print("="*60)
    
    profile = analyzer.get_opponent_profile("Liverpool", last_n_matches=10)
    
    if 'error' not in profile:
        print(f"\nLiverpool - Last {profile['matches_analyzed']} matches")
        print(f"Period: {profile['date_range'][0]} to {profile['date_range'][1]}")
        
        print(f"\n📊 Form:")
        print(f"  PPG: {profile['form']['ppg']:.2f}")
        print(f"  Record: {profile['form']['wins']}W-{profile['form']['draws']}D-{profile['form']['losses']}L")
        
        print(f"\n⚔️ Attack:")
        print(f"  Goals/game: {profile['attack']['goals_per_game']:.2f}")
        print(f"  xG/game: {profile['attack']['xG_per_game']:.2f}")
        print(f"  Shot accuracy: {profile['attack']['shot_accuracy']:.1%}")
        
        print(f"\n🛡️ Defense:")
        print(f"  Goals conceded/game: {profile['defense']['goals_conceded_per_game']:.2f}")
        print(f"  xGA/game: {profile['defense']['xGA_per_game']:.2f}")
        print(f"  Clean sheets: {profile['defense']['clean_sheets']}")
        
        # Strengths and weaknesses
        print("\n" + "="*60)
        print("STRENGTHS & WEAKNESSES")
        print("="*60)
        
        sw = analyzer.identify_strengths_weaknesses(profile)
        
        print("\n✅ Strengths:")
        for strength in sw['strengths']:
            print(f"  • {strength}")
        
        print("\n⚠️ Weaknesses:")
        for weakness in sw['weaknesses']:
            print(f"  • {weakness}")
    
    # Generate game plan
    print("\n" + "="*60)
    print("GAME PLAN GENERATOR")
    print("="*60)
    
    teams_available = team_df['team_name'].unique()
    if "Manchester City" in teams_available and "Liverpool" in teams_available:
        print("\nGenerating game plan: Manchester City vs Liverpool")
        
        game_plan = analyzer.generate_game_plan("Manchester City", "Liverpool", last_n_matches=10)
        
        if 'error' not in game_plan:
            print(f"\n🎯 Key Matchups:")
            print(f"  Attack vs Defense: Advantage {game_plan['key_matchup_areas']['attack_vs_defense']['advantage']}")
            print(f"  Defense vs Attack: Advantage {game_plan['key_matchup_areas']['defense_vs_attack']['advantage']}")
            
            print(f"\n📋 Tactical Recommendations:")
            for rec in game_plan['recommendations'][:5]:  # Show first 5
                print(f"\n  {rec['area']}:")
                print(f"    • {rec['insight']}")
                print(f"    → {rec['recommendation']}")
    
    print("\n" + "="*60)
    print("✅ Opponent analysis complete!")
    print("="*60)


if __name__ == "__main__":
    main()
