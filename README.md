# ⚽ Premier League Tactical & Scouting Decision Support System

**A comprehensive analytics platform for the 2023/24 Premier League season**

This project simulates how a professional football club's analysis department uses data to support tactical decisions, player scouting, and match preparation. Using historical Premier League data from the 2023/24 season, the system provides clear, visual insights with position-specific analysis, defensive metrics integration, and tactical style profiling.

Built for football fans and analysts who want data-backed insights without overwhelming technical jargon.

---

## 📋 Table of Contents
- [Project Overview](#-project-overview)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [Key Features](#-key-features)
- [Tech Stack](#️-tech-stack)
- [Data Approach](#-data-approach)
- [Analysis Modules](#-analysis-modules)
- [Position-Specific Analysis](#-position-specific-analysis)
- [Success Criteria](#-success-criteria)
- [Notes & Limitations](#-notes--limitations)

---

## 🎯 Project Overview

### Objectives
- Provide clear, visual explanations of team and player performance over time
- Support player scouting through position-specific profiling and similarity search
- Identify team playing styles and tactical patterns using clustering
- Diagnose strengths and weaknesses within a season context
- Support opponent preparation with data-backed tactical insights
- Simulate "as of matchweek X" analysis to reflect real-world usage

### Scope
- **League**: English Premier League
- **Season**: 2023/24 (380 matches, 11,384 player-match records)
- **Data Source**: Understat CSV exports (free, public data)
- **Deliverable**: Interactive Streamlit dashboard with 7 analysis modules
- **Analysis Areas**: Player scouting, tactical styles, performance diagnosis, opponent analysis, time-aware simulation

### Out of Scope
- Live data ingestion or real-time match tracking
- Scoreline predictions or betting-style forecasting
- Paid APIs or proprietary data sources
- Multi-league or multi-season comparative analysis

---

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Jupyter Notebook
- Source data files (included in repository):
  - `understat_matches_team.csv` (team-level match data)
  - `understat_matches_roster.csv` (player-level match data)

### Setup Steps

```bash
# 1. Clone repository
git clone <your-repo-url>
cd Premier_League_Analytics_Project

# 2. Install dependencies
pip install pandas numpy scikit-learn plotly streamlit

# 3. Run Jupyter notebooks to generate processed data
jupyter notebook 01_data_loading.ipynb
# Run notebooks in sequence: 01 → 02 → 03 → 04
# This generates CSV files in the data/ directory

# 4. Launch dashboard
streamlit run app.py
```

Dashboard opens at `http://localhost:8501`

### Data Files

**Source Files** (included in repo, ~15MB total):
- `understat_matches_team.csv` - Team match statistics (380 matches)
- `understat_matches_roster.csv` - Player match statistics (11,384 records)

**Generated Files** (excluded from git, created by notebooks):
- `data/team_matches_2023.csv` - Processed team data
- `data/player_matches_2023.csv` - Processed player data
- `data/team_features_2023.csv` - Engineered team features
- `data/player_features_2023.csv` - Engineered player features
- `data/player_profiles_2023.csv` - Basic player profiles
- `data/player_profiles_enhanced_2023.csv` - Profiles with percentiles
- `data/team_tactical_styles_2023.csv` - Tactical clustering results

---

## 📁 Project Structure

```
├── app.py                          # Main Streamlit application
├── pages/                          # Dashboard pages
│   ├── league_overview.py         # League standings & trends
│   ├── team_analysis.py           # Team deep dives
│   ├── player_scouting.py         # Player search & reports
│   ├── tactical_styles.py         # Team clustering
│   ├── opponent_analysis_page.py  # Match preparation
│   └── time_simulation_page.py    # Historical analysis
├── src/                            # Core modules
│   ├── player_scout.py            # Player similarity & profiling
│   ├── defensive_stats.py         # GK/Defender metrics
│   ├── opponent_analysis.py       # Match prep tools
│   └── time_simulation.py         # Time-aware filtering
├── 01_data_loading.ipynb          # Load Understat data
├── 02_feature_engineering.ipynb   # Generate features
├── 03_tactical_analysis.ipynb     # Team clustering
├── 04_player_scouting.ipynb       # Player analysis
├── data/                           # Generated CSVs
└── understat_matches_*.csv        # Source data
```

---

## 🛠️ Tech Stack

**Languages & Libraries:**
- Python 3.12
- pandas, numpy (data processing)
- scikit-learn (clustering, similarity)
- plotly (visualizations)
- streamlit (dashboard)

**Data:**
- Understat CSV exports (2023/24 season)
- 380 matches, 11,384 player-match records
- Advanced metrics: xG, xGA, xGChain, xGBuildup, PPDA

**Analysis:**
- K-means clustering for tactical styles
- Cosine similarity for player matching
- Rolling averages (L3/L5/L10)
- Position-specific feature engineering

---

## ✨ Key Features

### 📊 Dashboard Modules (7 Pages)
1. **Home** - Dataset overview, quick stats, navigation hub
2. **League Overview** - Standings, form tables, top performers by metric
3. **Team Analysis** - xG trends, shot quality, rolling form analysis
4. **Player Scouting** - Position-aware search, comprehensive player reports, similarity matching
5. **Tactical Styles** - K-means clustering, style profiles (possession vs counter-attacking vs pressing)
6. **Opponent Analysis** - Head-to-head stats, tactical matchups, danger area identification
7. **Time Simulation** - Historical "as of matchweek X" analysis (simulates real-world analyst workflow)

---

## 📊 Analysis Modules

### 1. Player Scouting (Enhanced)
**3 Sub-tabs**: Find Players | Player Report | Similar Players

**Find Players Tab**:
- Categorized metric search (Attacking, Creativity, Build-up Play, Discipline, Overall)
- Position filters (Forward, Midfielder, Defender)
- Minimum minutes threshold
- Top 20 leaderboards

**Player Report Tab** (Comprehensive Deep Dive):
- **Goalkeepers**: 
  - Shot stopping analysis (save %, saves estimate, shots faced)
  - Goals prevented vs xGA with interactive gauge
  - Save percentage gauge (0-100% color-coded)
  - Clean sheet tracking and consistency metrics
  
- **Defenders**:
  - Comprehensive defensive metrics (clean sheets, goals conceded/90, xGA/90)
  - Defensive performance gauge (actual vs expected, color-coded)
  - Pressing stats (PPDA allowed, shots against/90)
  - Build-up play contribution (xGBuildup, xGChain)
  - Discipline tracking (yellow/red cards)
  
- **Midfielders**:
  - Creative output (assists/90, xA/90, key passes/90)
  - Goal threat (goals/90, xG/90, shots/90)
  - Defensive contribution (clean sheets, goals conceded if available)
  - **Radar chart**: Attack vs creativity balance (6-axis comparison)
  
- **Forwards**:
  - Scoring efficiency (goals/90, xG/90, shot efficiency)
  - **Bar chart**: Goals vs xG total comparison
  - Playmaking metrics (assists/90, key passes/90, xGChain)

- **All Positions**:
  - Enhanced percentile rankings with emoji indicators (🟢🟡🔴)
  - Overall summary (matches, minutes, goal involvement)
  - Position-specific context explanations

**Similar Players Tab**:
- Position-aware similarity search using cosine distance
- Position-specific features for comparison:
  - **Goalkeepers**: save_percentage, goals_prevented_per90, clean_sheet_rate
  - **Defenders**: clean_sheet_rate, defensive_performance_per90, xGBuildup_per90
  - **Midfielders**: assists_per90, key_passes_per90, xA_per90, goals_per90
  - **Forwards**: goals_per90, xG_per90, shots_per90, assists_per90
- Searchable player selection (type to filter)
- Displays top 5 most similar players with relevant metrics

### 2. Tactical Styles
- K-means clustering (3 clusters: possession-based, counter-attacking, pressing)
- PCA visualization of team styles
- Cluster profiles with average metrics
- Team-by-team style assignment

### 3. Team Analysis
- xG trends over time (L3/L5/L10 rolling averages)
- Shot quality analysis
- Form analysis with expected vs actual performance
- Attack/defense balance

### 4. Opponent Analysis
- Head-to-head comparison
- Tactical matchup insights
- Key danger areas identification
- Strengths/weaknesses breakdown

### 5. Time Simulation
- "As of matchweek X" historical analysis
- No future data leakage
- Simulates real-world analyst workflow

---

## 🎯 Position-Specific Analysis

### Implementation Strategy
Each position uses different metrics for similarity calculations and performance evaluation:

**Forwards**:
- Primary: Goals/90, xG/90, shots/90
- Secondary: Assists/90, key passes/90, xGChain/90
- Visualizations: Goals vs xG bar chart

**Midfielders**:
- Primary: Assists/90, xA/90, key passes/90, xGChain/90
- Secondary: Goals/90, xG/90, xGBuildup/90
- Visualizations: 6-axis radar chart (attack vs creativity balance)
- Defensive contribution shown if available

**Defenders**:
- Primary: Clean sheet rate, goals conceded/90, defensive performance/90
- Secondary: xGBuildup/90, xGChain/90, PPDA allowed, discipline
- Visualizations: Defensive performance gauge (-15 to +15 range)

**Goalkeepers**:
- Primary: Save percentage, goals prevented/90, clean sheet rate
- Secondary: Goals conceded/90, xGA/90
- Visualizations: Goals prevented gauge, save percentage gauge

### Defensive Metrics Integration
Defensive statistics are **auto-calculated on app load** for all goalkeepers, defenders, and midfielders:
- Calculated using `DefensiveStatsCalculator` from team-level defensive data
- Metrics derived from team xGA when player was on field
- Stored as DataFrame columns for fast access
- No on-demand calculation (pre-computed for performance)

---

## 📈 Advanced Metrics

### Core Metrics
- **xG/xGA**: Expected goals for/against (shot quality measurement)
- **xGChain**: Total xG of possessions a player is involved in
- **xGBuildup**: xGChain excluding shots and assists (pure build-up contribution)
- **PPDA**: Passes per defensive action (pressing intensity - lower = more intense)
- **Shot Quality**: xG per shot (chance quality)
- **Deep Passes**: Passes into final third (progression metric)

### Derived Metrics
- **Save Percentage**: (Shots on target - goals) / shots on target × 100
- **Goals Prevented**: Expected goals against - actual goals conceded (GK performance)
- **Defensive Performance**: Actual goals conceded - xGA (team/player defensive quality)
- **Clean Sheet Rate**: Percentage of matches without conceding
- **Shot Efficiency**: Goals / shots (conversion rate)
- **Rolling Averages**: L3/L5/L10 match windows for form analysis

### Percentile Rankings
- Position-specific percentile calculations (player ranked vs positional peers)
- 0-100 scale with color-coding (🟢 ≥80th, 🟡 50-79th, 🔴 <50th)
- Displayed in bar charts and emoji-coded summaries

---

## 🛠️ Data Approach

### Data Pipeline
1. **Raw Data**: Understat match CSV exports (2 files: team-level, player-roster)
2. **Notebook 01**: Data loading, basic cleaning, HTML entity fixes
3. **Notebook 02**: Feature engineering, per90 calculations, position mapping
4. **Notebook 03**: Tactical clustering, team style profiles
5. **Notebook 04**: Player percentiles, scouting features, enhanced profiles
6. **Dashboard**: Defensive stats auto-calculation, live analysis

### Data Quality Enhancements
- **HTML Entity Decoding**: Fixed `&#039;` → `'` (e.g., "Amari'i Bell")
- **Position Normalization**: Corrected GK mapping (was "Midfielder", now "Goalkeeper")
- **Defensive Stats**: Auto-calculated for 32 goalkeepers, 152 defenders, 189 midfielders
- **Time-Aware**: All analysis respects match dates (no future data leakage)

### Data Volume
- **Matches**: 380 Premier League matches (full 2023/24 season)
- **Player Records**: 11,384 player-match observations
- **Teams**: 20 Premier League clubs
- **Players**: 435 unique players (after 900+ minute filter)
- **Position Distribution**: 62 Forwards, 189 Midfielders, 152 Defenders, 32 Goalkeepers

---

## ✅ Success Criteria

### Functional Requirements
✅ **No Future Data Leakage**: Time simulation ensures only historical data is used  
✅ **Non-Technical Accessibility**: Dashboard designed for fans, minimal jargon with tooltips  
✅ **Realistic Use Cases**: Demonstrates scouting, tactical analysis, and match preparation workflows  
✅ **Position-Specific Logic**: Different metrics and visualizations per position  
✅ **Defensive Integration**: GK/Defender/Midfielder defensive stats fully integrated  

### Technical Requirements
✅ **Modular Architecture**: Reusable `src/` modules for notebooks and dashboard  
✅ **Performance**: Data pre-calculated at load time, fast interactive filtering  
✅ **Data Quality**: HTML entities decoded, position mapping corrected, validation checks  
✅ **Visualization Quality**: Plotly interactive charts, gauges, radar charts, bar charts  
✅ **Code Maintainability**: Single source of truth, DRY principles, clear separation of concerns  

### User Experience
✅ **Clear Navigation**: 7 pages with intuitive icons and descriptions  
✅ **Visual Feedback**: Color-coded metrics, emoji indicators, progress indicators  
✅ **Comprehensive Reports**: Deep-dive player analysis with 4+ sections per position  
✅ **Search UX**: Searchable dropdowns (type to filter player names)  
✅ **Contextual Help**: Tooltips, captions, metric explanations  

---

## 📝 Notes & Limitations

### Data Source
- **Provider**: Understat (free CSV exports)
- **Coverage**: 2023/24 Premier League season only
- **Update Frequency**: Static dataset (no live updates)
- **Metrics Available**: xG, xGA, xGChain, xGBuildup, shots, key passes, PPDA, deep passes

### Data Limitations
- **Defensive Stats**: Derived from team-level data (not individual tracking data)
  - Save percentage estimated as (shots on target - goals) / shots on target
  - Individual tackles, clearances, blocks not available
  - Goalkeeper stats approximated from team defensive performance
  
- **Position Data**: 
  - Players mapped to primary position (no multi-position handling)
  - Position changes mid-season not tracked
  
- **Context Missing**:
  - No injury data, squad rotation reasoning
  - No match context (home/away not fully utilized)
  - No set-piece specific analysis

### Technical Constraints
- **Python 3.12**: Requires compatible package versions
- **Memory**: Full dataset loads into memory (~15MB)
- **Processing Time**: Defensive stats calculation adds ~5-10 seconds to load time

### Known Issues
- **Goalkeeper Data**: Limited availability (Understat focuses on outfield events)
- **Defensive Approximations**: Team-level defensive metrics may not fully represent individual contribution
- **Minimum Minutes Filter**: 900+ minutes excludes rotation players and new signings

### Future Enhancements (Out of Current Scope)
- Multi-season comparative analysis
- Advanced set-piece analysis
- Expected assists (xA) breakdowns
- Player injury/availability tracking
- Multi-league support

---

## 🏗️ Built By

This project demonstrates a realistic football analytics workflow using free, public data. It simulates the type of analysis performed by professional club analytics departments while remaining accessible to football fans and aspiring analysts.

**Primary Use Cases**: Player scouting, tactical preparation, performance diagnosis, opponent analysis

**Target Users**: Football fans, amateur analysts, students learning sports analytics
