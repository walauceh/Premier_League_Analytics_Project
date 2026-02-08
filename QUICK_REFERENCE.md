# Premier League Analytics - Quick Reference Guide

## 🚀 Getting Started in 30 Seconds

1. **Launch the dashboard:**
   ```bash
   streamlit run app.py
   ```

2. **Open your browser to:** http://localhost:8501

3. **Start exploring!**

---

## 📖 Common Use Cases

### Use Case 1: Prepare for an Upcoming Match

**Goal:** Analyze Liverpool as your next opponent

**Steps:**
1. Go to **⚔️ Opponent Analysis**
2. Select "Liverpool" as opponent
3. Set analysis to last 10 matches
4. Review:
   - Form (PPG, W-D-L record)
   - Attack metrics (goals/game, xG, shot accuracy)
   - Defense metrics (goals conceded, clean sheets)
   - Strengths & Weaknesses
5. Use **Game Plan Generator** tab:
   - Select your team
   - Select Liverpool as opponent
   - Click "Generate Game Plan"
   - Review tactical recommendations

**What you'll learn:**
- Is Liverpool in good form or struggling?
- Do they score a lot but also concede?
- Are they high-pressing or sitting deep?
- What are their main weaknesses to exploit?

---

### Use Case 2: Scout for a New Striker

**Goal:** Find a striker similar to Harry Kane

**Steps:**
1. Go to **👤 Player Scouting**
2. Click the **"Similar Players"** tab
3. Select "Harry Kane" from dropdown
4. Adjust number of similar players (default: 5)
5. Review similar players with:
   - Similarity score (higher = more similar)
   - Goals/90, assists/90, xG/90
   - Current team and minutes played

**What you'll learn:**
- Who plays in a similar style to Harry Kane?
- Are there cheaper alternatives in lower teams?
- What are their production rates?

---

### Use Case 3: Understand Your Team's Playing Style

**Goal:** See how Manchester City's style compares to others

**Steps:**
1. Go to **🎨 Tactical Styles**
2. Find Manchester City in the cluster visualization
3. Select their style cluster from dropdown
4. Review average characteristics:
   - xG/game (attack volume)
   - Pressing intensity
   - Shot quality
5. Check "Similar Teams" section

**What you'll learn:**
- What tactical style cluster does your team belong to?
- Who plays similarly?
- Are you an attacking, defensive, or balanced team?

---

### Use Case 4: Analyze Team Performance Over Time

**Goal:** Check how Arsenal has performed recently

**Steps:**
1. Go to **🔍 Team Analysis**
2. Select "Arsenal" from dropdown
3. Adjust "Last N matches" slider (try 10)
4. Review:
   - Key metrics (PPG, wins, goals/game)
   - Form timeline (points rolling average)
   - Goals vs xG chart
   - Recent matches table with opponents

**What you'll learn:**
- Is the team's form improving or declining?
- Are they scoring more than expected (xG)?
- What's their recent record?

---

### Use Case 5: Find Top Players in a Position

**Goal:** Who are the best midfielders for assists?

**Steps:**
1. Go to **👤 Player Scouting**
2. Stay on **"Find Players"** tab
3. Select metric: "assists_per90"
4. Select position: "MID"
5. Set minimum minutes: 900 (10+ full matches)
6. Review bar chart and table of top 20

**What you'll learn:**
- Who are the most creative midfielders?
- What teams do they play for?
- How many minutes have they played?

---

### Use Case 6: Compare League Standings to Expected Performance

**Goal:** Which teams are overperforming or lucky?

**Steps:**
1. Go to **📈 League Overview**
2. Select current or recent season
3. View the league table
4. Check the "Points vs Expected Points" chart
   - Teams above the diagonal line = overperforming
   - Teams below the line = underperforming
5. Scroll to "Overperformers" section

**What you'll learn:**
- Which teams are getting more points than their performance suggests?
- Which teams are creating good chances but not winning?
- Who might regress or improve?

---

### Use Case 7: View Historical Data (Backtesting)

**Goal:** Analyze data as of January 1, 2023

**Steps:**
1. Go to **📅 Time Simulation**
2. Select season: "2023"
3. Use slider to select matchweek, OR
4. Use date picker to select "2023-01-01"
5. Click "Set Date"
6. Review data available as of that date
7. Click "Validate" to ensure no future data leakage

**What you'll learn:**
- What did the standings look like mid-season?
- Who were the top scorers at that point?
- Test your analysis as if you were there

---

## 🎯 Pro Tips

### For Team Analysis:
- Use last 5-10 matches for recent form
- Compare actual goals vs xG to spot luck factors
- Check home vs away splits for venue bias

### For Player Scouting:
- Set minimum minutes (900+) to filter out small samples
- Use per90 metrics for fair comparison
- Look at xG/xA to assess quality, not just results

### For Opponent Analysis:
- Analyze last 10 matches for stable estimates
- Focus on weaknesses you can exploit with your strengths
- Check venue splits (home/away differences)

### For Tactical Styles:
- Compare your style to upcoming opponents
- Look for mismatches (high press vs low build-up)
- Identify similar teams for inspiration

---

## 📊 Key Metrics Explained

| Metric | What It Means | Good Value |
|--------|---------------|------------|
| **PPG** | Points per game | >2.0 is excellent |
| **xG** | Expected goals (chance quality) | >1.5/game is strong attack |
| **xGA** | Expected goals against | <1.0/game is strong defense |
| **PPDA** | Passes allowed per defensive action | <8 = high press, >12 = deep block |
| **Shot Accuracy** | % shots on target | >35% is good |
| **Per 90** | Stat per 90 minutes | Normalizes for playing time |

---

## ⌨️ Keyboard Shortcuts (Streamlit)

- `Ctrl + R` - Rerun the app
- Use sidebar to navigate between pages
- Most charts are interactive (hover, zoom, pan)

---

## 🆘 Troubleshooting

**Dashboard won't load?**
- Check terminal for errors
- Ensure port 8501 is not in use
- Try: `streamlit run app.py --server.port 8502`

**No data showing?**
- Verify .csv files exist in `data/` folder
- Run data processing scripts again
- Check date filters aren't too restrictive

**Charts not displaying?**
- Reload page (F5)
- Check browser console for errors
- Try different browser (Chrome recommended)

---

## 📚 Additional Resources

- **Full documentation:** See `SETUP_GUIDE.md`
- **Project overview:** See `README.md`
- **Task completion:** See `Task_Checklist.md`

---

**Happy Analyzing! ⚽📊**
