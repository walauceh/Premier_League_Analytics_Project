# Premier League Tactical & Scouting Decision Support System (2024/25 Season)

## Project Description
This project is a proof-of-concept football analytics system that simulates how a professional club’s analysis department would use data throughout a season to support decisions. Using historical Premier League data from the 2024/25 season, the system will treat the data as if it were arriving week by week, ensuring no future information is used. The focus is on explaining performance, profiling players and teams, identifying tactical patterns, and supporting match preparation — not predicting scorelines.

The primary users are football fans who want clear, visual insights with minimal jargon.

## Objectives
- Provide clear, visual explanations of how teams and players perform over time
- Support player scouting through role profiling and similarity search
- Identify team playing styles and tactical patterns using data
- Diagnose strengths and weaknesses of teams in a season context
- Support opponent preparation with simple, data-backed insights
- Simulate “as of matchweek X” analysis to reflect real-world usage

## In Scope
- League: English Premier League
- Season: 2024/25 (full season, used in time-aware simulation)
- Data: Free, public sources (via Python libraries such as soccerdata)
- Analysis areas:
    - Player scouting & profiling
    - Team tactical style analysis
    - Performance diagnosis (strengths/weaknesses, trends)
    - Opponent analysis & matchup insights
- Deliverable: Interactive Python dashboard (Streamlit)

## Out of Scope
- Live data ingestion
- Scoreline or betting-style predictions
- Paid APIs or proprietary data sources
- Real-time match tracking

## Data Approach
- Use historical match, team, and player data with match dates
- All analysis will be time-aware (only data before a selected matchweek is used)
- Rolling and season-to-date metrics will be computed to simulate real usage
- No future data leakage

## Key Features (Dashboard Modules)
1. League & Team Overview
    - Table vs expected performance
    - Team trends over time
    - Simple strengths/weaknesses summaries
2. Player Scouting
    - Player role clusters
    - Radar charts
    - “Find similar players” tool
3. Tactical Patterns
    - Team style clustering and visual maps
    - Comparison of how teams play
4. Opponent Analysis
    - Team vs team comparison
    - Key danger areas and weaknesses
    - Simple, human-readable tactical notes
5. Time Simulation Control
    - Matchweek/date selector
    - Dashboard updates as if viewed at that point in the season

## Success Criteria
- The system works without using any future data
- A non-technical football fan can understand the main insights
- The dashboard clearly demonstrates scouting, tactical, and diagnostic use cases
- The project can be presented as a realistic club analytics proof of concept