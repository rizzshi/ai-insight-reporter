# 🎯 Getting Started Guide - AI Insight Reporter

Welcome to AI Insight Reporter! This guide will get you up and running in under 5 minutes.

---

## 📋 Prerequisites

- **Python 3.10 or higher** ([Download](https://www.python.org/downloads/))
- **pip** (comes with Python)
- **Terminal/Command Prompt** access

---

## 🚀 Installation (Choose Your Path)

### Path A: Automated Setup (Recommended)

```bash
# 1. Navigate to project directory
cd /Users/om/Documents/Github-Projects/AiInsight

# 2. Run setup wizard
python setup.py

# Follow the prompts - it will:
# ✓ Check Python version
# ✓ Create directories
# ✓ Install dependencies
# ✓ Generate sample data
# ✓ Run test analysis
```

### Path B: Manual Setup

```bash
# 1. Navigate to project directory
cd /Users/om/Documents/Github-Projects/AiInsight

# 2. Create virtual environment (recommended)
python -m venv venv

# 3. Activate virtual environment
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate     # Windows

# 4. Install dependencies
pip install -r requirements.txt

# 5. Generate sample data
python generate_sample_data.py

# 6. Test installation
python main.py data/sample_dataset.csv
```

---

## ✅ Verify Installation

After installation, verify everything works:

```bash
# Should show help message
python main.py --help

# Should launch web UI
streamlit run streamlit_app.py
```

If both commands work, you're ready to go! 🎉

---

## 🎓 Your First Analysis (3 Minutes)

### Option 1: Web UI (Easiest)

```bash
# 1. Launch the app
streamlit run streamlit_app.py

# 2. Open browser to: http://localhost:8501

# 3. Click "Browse files" and select:
data/sample_dataset.csv

# 4. Click "Generate AI Report"

# 5. Download your PDF report!
```

### Option 2: Command Line

```bash
# Run analysis on sample data
python main.py data/sample_dataset.csv

# Your report will be saved to:
# reports/Algorzen_Insight_Report_YYYYMMDD.pdf
```

---

## 📊 Analyze Your Own Data

### Step 1: Prepare Your Data

Supported formats:
- ✅ CSV (`.csv`)
- ✅ Excel (`.xlsx`, `.xls`)
- ✅ Parquet (`.parquet`)

Your data should have:
- Column headers (first row)
- At least 100 rows (more is better)
- Mix of numeric and text columns

### Step 2: Run Analysis

```bash
# Basic analysis
python main.py path/to/your/data.csv

# With custom author name
python main.py your_data.csv --author "Jane Doe"

# Save to custom location
python main.py your_data.csv --output custom_reports/

# See detailed progress
python main.py your_data.csv --verbose
```

---

## 🤖 Enable AI Narratives (Optional)

To use GPT-4 for enhanced narratives:

### Step 1: Get API Key

1. Go to: https://platform.openai.com/api-keys
2. Sign up / Log in
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)

### Step 2: Configure

**Method A: Environment File**
```bash
# Copy the example
cp .env.example .env

# Edit .env and add your key
OPENAI_API_KEY=sk-your-actual-key-here
```

**Method B: Command Line**
```bash
python main.py data.csv --api-key sk-your-key-here
```

**Method C: Streamlit UI**
- Open sidebar
- Check "Use GPT-4"
- Enter your API key

---

## 📚 Learn More

### Quick References

- **Common commands**: See `QUICK_REFERENCE.md`
- **Usage examples**: See `examples/README.md`
- **Troubleshooting**: See `TROUBLESHOOTING.md`
- **Full documentation**: See `README.md`

### Key Concepts

**Dataset Types** (auto-detected):
- 🛒 **Sales**: Revenue, products, orders
- 💰 **Finance**: Transactions, balances
- 👥 **Customer**: Churn, segments, value
- 📊 **General**: Everything else

**KPIs** (context-aware):
- Automatically extracted based on dataset type
- Industry-specific metrics
- Custom calculations

**Narratives** (AI-powered):
- Executive summaries
- Key findings
- Recommendations
- Risk analysis

---

## 🎯 Common Tasks

### Generate Multiple Reports

```bash
# Loop through files
for file in data/*.csv; do
    python main.py "$file" --author "Data Team"
done
```

### Schedule Daily Reports

```bash
# Add to crontab (Mac/Linux)
0 9 * * * cd ~/AiInsight && python main.py data/daily.csv

# Or use Task Scheduler (Windows)
# Action: Start a program
# Program: python
# Arguments: main.py data/daily.csv
# Start in: C:\path\to\AiInsight
```

### Integrate with Python Script

```python
from src import (
    load_dataset,
    perform_eda,
    extract_kpis,
    generate_narrative,
    generate_pdf_report
)

# Your workflow
df = load_dataset('data.csv')
eda = perform_eda(df)
kpis = extract_kpis(df, eda['dataset_info']['dataset_type'])
narrative = generate_narrative(eda, kpis)
pdf = generate_pdf_report(eda, kpis, narrative)

print(f"Report: {pdf}")
```

---

## 🆘 Need Help?

### Check Installation

```bash
# Verify Python version
python --version  # Should be 3.10+

# Check installed packages
pip list | grep -E "pandas|streamlit|reportlab|openai"

# Test imports
python -c "import pandas, streamlit, reportlab; print('✓ All good!')"
```

### Common Issues

| Problem | Quick Fix |
|---------|-----------|
| Import errors | `pip install -r requirements.txt` |
| Streamlit not found | `pip install streamlit` |
| No sample data | `python generate_sample_data.py` |
| Permission denied | `chmod +x setup.py` |
| PDF not generated | Check `reports/` directory exists |

### Still Stuck?

1. Check `TROUBLESHOOTING.md`
2. Run with `--verbose` flag
3. Open an issue on GitHub

---

## 🎓 Tutorial Walkthrough

### Complete Beginner Tutorial

```bash
# 1. Install everything
python setup.py
# Answer 'y' to all prompts

# 2. Launch web UI
streamlit run streamlit_app.py

# 3. In the browser:
#    - Upload: data/sample_dataset.csv
#    - Click: Generate AI Report
#    - Download the PDF

# 4. Try with CLI:
python main.py data/sample_dataset.csv --verbose

# 5. Check your report:
open reports/Algorzen_Insight_Report_*.pdf
```

### Intermediate Tutorial

```bash
# 1. Create your own data
cat > mydata.csv << EOF
product,sales,region
Widget,1000,North
Gadget,1500,South
Gizmo,800,East
EOF

# 2. Analyze it
python main.py mydata.csv --author "Your Name"

# 3. View results
ls -lh reports/
cat reports/report_metadata.json

# 4. Customize
# Edit src/kpi_extractor.py to add your KPIs
# Edit src/pdf_generator.py to change branding
```

---

## 🎉 Next Steps

Now that you're set up:

1. **Explore the UI**
   - Try different datasets
   - Experiment with settings
   - Download reports

2. **Read the Docs**
   - `README.md` - Full documentation
   - `examples/README.md` - Code examples
   - `QUICK_REFERENCE.md` - Command cheat sheet

3. **Customize**
   - Add custom KPIs
   - Change branding
   - Extend functionality

4. **Share**
   - Generate reports for stakeholders
   - Automate your workflows
   - Contribute improvements

---

## 📞 Support

- **Documentation**: `README.md`
- **Examples**: `examples/README.md`
- **Issues**: GitHub Issues
- **Questions**: GitHub Discussions

---

**Welcome to AI Insight Reporter!**

Built with ❤️ by Algorzen Research Division

© 2025 Algorzen Research | Om Singh

---

*Ready to transform your data into strategic intelligence?* 🚀
