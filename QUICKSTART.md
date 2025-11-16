# 🚀 Quick Start Guide

Get your BI Intelligence Agent System up and running in 5 minutes!

---

## Prerequisites

- Python 3.9 or higher
- pip package manager
- Google AI API key ([Get free key here](https://aistudio.google.com/app/apikey))

---

## Installation (3 Steps)

### Step 1: Install Dependencies

```bash
cd /Users/c9c4dd/kaggle
pip install -r requirements.txt
```

### Step 2: Configure API Key

```bash
# Create .env file from template
cp .env.example .env

# Edit .env and add your API key
# GOOGLE_API_KEY=your_actual_api_key_here
```

Or set directly in terminal:
```bash
export GOOGLE_API_KEY="your_api_key_here"
```

### Step 3: Test Installation

```bash
python demo.py
```

✅ If you see analysis results, you're all set!

---

## Usage Examples

### Example 1: Quick Analysis

```bash
python main.py analyze data/examples/sales_data.csv
```

**Output:** HTML report in `reports/` directory with visualizations in `outputs/`

### Example 2: Time Series Analysis

```bash
python main.py analyze data/examples/sales_data.csv \
  --type timeseries \
  --date-column Date \
  --value-column Revenue
```

### Example 3: Your Own Data

```bash
python main.py analyze path/to/your/data.csv
```

Supported formats: CSV, JSON, Excel (.xlsx, .xls)

---

## What You Get

Every analysis produces:

📊 **Comprehensive Report** (HTML)
- Professional formatting
- Embedded visualizations
- Executive summary
- Detailed statistics

📈 **Visualizations**
- Correlation heatmaps
- Distribution plots
- Time series charts
- Box plots for outliers

💡 **AI-Powered Insights**
- 5-7 actionable business insights
- Pattern identification
- Anomaly detection
- Trend analysis

📁 **Session Memory**
- Analysis history
- Learned patterns
- Context for future analyses

---

## Viewing Results

### Open HTML Report

```bash
# Mac
open reports/bi_report_*.html

# Linux
xdg-open reports/bi_report_*.html

# Windows
start reports/bi_report_*.html
```

### Check Visualizations

```bash
ls outputs/
```

### Review Session History

```bash
python main.py list-sessions
```

---

## Python API Usage

```python
from agents import CoordinatorAgent
from memory import MemoryBank

# Initialize
memory_bank = MemoryBank()
coordinator = CoordinatorAgent(memory_bank)

# Analyze
results = coordinator.analyze_file("data/sales_data.csv")

# Access results
print(f"Success: {results['success']}")
print(f"Report: {results['report_path']}")
print(f"Insights: {len(results['insights'])}")

# View insights
for insight in results['insights']:
    print(f"• {insight}")
```

---

## Common Issues & Solutions

### Issue: "GOOGLE_API_KEY not found"

**Solution:**
```bash
# Set in .env file
echo "GOOGLE_API_KEY=your_key_here" >> .env

# Or export in terminal
export GOOGLE_API_KEY="your_key_here"
```

### Issue: "Module not found"

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "File not found"

**Solution:** Check file path and ensure it exists
```bash
ls data/examples/sales_data.csv
```

### Issue: Permission errors on outputs

**Solution:**
```bash
mkdir -p outputs reports memory data
chmod 755 outputs reports memory data
```

---

## Next Steps

1. ✅ **Run the demo** to see all features
   ```bash
   python demo.py
   ```

2. 📊 **Analyze sample data** to understand outputs
   ```bash
   python main.py analyze data/examples/sales_data.csv
   ```

3. 🎯 **Try your own data** for real insights
   ```bash
   python main.py analyze your_data.csv
   ```

4. 📖 **Read full docs** for advanced features
   - `README.md` - Complete documentation
   - `DEPLOYMENT.md` - Production deployment
   - `CAPSTONE_WRITEUP.md` - Project details

---

## Getting Help

- **Documentation**: See README.md for detailed information
- **Examples**: Check `data/examples/` for sample datasets
- **Demo**: Run `demo.py` to see all features in action

---

## Features Highlights

✨ **Multi-Agent System**
- Coordinator, Analyst, Visualizer, Reporter agents
- Parallel and sequential execution
- Intelligent workflow orchestration

🛠️ **Custom Tools**
- Data ingestion (CSV, JSON, Excel)
- Statistical analysis
- Professional visualizations
- Report generation

💾 **Memory & Learning**
- Session persistence
- Pattern learning
- Context-aware recommendations

📈 **Observability**
- Structured logging
- Performance metrics
- Error tracking

🤖 **Powered by Google Gemini**
- AI-generated insights
- Natural language summaries
- Context-aware analysis

---

## Performance

Typical analysis of 1000-row dataset:
- ⏱️ **Time**: 15-30 seconds
- 📊 **Insights**: 5-7 actionable items
- 📈 **Visualizations**: 3-5 charts
- 📄 **Report**: Professional HTML format

---

## Project Structure

```
kaggle/
├── main.py              # CLI entry point (START HERE)
├── demo.py              # Feature demonstration
├── agents.py            # Multi-agent system
├── tools.py             # Analysis tools
├── memory.py            # Session management
├── observability.py     # Logging & metrics
├── evaluation.py        # Performance evaluation
├── config.py            # Configuration
├── requirements.txt     # Dependencies
├── .env.example         # Configuration template
├── README.md            # Full documentation
├── DEPLOYMENT.md        # Production deployment
└── CAPSTONE_WRITEUP.md  # Project writeup
```

---

## Example Output

```
╔══════════════════════════════════════════════════════════╗
║     📊 BI INTELLIGENCE AGENT SYSTEM 📊                   ║
╚══════════════════════════════════════════════════════════╝

🔍 Analyzing file: data/examples/sales_data.csv
⚙️  Initializing agents...
🚀 Starting analysis...

✅ Analysis Complete!
📁 Session ID: session_20241116_123456

📊 Data Summary:
   • Rows: 50
   • Columns: 7
   • Memory: 0.05 MB

💡 Key Insights (5):
   1. Strong positive correlation (r=0.94) between Units_Sold and Revenue
   2. Customer satisfaction increased 15% in Electronics category
   3. South region shows 22% higher growth rate
   4. Outlier detected: March 15 Mouse sales anomaly
   5. Furniture category steady 8% month-over-month growth

📈 Visualizations: 4 created
   • correlation_heatmap_20241116_123456.png
   • distribution_Revenue_20241116_123456.png
   • distribution_Units_Sold_20241116_123456.png
   • distribution_Customer_Satisfaction_20241116_123456.png

📄 Report: reports/bi_report_20241116_123456.html

════════════════════════════════════════════════════════════
Open the HTML report in your browser to view full analysis!
════════════════════════════════════════════════════════════
```

---

**Ready to analyze your data? Run this command:**

```bash
python main.py analyze data/examples/sales_data.csv
```

**That's it! You're now using AI agents for business intelligence!** 🎉

---

*Built for the Google AI Agents Intensive Course Capstone Project*

