# 🎬 Video Shot List - What to Show When

## Quick Reference Guide for Recording

---

## 🎥 SHOT-BY-SHOT BREAKDOWN

### **SHOT 1: Opening Title** (0:00-0:05)
**Show:**
- Project title card OR
- GitHub repository homepage
- Text overlay: "BI Intelligence Agent System"

**Say:**
> "Hi! I'm presenting the BI Intelligence Agent System..."

---

### **SHOT 2: Problem Statement** (0:05-0:30)
**Show:**
- README.md section on problem
- OR simple text slide with bullet points:
  ```
  PROBLEMS:
  • 4-8 hours per dataset
  • Inconsistent quality
  • Expensive ($100k+ analysts)
  • Insights too late
  ```

**Say:**
> "The problem: Traditional BI analysis is time-consuming... [continue script]"

---

### **SHOT 3: Architecture Overview** (0:30-0:50)
**Show:**
- README.md architecture diagram
- OR show this in terminal:
  ```
  Coordinator Agent
       ↓
  [Analyst + Visualizer] (Parallel)
       ↓
  Report Generator (Sequential)
       ↓
  Memory Bank
  ```

**Say:**
> "Why agents? This problem uniquely benefits... [continue script]"

---

### **SHOT 4: Code Structure** (0:50-1:10)
**Show:**
- GitHub repository file list
- Briefly scroll through `agents.py` (just to show it's real code)
- Show file structure:
  ```
  agents.py           # 541 lines
  tools.py            # 380 lines
  memory.py           # 350 lines
  observability.py    # 142 lines
  ```

**Say:**
> "The architecture uses four specialized agents... [continue script]"

---

### **SHOT 5: Demo Setup** (1:10-1:15)
**Show:**
- Terminal window
- Your current directory: `/Users/c9c4dd/kaggle`
- Show the data file:
  ```bash
  ls data/examples/
  # sales_data.csv  employee_data.json
  ```

**Say:**
> "Let me show you a live demo. I'll analyze this sales dataset..."

---

### **SHOT 6: Running Analysis** (1:15-1:35)
**Show:**
- Terminal: Type and run:
  ```bash
  python main.py analyze data/examples/sales_data.csv
  ```
- Show the progress messages:
  ```
  🔍 Analyzing file: data/examples/sales_data.csv
  ⚙️  Initializing agents...
  🚀 Starting analysis...
  ✅ Analysis Complete!
  ```

**Say:**
> "Watch as the system works... [narrate what's happening]"

---

### **SHOT 7: Analysis Results** (1:35-1:50)
**Show:**
- Terminal output showing:
  ```
  📊 Data Summary:
     • Rows: 50
     • Columns: 7
  
  💡 Key Insights (5):
     1. Strong positive correlation...
     2. Customer satisfaction increased...
  
  📈 Visualizations: 4 created
  📄 Report: reports/bi_report_*.html
  ```

**Say:**
> "In just 28 seconds, we get a comprehensive report..."

---

### **SHOT 8: Opening HTML Report** (1:50-2:00)
**Show:**
- Browser opening
- HTML report loading
- Scroll to show header with title and timestamp

**Say:**
> "Look at this professional HTML report..."

---

### **SHOT 9: Report Visualizations** (2:00-2:10)
**Show:**
- Scroll through report showing:
  1. Correlation heatmap
  2. Distribution plots
  3. Data summary section

**Say:**
> "We have professional visualizations, statistical analysis..."

---

### **SHOT 10: Key Insights** (2:10-2:20)
**Show:**
- Insights section in report
- Highlight 2-3 specific insights by hovering/scrolling slowly

**Say:**
> "And five AI-generated business insights. Look at these..."

---

### **SHOT 11: GitHub Repository** (2:20-2:35)
**Show:**
- GitHub: https://github.com/pharsha9/kaggleproject
- Scroll through files quickly
- Show README.md preview
- Show green "committed" indicators

**Say:**
> "How I built this: The system uses Google Gemini..."

---

### **SHOT 12: Documentation** (2:35-2:45)
**Show:**
- README.md on GitHub
- Quickly show:
  - DEPLOYMENT.md
  - QUICKSTART.md
  - Other docs

**Say:**
> "It's over 2000 lines of production-ready Python code..."

---

### **SHOT 13: Results Summary** (2:45-2:55)
**Show:**
- Simple results slide:
  ```
  RESULTS:
  ⏱️  10x Faster (28 sec vs 5+ hours)
  💰 90% Cost Reduction  
  🎯 Consistent Quality
  🔄 Continuous Learning
  ```

**Say:**
> "The results: 10x faster, 90% cost reduction..."

---

### **SHOT 14: Closing** (2:55-3:00)
**Show:**
- Title slide with:
  ```
  BI Intelligence Agent System
  Google AI Agents Capstone Project
  
  GitHub: github.com/pharsha9/kaggleproject
  ```

**Say:**
> "This is the BI Intelligence Agent System. Thank you!"

---

## 🎯 TIMING GUIDE

| Section | Duration | Cumulative |
|---------|----------|------------|
| Opening | 5s | 0:05 |
| Problem | 25s | 0:30 |
| Why Agents | 20s | 0:50 |
| Architecture | 20s | 1:10 |
| Demo Setup | 5s | 1:15 |
| Running | 20s | 1:35 |
| Results | 15s | 1:50 |
| Open Report | 10s | 2:00 |
| Visualizations | 10s | 2:10 |
| Insights | 10s | 2:20 |
| GitHub | 15s | 2:35 |
| Docs | 10s | 2:45 |
| Results | 10s | 2:55 |
| Closing | 5s | 3:00 |

---

## 📱 RECORDING SHORTCUTS

### Mac Recording with QuickTime

```bash
# 1. Open QuickTime Player
open -a "QuickTime Player"

# 2. File → New Screen Recording (or Cmd+Control+N)

# 3. Click record, select area or full screen

# 4. Click Stop in menu bar when done

# 5. File → Save (Cmd+S)
```

### Using Screenshot Tool (Mac)

```bash
# Press: Cmd + Shift + 5
# Select: "Record Entire Screen" or "Record Selected Portion"
# Click: Options → Microphone → Select your mic
# Click: Record
# Click: Stop in menu bar when done
```

---

## 🎬 ALTERNATIVE: Simple Slideshow + Voiceover

If live recording feels difficult, create slides:

### Tools:
- Google Slides (free)
- PowerPoint
- Keynote (Mac)

### Slides to Create:

1. **Title Slide** - Project name
2. **Problem Slide** - 4 bullet points
3. **Solution Slide** - Architecture diagram
4. **Agents Slide** - 4 agent boxes
5. **Demo Slide** - Screenshot of terminal
6. **Results Slide** - Screenshot of report
7. **Code Slide** - Screenshot of GitHub
8. **Impact Slide** - Metrics
9. **End Slide** - Thank you + link

### Record:
- Google Slides: Present → Record
- PowerPoint: Slide Show → Record
- Export as video
- Upload to YouTube

---

## 💡 PRO TIPS

### For Best Results:

1. **Lighting**: Record during daytime or use lamp
2. **Audio**: Use earbuds/headset mic (better than laptop)
3. **Background**: Clean desktop, close unnecessary windows
4. **Pace**: Speak slowly and clearly
5. **Practice**: Do 1-2 practice runs before final recording
6. **Energy**: Smile while talking (it comes through in voice!)

### Common Mistakes to Avoid:

❌ Going over 3 minutes (instant disqualification from bonus)
❌ No audio or too quiet
❌ Rushing through demo
❌ Not showing actual working code
❌ Forgetting to mention Gemini/Google AI

---

## ✅ PRE-RECORDING TEST

Run this checklist before hitting record:

```bash
# 1. Test your demo command
cd /Users/c9c4dd/kaggle
python main.py analyze data/examples/sales_data.csv

# 2. Verify report opens
open reports/bi_report_*.html

# 3. Check GitHub loads
# Visit: https://github.com/pharsha9/kaggleproject

# 4. Test microphone (record 5 seconds and play back)

# 5. Check recording software works

# 6. Turn off notifications:
# Mac: Option+Click bell icon in menu bar
```

---

## 🎥 SIMPLEST RECORDING METHOD

**For absolute beginners:**

1. **Use Loom** (https://www.loom.com)
   - Free, no editing needed
   - Browser-based
   - Auto-uploads to cloud

2. **Follow this sequence:**
   - Show GitHub README (30 sec)
   - Run terminal demo (60 sec)
   - Show HTML report (30 sec)
   - Show GitHub files (30 sec)
   - Show results (30 sec)

3. **Download from Loom**

4. **Upload to YouTube**

**Total time: 20 minutes including upload!**

---

## 📤 QUICK YOUTUBE UPLOAD

Once video is ready:

1. **Go to**: youtube.com/upload

2. **Upload file**

3. **Copy-paste these:**

**Title:**
```
BI Intelligence Agent System - Multi-Agent BI Analyzer (Google AI Capstone)
```

**Description:**
```
Multi-agent business intelligence system built for Google AI Agents Intensive Course Capstone Project.

GitHub: https://github.com/pharsha9/kaggleproject

Features:
• 4 specialized AI agents
• 10x faster than manual analysis  
• Powered by Google Gemini 2.0
• Production-ready deployment

Track: Enterprise Agents
```

4. **Set visibility**: Public or Unlisted

5. **Click Publish**

6. **Copy YouTube URL**

7. **Add to Kaggle submission!**

---

## 🎊 YOU'VE GOT THIS!

The video is easier than you think. Your project is excellent - just show it off!

**Key points:**
- Keep it under 3 minutes ✓
- Show working demo ✓
- Mention Gemini ✓
- Show GitHub repo ✓

**Good luck recording! 🎬**

