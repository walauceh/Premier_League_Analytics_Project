"""
Time simulation framework to ensure no future data leakage.
Allows filtering data as if viewing it at a specific point in the season.
"""

import pandas as pd
from datetime import datetime
from typing import Optional, List, Dict


class TimeSimulator:
    """
    Manages time-aware data filtering to simulate viewing data at different points in time.
    This ensures no future data leakage in analysis and modeling.
    """
    
    def __init__(self, team_data: pd.DataFrame, player_data: pd.DataFrame):
        """
        Initialize with team and player datasets.
        
        Args:
            team_data: DataFrame with team-match data (must have 'date' column)
            player_data: DataFrame with player-match data (must have 'date' column)
        """
        self.team_data = team_data.copy()
        self.player_data = player_data.copy()
        
        # Ensure date columns are datetime
        self.team_data['date'] = pd.to_datetime(self.team_data['date'])
        self.player_data['date'] = pd.to_datetime(self.player_data['date'])
        
        # Store date ranges
        self.min_date = min(self.team_data['date'].min(), self.player_data['date'].min())
        self.max_date = max(self.team_data['date'].max(), self.player_data['date'].max())
        
        # Current simulation date (defaults to latest available data)
        self.simulation_date = self.max_date
        
    def set_simulation_date(self, date: datetime or str) -> None:
        """
        Set the simulation date. All queries will return data <= this date.
        
        Args:
            date: The simulation date (datetime object or string in YYYY-MM-DD format)
        """
        if isinstance(date, str):
            date = pd.to_datetime(date)
        
        if date < self.min_date or date > self.max_date:
            print(f"Warning: Date {date} is outside available data range "
                  f"({self.min_date.date()} to {self.max_date.date()})")
        
        self.simulation_date = date
        print(f"Simulation date set to: {self.simulation_date.date()}")
        
    def get_data_as_of(self, date: Optional[datetime or str] = None) -> Dict[str, pd.DataFrame]:
        """
        Get all data as of a specific date (or current simulation date).
        
        Args:
            date: Optional date to query. If None, uses current simulation_date.
            
        Returns:
            Dictionary with 'team_data' and 'player_data' keys
        """
        if date is None:
            date = self.simulation_date
        elif isinstance(date, str):
            date = pd.to_datetime(date)
            
        team_filtered = self.team_data[self.team_data['date'] <= date].copy()
        player_filtered = self.player_data[self.player_data['date'] <= date].copy()
        
        return {
            'team_data': team_filtered,
            'player_data': player_filtered,
            'simulation_date': date
        }
    
    def get_team_data(self, team_name: Optional[str] = None, 
                     date: Optional[datetime or str] = None) -> pd.DataFrame:
        """
        Get team data up to simulation date, optionally filtered by team.
        
        Args:
            team_name: Optional team name to filter
            date: Optional date override
            
        Returns:
            DataFrame of team match data
        """
        data = self.get_data_as_of(date)['team_data']
        
        if team_name:
            data = data[data['team_name'] == team_name]
            
        return data
    
    def get_player_data(self, player_name: Optional[str] = None,
                       team_name: Optional[str] = None,
                       position: Optional[str] = None,
                       date: Optional[datetime or str] = None,
                       min_minutes: int = 0) -> pd.DataFrame:
        """
        Get player data up to simulation date with optional filters.
        
        Args:
            player_name: Optional player name filter
            team_name: Optional team name filter
            position: Optional position filter
            date: Optional date override
            min_minutes: Minimum minutes played filter
            
        Returns:
            DataFrame of player match data
        """
        data = self.get_data_as_of(date)['player_data']
        
        if player_name:
            data = data[data['player_name'] == player_name]
        if team_name:
            data = data[data['team_name'] == team_name]
        if position:
            data = data[data['position'] == position]
        if min_minutes > 0:
            data = data[data['minutes'] >= min_minutes]
            
        return data
    
    def get_season_data(self, season: str, date: Optional[datetime or str] = None) -> Dict[str, pd.DataFrame]:
        """
        Get data for a specific season up to simulation date.
        
        Args:
            season: Season string (e.g., "2024")
            date: Optional date override
            
        Returns:
            Dictionary with season-filtered team and player data
        """
        data = self.get_data_as_of(date)
        
        team_data = data['team_data'][data['team_data']['season'] == season]
        player_data = data['player_data'][data['player_data']['season'] == season]
        
        return {
            'team_data': team_data,
            'player_data': player_data,
            'season': season,
            'simulation_date': data['simulation_date']
        }
    
    def get_available_seasons(self, date: Optional[datetime or str] = None) -> List[str]:
        """Get list of seasons available up to simulation date."""
        data = self.get_data_as_of(date)
        seasons = sorted(data['team_data']['season'].unique())
        return list(seasons)
    
    def get_available_teams(self, season: Optional[str] = None,
                           date: Optional[datetime or str] = None) -> List[str]:
        """Get list of teams available up to simulation date, optionally filtered by season."""
        data = self.get_team_data(date=date)
        
        if season:
            data = data[data['season'] == season]
            
        teams = sorted(data['team_name'].unique())
        return list(teams)
    
    def get_matchweek_dates(self, season: str) -> pd.DataFrame:
        """
        Get approximate matchweek boundaries for a season.
        Groups matches by week.
        
        Args:
            season: Season string
            
        Returns:
            DataFrame with matchweek, start_date, end_date, num_matches
        """
        season_data = self.get_season_data(season)['team_data']
        
        # Group by week
        season_data['week'] = (season_data['date'] - season_data['date'].min()).dt.days // 7
        
        matchweeks = season_data.groupby('week').agg({
            'date': ['min', 'max', 'count']
        }).reset_index()
        
        matchweeks.columns = ['matchweek', 'start_date', 'end_date', 'num_matches']
        matchweeks['matchweek'] = matchweeks['matchweek'] + 1  # Start from 1
        
        return matchweeks
    
    def advance_to_matchweek(self, season: str, matchweek: int) -> None:
        """
        Advance simulation date to the end of a specific matchweek.
        
        Args:
            season: Season string
            matchweek: Matchweek number (1-indexed)
        """
        matchweeks = self.get_matchweek_dates(season)
        
        if matchweek < 1 or matchweek > len(matchweeks):
            print(f"Error: Matchweek {matchweek} not found. Available: 1-{len(matchweeks)}")
            return
        
        target_date = matchweeks[matchweeks['matchweek'] == matchweek]['end_date'].iloc[0]
        self.set_simulation_date(target_date)
        
    def get_current_info(self) -> Dict:
        """Get information about current simulation state."""
        data = self.get_data_as_of()
        
        return {
            'simulation_date': self.simulation_date,
            'data_range': (self.min_date, self.max_date),
            'team_matches_available': len(data['team_data']),
            'player_matches_available': len(data['player_data']),
            'seasons_available': self.get_available_seasons(),
            'teams_available': len(self.get_available_teams())
        }
    
    def validate_no_future_data(self, df: pd.DataFrame, date_column: str = 'date') -> bool:
        """
        Validate that a DataFrame contains no data after simulation date.
        
        Args:
            df: DataFrame to validate
            date_column: Name of date column
            
        Returns:
            True if valid (no future data), False otherwise
        """
        if date_column not in df.columns:
            print(f"Warning: Column '{date_column}' not found in DataFrame")
            return False
            
        future_data = df[pd.to_datetime(df[date_column]) > self.simulation_date]
        
        if len(future_data) > 0:
            print(f"ERROR: Found {len(future_data)} records after simulation date {self.simulation_date.date()}")
            print(f"Date range in data: {df[date_column].min()} to {df[date_column].max()}")
            return False
        
        return True


def demo():
    """Demonstrate time simulation functionality."""
    # Load data
    team_df = pd.read_csv("./data/team_matches_with_rolling.csv")
    player_df = pd.read_csv("./data/player_matches_with_rolling.csv")
    
    # Initialize simulator
    sim = TimeSimulator(team_df, player_df)
    
    print("="*60)
    print("TIME SIMULATION DEMO")
    print("="*60)
    
    # Show current state
    info = sim.get_current_info()
    print(f"\n📅 Simulation Date: {info['simulation_date'].date()}")
    print(f"📊 Team Matches: {info['team_matches_available']}")
    print(f"📊 Player Matches: {info['player_matches_available']}")
    print(f"🏆 Seasons: {', '.join(map(str, info['seasons_available']))}")
    print(f"⚽ Teams: {info['teams_available']}")
    
    # Move to a specific date
    print("\n" + "-"*60)
    print("Setting simulation date to Jan 1, 2024...")
    sim.set_simulation_date("2024-01-01")
    
    # Get data as of that date
    data = sim.get_data_as_of()
    print(f"Team matches available: {len(data['team_data'])}")
    print(f"Player matches available: {len(data['player_data'])}")
    
    # Get specific team data
    print("\n" + "-"*60)
    print("Getting Manchester City data...")
    city_data = sim.get_team_data(team_name="Manchester City")
    print(f"Matches found: {len(city_data)}")
    print(f"Latest match: {city_data['date'].max().date()}")
    
    # Validate no future data
    print("\n" + "-"*60)
    print("Validating no future data leakage...")
    is_valid = sim.validate_no_future_data(city_data)
    print(f"Validation result: {'✓ PASS' if is_valid else '✗ FAIL'}")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    demo()
