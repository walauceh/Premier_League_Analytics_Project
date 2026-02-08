# Premier League Analytics - Notebook Guide

## 📚 Notebook Overview

This project uses Jupyter notebooks for data processing and analysis, with Python modules for reusable components and the Streamlit dashboard for visualization.

### Notebook Workflow

The analysis pipeline consists of 4 main notebooks that should be run in sequence:

```
01_data_loading.ipynb
    ↓
02_feature_engineering.ipynb
    ↓
03_tactical_analysis.ipynb
    ↓
04_player_scouting.ipynb
```

## 🗂️ Notebook Descriptions

### 01_data_loading.ipynb
**Purpose**: Load and transform raw data from multiple sources

**What it does**:
- Loads FBref data via soccerdata library (schedule, team stats, player stats)
- Loads Understat CSV files (match xG data, player rosters)
- Focuses on 2024/25 season data
- Transforms match data from wide format to team perspective (long format)
- Processes player-match records with match metadata
- Loads historical player data for context

**Outputs**:
- `data/team_matches_2024.csv` - Team-match records for 2024/25
- `data/player_matches_2024.csv` - Player-match records for 2024/25
- `data/player_matches_historical.csv` - Historical player data
- `data/fbref_schedule.csv` - FBref match schedule (if available)
- `data/fbref_team_stats.csv` - FBref team statistics (if available)
- `data/fbref_player_stats.csv` - FBref player statistics (if available)

**Run time**: ~1-2 minutes (depends on FBref API response time)

---

### 02_feature_engineering.ipynb
**Purpose**: Generate advanced features and performance metrics

**What it does**:
- Creates rolling form features (3, 5, 10 match windows)
- Calculates team performance metrics (xG trends, shot quality, conversion rate, pressing intensity)
- Computes player per-90 statistics for fair comparison
- Generates cumulative season stats
- Calculates season averages for players
- Aggregates season-level player profiles

**Outputs**:
- `data/team_features_2024.csv` - Team features with rolling metrics
- `data/player_features_2024.csv` - Player match-level features
- `data/player_season_stats_2024.csv` - Aggregated player season stats
- `data/player_profiles_2024.csv` - Qualified players (≥450 minutes)

**Dependencies**: Requires outputs from `01_data_loading.ipynb`

**Run time**: ~30-60 seconds

---

### 03_tactical_analysis.ipynb
**Purpose**: Analyze team playing styles and cluster similar teams

**What it does**:
- Creates team style vectors from tactical metrics
- Applies K-means clustering (k=5) to group teams by playing style
- Generates cluster labels (e.g., "Attacking Pressing", "Defensive Deep Block")
- Analyzes cluster characteristics
- Visualizes clusters using PCA (2D projection)
- Creates radar charts for team comparisons
- Identifies tactical profiles for each cluster

**Outputs**:
- `data/team_tactical_styles_2024.csv` - Teams with cluster assignments
- `data/cluster_profiles_2024.csv` - Cluster centroids and characteristics
- Interactive visualizations (PCA scatter plot, radar charts)

**Dependencies**: Requires `data/team_features_2024.csv`

**Run time**: ~20-30 seconds

---

### 04_player_scouting.ipynb
**Purpose**: Player similarity analysis and scouting reports

**What it does**:
- Creates player feature vectors for comparison
- Groups players by position (Forward, Midfielder, Defender)
- Calculates cosine similarity to find similar players
- Computes percentile rankings within position groups
- Generates overall ratings based on position-specific metrics
- Creates detailed scouting reports
- Visualizes player comparisons (scatter plots, radar charts)
- Generates position-specific leaderboards

**Outputs**:
- `data/player_profiles_enhanced_2024.csv` - Player profiles with percentiles and ratings
- `data/leaderboard_forward_2024.csv` - Top 20 forwards
- `data/leaderboard_midfielder_2024.csv` - Top 20 midfielders
- `data/leaderboard_defender_2024.csv` - Top 20 defenders
- Interactive visualizations (scatter plots, radar charts)

**Dependencies**: Requires `data/player_profiles_2024.csv`

**Run time**: ~30-45 seconds

---

## 🚀 Quick Start

### Option 1: Run All Notebooks
```bash
# From project root
jupyter notebook
```
Then run notebooks 01-04 in sequence.

### Option 2: Run Individual Notebooks
Open VS Code and use the Jupyter extension to run cells interactively.

### Option 3: Convert to Script
```bash
# Convert notebook to Python script
jupyter nbconvert --to script 01_data_loading.ipynb
python 01_data_loading.py
```

## 📊 Data Flow Diagram

```
Understat CSV + FBref API
         ↓
    [01_data_loading]
         ↓
    Raw Match Data (Team & Player)
         ↓
  [02_feature_engineering]
         ↓
    Features (Rolling, Per90, Cumulative)
         ↓
         ├──→ [03_tactical_analysis]
         │         ↓
         │    Team Clusters & Styles
         │
         └──→ [04_player_scouting]
                   ↓
              Player Profiles & Similarity
```

## 🎯 Key Features Generated

### Team Features (65 metrics)
- **Form Features**: ppg_L3, ppg_L5, ppg_L10, win_rate_L3/5/10
- **Attacking**: goals_for_L3/5/10, xG_L3/5/10, shots_L3/5/10
- **Defensive**: goals_against_L3/5/10, xGA_L3/5/10, shots_against_L3/5/10
- **Derived**: xG_diff, shot_quality, conversion_rate, pressing_intensity

### Player Features (48 metrics)
- **Per 90 Stats**: goals_per90, assists_per90, xG_per90, xA_per90
- **Cumulative**: goals_cumsum, assists_cumsum, minutes_cumsum
- **Season Averages**: goals_season_avg, xG_season_avg, etc.
- **Percentile Ranks**: All metrics ranked within position groups
- **Overall Rating**: Position-specific weighted average

## 🔧 Troubleshooting

### FBref Connection Issues
If FBref data loading fails:
1. Check internet connection
2. Try again later (API may be rate-limited)
3. Analysis will proceed with Understat data only

### Missing Data Files
If a notebook fails:
```python
# Check required files exist
import os
print(os.listdir('data/'))
```

### Memory Issues
For large datasets:
```python
# Use chunking in data loading
chunks = pd.read_csv('file.csv', chunksize=10000)
df = pd.concat([chunk for chunk in chunks])
```

## 📝 Season Focus: 2024/25

All analyses focus on the **2024/25 Premier League season** as the current season. Historical player data (2015-2024) is available for context but the primary analysis concentrates on 2024/25.

### Why 2024/25?
- Reflects current team form and tactics
- Player statistics are most relevant for current decisions
- Historical data used only for player profiling context
- Avoids data leakage from future seasons

## 🔄 Updating Data

To refresh with new matchweek data:

1. Update Understat CSVs or re-download from API
2. Re-run `01_data_loading.ipynb`
3. Re-run subsequent notebooks (02-04)
4. Dashboard will automatically reflect new data

## 💡 Tips

- **Run cells sequentially**: Don't skip cells within a notebook
- **Check cell outputs**: Verify data shapes and summary statistics
- **Interactive visualizations**: Plotly charts are interactive (zoom, hover, pan)
- **Save intermediate results**: Each notebook saves outputs to `data/`
- **Clear output before commit**: Keep notebooks clean in version control

## 🎓 Learning Resources

- **Understat Data**: https://understat.com/
- **FBref**: https://fbref.com/en/comps/9/Premier-League-Stats
- **soccerdata Library**: https://github.com/probberechts/soccerdata
- **Scikit-learn**: https://scikit-learn.org/
- **Plotly**: https://plotly.com/python/

## 🆘 Support

For issues or questions:
1. Check notebook cell outputs for error messages
2. Review data file existence in `data/` folder
3. Ensure all dependencies are installed (`pip install -r requirements.txt`)
4. Check README.md for overall project setup

---

**Next Steps**: After running all notebooks, launch the Streamlit dashboard:
```bash
streamlit run app.py
```
