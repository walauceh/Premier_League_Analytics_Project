## 📦 Phase 1 — Data Sourcing
- [x] Identify data sources:
    - [x] FBref via soccerdata
    - [x] Understat match team dataset (CSV)
    - [x] Understat match roster dataset (CSV)
- [ ] Download / place datasets in /data/raw
- [ ] Verify columns:
    - [ ] Match ID
    - [ ] Date
    - [ ] Team name
    - [ ] Player name
- [ ] Decide season(s) to include
- [ ] Document data schema in docs/data_dictionary.md

## 🧹 Phase 2 — Data Loading & Cleaning
- [ ] Create data_loading.py / notebook
- [ ] Load FBref data using soccerdata
- [ ] Load Understat CSV datasets
- [ ] Standardize:
    - [ ] Date formats
    - [ ] Team names
    - [ ] Player names
- [ ] Handle missing values
- [ ] Filter to target league & season
- [ ] Save cleaned datasets to /data/processed:
    - [ ] matches_team.csv
    - [ ] matches_player.csv
    - [ ] schedule.csv

## 🧱 Phase 3 — Data Model & Time Simulation
- [ ] Define core tables:
    - [ ] Team-match table
    - [ ] Player-match table
    - [ ] Match schedule table
- [ ] Ensure each table includes:
    - [ ] Match ID
    - [ ] Date
    - [ ] Team / Player ID
- [ ] Implement “simulation date” filter:
    - [ ] Filter data by date < sim_date
- [ ] Add helper function:
    - [ ] get_data_as_of(date)
- [ ] Verify no future data leakage

## 📐 Phase 4 — Feature Engineering
- [ ] Team features:
    - [ ] Rolling xG (last 5 / 10 matches)
    - [ ] Rolling xGA
    - [ ] Rolling goals scored / conceded
    - [ ] Shots for / against
- [ ] Player features:
    - [ ] xG per 90
    - [ ] xA per 90
    - [ ] Shots per 90
    - [ ] Minutes played
- [ ] Trend features:
    - [ ] Moving averages
    - [ ] Form change vs previous window
- [ ] Performance gap metrics:
    - [ ] Goals − xG
    - [ ] Conceded − xGA

## 🧠 Phase 5 — Tactical & Style Modelling
- [ ] Build team style vectors:
    - [ ] Attack volume vs quality
    - [ ] Defensive vulnerability
    - [ ] Tempo / control proxies
- [ ] Normalize features
- [ ] Cluster teams (e.g. KMeans / Hierarchical)
- [ ] Label clusters with football-friendly names
- [ ] Track style changes over time

🧍 Phase 6 — Player Scouting & Similarity
- [ ] Build player profile vectors by position
- [ ] Normalize per 90 metrics
- [ ] Implement similarity search:
    - [ ] Cosine similarity
    - [ ] Euclidean distance
- [ ] Features:
    - [ ] “Find similar players to X”
    - [ ] “Find underrated profiles”

## 🎯 Phase 7 — Opponent Analysis
- [ ] Create opponent profile page:
    - [ ] Recent form (xG / xGA trends)
    - [ ] Over/underperformance indicators
    - [ ] Tactical style cluster
- [ ] Build team vs opponent comparison view
- [ ] Generate simple insights:
    - [ ] Strengths to exploit
    - [ ] Risks to avoid

## ⏱️ Phase 8 — Time Simulation / Backtesting
- [ ] Add matchweek / date selector
- [ ] Recompute:
    - [ ] Rolling features
    - [ ] Team clusters
    - [ ] Player profiles
- [ ] Show how insights evolve over time
- [ ] Validate realism of outputs

## 🖥️ Phase 9 — Dashboard / UI
- [ ] Choose framework (Streamlit / Power BI / Tableau)
- [ ] Build pages:
    - [ ] League overview
    - [ ] Team analysis
    - [ ] Player scouting
    - [ ] Opponent analysis
- [ ] Add charts:
    - [ ] Trend lines
    - [ ] Radar charts
    - [ ] Bar charts
    - [ ] Filterable tables
- [ ] Add short explanations for each view (fan-friendly)