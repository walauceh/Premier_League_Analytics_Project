# Premier League Tactical & Scouting Decision Support System

## 🎯 Project Overview

A comprehensive football analytics platform that simulates how professional club analysis departments use data throughout a season. Built using Premier League historical data (2015-2024), this system provides tactical insights, player scouting tools, and opponent analysis with strict time-aware data handling to prevent future data leakage.

**Dashboard Live:** http://localhost:8501

## ✨ Key Features

### 📈 League Overview
- Season standings and league tables
- Performance vs expectation (actual vs xG)
- Attack vs defense profiling
- Top performers and overperformers

### 🔍 Team Analysis
- Comprehensive team performance metrics
- Form trends and rolling averages
- Goals vs xG analysis
- Recent match history
- Home/away splits
- Attack and defense breakdowns

### 👤 Player Scouting
- Player search by metrics (goals/90, assists/90, xG/90, etc.)
- Detailed player reports with percentile rankings
- Similar player finder using cosine similarity
- Position-based comparisons
- Performance vs expectation analysis

### 🎨 Tactical Styles
- Team clustering by playing style (K-means + PCA)
- Visual style maps (2D PCA projection)
- Style profile comparisons
- Similar team identification
- Radar charts for tactical characteristics

### ⚔️ Opponent Analysis
- Detailed opponent profiling
- Strengths and weaknesses identification
- Tactical game plan generator
- Key matchup analysis
- Home/away performance splits
- Match preparation insights

### 📅 Time Simulation
- Historical date selector
- No future data leakage validation
- Matchweek-based navigation
- Data availability timeline
- Realistic backtesting framework

## 🏗️ Architecture

```
/
├── app.py                          # Main Streamlit application
├── data/                           # Processed datasets
│   ├── team_features_complete.csv
│   ├── player_features_complete.csv
│   ├── team_tactical_styles.csv
│   └── player_profiles.csv
├── src/                            # Core modules
│   ├── data_loader.py             # Data transformation
│   ├── time_simulation.py         # Time-aware filtering
│   ├── features.py                # Feature engineering
│   ├── tactical_analysis.py      # Style clustering
│   ├── player_scout.py            # Player similarity
│   └── opponent_analysis.py      # Match preparation
├── pages/                          # Dashboard pages
│   ├── league_overview.py
│   ├── team_analysis.py
│   ├── player_scouting.py
│   ├── tactical_styles.py
│   ├── opponent_analysis_page.py
│   └── time_simulation_page.py
├── data_download.ipynb            # Data acquisition notebook
├── understat_matches_team.csv     # Raw match data
└── understat_matches_roster.csv   # Raw player data
```

## 🚀 Setup Instructions

### Prerequisites
- Python 3.12+
- pip package manager

### Installation

1. **Install required packages:**
```powershell
pip install pandas numpy scikit-learn streamlit plotly
```

2. **Process the data:**
```powershell
python src\data_loader.py
python src\features.py
python src\tactical_analysis.py
python src\player_scout.py
```

3. **Launch the dashboard:**
```powershell
streamlit run app.py
```

4. **Access the dashboard:**
Open your browser to http://localhost:8501

## 📊 Data Pipeline

### 1. Data Loading (`data_loader.py`)
- Transforms match-level data to team-match level (home/away perspectives)
- Joins player rosters with match information
- Calculates basic rolling averages (5-match windows)
- Creates derived metrics (goal difference, result, points)
- **Output:** `team_matches_with_rolling.csv`, `player_matches_with_rolling.csv`

### 2. Feature Engineering (`features.py`)
- Team features: form metrics, performance vs expectation, style indicators
- Player features: per 90 metrics, efficiency, role indicators
- Season aggregates and cumulative statistics
- **Output:** `team_features_complete.csv` (65 features), `player_features_complete.csv` (48 features)

### 3. Tactical Analysis (`tactical_analysis.py`)
- Creates team style vectors from recent performance
- K-means clustering (5 clusters) with PCA visualization
- Automatic cluster labeling based on characteristics
- **Output:** `team_tactical_styles.csv`

### 4. Player Profiling (`player_scout.py`)
- Aggregates player statistics (minimum 450 minutes)
- Per 90 normalizations for fair comparison
- Similarity search using cosine similarity
- **Output:** `player_profiles.csv`

## 🔍 Key Concepts

### Expected Goals (xG)
Measures the quality of scoring chances. Values near 1.0 indicate high-quality chances.
- **xG > Actual Goals**: Underperforming (poor finishing)
- **xG < Actual Goals**: Overperforming (clinical finishing or luck)

### PPDA (Passes Allowed Per Defensive Action)
Measures defensive pressing intensity:
- **Low PPDA (<8)**: High press, aggressive
- **High PPDA (>12)**: Deep block, passive

### Rolling Averages
Statistics averaged over last N matches (typically 5 or 10) to show recent form rather than full season performance.

### Per 90 Metrics
All statistics normalized per 90 minutes of play, allowing fair comparison between players with different playing time.

## 🎯 Use Cases

1. **Match Preparation**
   - Analyze upcoming opponent's recent form
   - Identify tactical weaknesses to exploit
   - Generate data-backed game plan recommendations

2. **Player Recruitment**
   - Find players similar to your star performer
   - Identify undervalued players in specific positions
   - Compare candidates side-by-side

3. **Performance Analysis**
   - Track team form trends over time
   - Identify over/underperformance vs expectations
   - Understand tactical identity and playing style

4. **Historical Analysis**
   - Use time simulation to analyze past seasons
   - Backtest tactical approaches
   - Validate models without data leakage

## 📈 Technical Highlights

- **Time-Aware Architecture**: All analysis respects temporal ordering
- **No Data Leakage**: Strict filtering ensures no future information used
- **Scalable Processing**: Modular design allows easy extension
- **Interactive Visualization**: Plotly charts for exploration
- **ML-Based Clustering**: KMeans + PCA for tactical style identification
- **Similarity Search**: Cosine similarity in standardized feature space

## 🎨 Technologies Used

- **Python 3.12**: Core language
- **Pandas**: Data manipulation
- **NumPy**: Numerical operations
- **Scikit-learn**: Clustering, PCA, similarity metrics
- **Streamlit**: Interactive dashboard
- **Plotly**: Interactive visualizations

## 📝 Data Sources

- **Understat**: Match-level team and player data (2015-2024)
  - Match results, goals, xG, xGA
  - Player appearances, goals, assists, xG, xA
  - Shots, key passes, defensive actions

## 🚧 Future Enhancements

- [ ] Add xG timeline charts for individual matches
- [ ] Implement player form prediction
- [ ] Add head-to-head history visualization
- [ ] Include set-piece analysis
- [ ] Add injury and suspension tracking
- [ ] Integrate live data APIs
- [ ] Export reports to PDF
- [ ] Add team composition analysis
- [ ] Implement passing network visualization

## 📄 License

This project is for educational and demonstration purposes.

## 🙏 Acknowledgments

- Data from Understat.com
- Built as a proof-of-concept for football analytics

---

**Built with ⚽ by Python | Streamlit | Pandas | Scikit-learn**
