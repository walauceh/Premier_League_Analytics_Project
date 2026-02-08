# Premier League Tactical & Scouting Decision Support System (2024/25 Season)

## 📊 Project Status: Complete + Improved

**Original Build**: ✅ All 10 phases complete  
**Improvements**: ✅ 4 major enhancements implemented

See [IMPROVEMENTS.md](IMPROVEMENTS.md) for details on recent enhancements.

---

## Project Description

This project is a proof-of-concept football analytics system that simulates how a professional club's analysis department would use data throughout a season to support decisions. Using Premier League data from the 2024/25 season, the system provides time-aware analysis ensuring no future information is used. The focus is on explaining performance, profiling players and teams, identifying tactical patterns, and supporting match preparation.

The primary users are football fans who want clear, visual insights with minimal jargon.

---

## 🎯 Objectives

- Provide clear, visual explanations of how teams and players perform over time
- Support player scouting through role profiling and similarity search
- Identify team playing styles and tactical patterns using data
- Diagnose strengths and weaknesses of teams in a season context
- Support opponent preparation with simple, data-backed insights
- Simulate "as of matchweek X" analysis to reflect real-world usage

---

## 📦 Project Components

### 1. Jupyter Notebooks (Analysis Pipeline)

Interactive notebooks for data processing and exploration:
- `01_data_loading.ipynb` - Load FBref + Understat data for 2024/25
- `02_feature_engineering.ipynb` - Generate rolling and per-90 features
- `03_tactical_analysis.ipynb` - Cluster teams by playing style
- `04_player_scouting.ipynb` - Player similarity and scouting reports

**See [NOTEBOOKS.md](NOTEBOOKS.md) for detailed notebook guide.**

### 2. Streamlit Dashboard (Interactive Visualization)

Multi-page dashboard with theme-aware design:
- 🏠 **Home** - Project overview and data summary
- 📈 **League Overview** - Standings, trends, team performance
- 🔍 **Team Analysis** - Deep dive into specific teams
- 👤 **Player Scouting** - Find and compare players
- 🎨 **Tactical Styles** - Team clustering and style comparison
- ⚔️ **Opponent Analysis** - Match preparation insights
- 📅 **Time Simulation** - Historical date filtering

### 3. Python Modules (Core Logic)

Reusable code in `src/` directory:
- `data_loader.py` - Data transformation and processing
- `features.py` - Feature engineering functions
- `tactical_analysis.py` - Team clustering and style analysis
- `player_scout.py` - Player similarity and profiling
- `opponent_analysis.py` - Match preparation tools
- `time_simulation.py` - Time-aware data filtering

---

## 🔍 In Scope

- **League**: English Premier League
- **Season**: 2024/25 (current season focus)
- **Data Sources**: 
  - FBref (via soccerdata library)
  - Understat (CSV exports)
- **Analysis Areas**:
  - Player scouting & profiling
  - Team tactical style analysis
  - Performance diagnosis (strengths/weaknesses, trends)
  - Opponent analysis & matchup insights
- **Deliverable**: Interactive Streamlit dashboard + Jupyter notebooks

---

## ❌ Out of Scope

- Live data ingestion
- Scoreline or betting-style predictions
- Paid APIs or proprietary data sources
- Real-time match tracking

---

## 📊 Data Approach

- **Primary Focus**: 2024/25 season data
- **Historical Context**: 2015-2024 data available for player profiling
- **Time-aware Analysis**: Only data before selected matchweek is used
- **Multiple Sources**: FBref + Understat with fallback handling
- **Rolling Metrics**: 3, 5, 10 match windows for form analysis
- **No Future Data Leakage**: Validation built into TimeSimulator class

---

## 🎯 Key Features (Dashboard Modules)

### 1. League & Team Overview
- Table vs expected performance
- Team trends over time
- Simple strengths/weaknesses summaries

### 2. Player Scouting
- Player role clusters (Forward, Midfielder, Defender)
- Radar charts with percentile rankings
- "Find similar players" tool using cosine similarity
- Detailed scouting reports

### 3. Tactical Patterns
- Team style clustering (K-means with k=5)
- PCA visualization of tactical spaces
- Comparison of how teams play
- Cluster profiles (Attacking Pressing, Defensive Deep Block, etc.)

### 4. Opponent Analysis
- Team vs team comparison
- Key danger areas and weaknesses
- Simple, human-readable tactical notes
- Recent form analysis

### 5. Time Simulation Control
- Matchweek/date selector
- Dashboard updates as if viewed at that point in the season
- Historical analysis without data leakage

---

## ✅ Success Criteria

- [x] The system works without using any future data
- [x] A non-technical football fan can understand the main insights
- [x] The dashboard clearly demonstrates scouting, tactical, and diagnostic use cases
- [x] The project can be presented as a realistic club analytics proof of concept
- [x] Dashboard works in both light and dark themes
- [x] Code is modular and well-documented
- [x] Multiple data sources with error handling

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Data Pipeline (Notebooks)
```bash
jupyter notebook
# Run notebooks in sequence: 01 → 02 → 03 → 04
```

### 3. Launch Dashboard
```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
Premier_League_Analytics_Project/
├── 01_data_loading.ipynb              # Data sourcing (FBref + Understat)
├── 02_feature_engineering.ipynb       # Feature generation
├── 03_tactical_analysis.ipynb         # Team clustering
├── 04_player_scouting.ipynb           # Player analysis
│
├── app.py                             # Streamlit dashboard main
├── pages/                             # Dashboard page modules
│   ├── league_overview.py
│   ├── team_analysis.py
│   ├── player_scouting.py
│   ├── tactical_styles.py
│   ├── opponent_analysis_page.py
│   └── time_simulation_page.py
│
├── src/                               # Core Python modules
│   ├── data_loader.py
│   ├── features.py
│   ├── tactical_analysis.py
│   ├── player_scout.py
│   ├── opponent_analysis.py
│   └── time_simulation.py
│
├── data/                              # Processed data files
│   ├── team_matches_2024.csv
│   ├── player_matches_2024.csv
│   ├── team_features_2024.csv
│   ├── player_profiles_2024.csv
│   └── ... (other processed files)
│
├── README.md                          # This file
├── NOTEBOOKS.md                       # Notebook workflow guide
├── IMPROVEMENTS.md                    # Recent enhancements
├── SETUP_GUIDE.md                     # Technical setup guide
├── QUICK_REFERENCE.md                 # User guide
├── PROJECT_SUMMARY.md                 # Complete project summary
└── Task_Checklist.md                  # Development checklist
```

---

## 📚 Documentation

- **[NOTEBOOKS.md](NOTEBOOKS.md)** - Jupyter notebook workflow and guide
- **[IMPROVEMENTS.md](IMPROVEMENTS.md)** - Recent enhancements and improvements
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Technical setup and architecture
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Common use cases and workflows
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Complete project documentation
- **[Task_Checklist.md](Task_Checklist.md)** - Development progress tracking

---

## 🛠️ Technical Stack

- **Python 3.12+**
- **Data Sources**: soccerdata (FBref), Understat CSVs
- **Data Processing**: pandas, numpy
- **Machine Learning**: scikit-learn (K-means, PCA, StandardScaler)
- **Visualization**: Plotly, Streamlit
- **Analysis**: Jupyter notebooks

---

## 🎨 Features Highlights

### Data Integration
- ✅ FBref API integration with retry logic
- ✅ Understat CSV processing
- ✅ Graceful fallback if FBref unavailable
- ✅ Cross-validation between sources

### Feature Engineering
- ✅ 65 team features (rolling, performance, tactical)
- ✅ 48 player features (per-90, cumulative, percentiles)
- ✅ Time-aware rolling windows (3, 5, 10 matches)
- ✅ Position-specific metrics for players

### Machine Learning
- ✅ K-means clustering for team styles (k=5)
- ✅ PCA visualization of tactical spaces
- ✅ Cosine similarity for player matching
- ✅ Percentile-based player ratings

### User Experience
- ✅ Theme-aware dashboard (light & dark mode)
- ✅ Interactive Plotly visualizations
- ✅ Clear non-technical explanations
- ✅ Step-by-step Jupyter notebooks

---

## 🧪 Testing

### Manual Testing Checklist
- [x] Data loading handles FBref errors gracefully
- [x] Dashboard displays 2024/25 season focus
- [x] All notebooks run without errors
- [x] Dashboard readable in light mode
- [x] Dashboard readable in dark mode
- [x] Time simulation prevents future data leakage
- [x] Player similarity returns relevant matches
- [x] Team clustering identifies distinct styles

---

## 📝 Usage Examples

### Find Similar Players
```python
from src.player_scout import PlayerScout

scout = PlayerScout(player_data)
similar = scout.find_similar_players("Erling Haaland", n=5)
print(similar)
```

### Analyze Team Tactics
```python
from src.tactical_analysis import TacticalAnalyzer

analyzer = TacticalAnalyzer(team_data)
analyzer.cluster_teams(n_clusters=5)
analyzer.visualize_clusters()
```

### Time Simulation
```python
from src.time_simulation import TimeSimulator

sim = TimeSimulator(team_data)
sim.set_simulation_date("2024-12-01")
data_as_of = sim.get_data_as_of()
print(f"Matches available: {len(data_as_of)}")
```

---

## 🤝 Contributing

This is a portfolio/proof-of-concept project. Contributions are welcome via:
- Bug reports
- Feature suggestions
- Code improvements
- Documentation enhancements

---

## 📄 License

This project is for educational and portfolio purposes. Data sources (FBref, Understat) have their own terms of use.

---

## 🙏 Acknowledgments

- **Understat** for xG and advanced match data
- **FBref** (via soccerdata) for comprehensive football statistics
- **Streamlit** for rapid dashboard development
- **scikit-learn** for machine learning tools
- **Plotly** for interactive visualizations

---

## 📧 Contact

For questions or feedback about this project, please create an issue in the repository.

---

**Last Updated**: 2024  
**Status**: ✅ Complete and Improved
