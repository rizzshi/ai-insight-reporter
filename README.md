# 🤖 AI Insight Reporter

> **Autonomous Business Intelligence System by Algorzen Research Division**

An enterprise-grade data analytics automation platform that transforms raw datasets into executive-level business intelligence reports with AI-powered narratives, comprehensive EDA, and professional PDF outputs.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenAI GPT-4](https://img.shields.io/badge/AI-GPT--4-green.svg)](https://openai.com/)

---

## 🌟 Features

### 🔹 Core Analytics Engine
- ✅ **Automatic Dataset Detection** — Identifies sales, finance, customer, or general data types
- ✅ **Comprehensive EDA** — Missing values, statistics, correlations, distributions
- ✅ **Smart KPI Extraction** — Context-aware metrics based on dataset characteristics
- ✅ **Interactive Visualizations** — Heatmaps, distributions, and statistical plots

### 🔹 AI-Powered Insights
- ✅ **GPT-4 Integration** — Executive-level narratives with strategic recommendations
- ✅ **Fallback Intelligence** — Rule-based narrative generation when API unavailable
- ✅ **Business Tone** — Professional, McKinsey-style executive summaries
- ✅ **Actionable Recommendations** — Data-driven strategic insights

### 🔹 Professional Reporting
- ✅ **Branded PDF Reports** — Algorzen Research Division formatting
- ✅ **Executive Presentation Quality** — Ready for stakeholder meetings
- ✅ **Metadata Tracking** — JSON reports with full traceability
- ✅ **Multi-Format Support** — CSV, Excel, Parquet inputs

### 🔹 Deployment Options
- ✅ **Streamlit Web UI** — User-friendly drag-and-drop interface
- ✅ **CLI Tool** — Scriptable command-line automation
- ✅ **Modular API** — Integrate into existing pipelines

---

## 📦 Installation

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Quick Setup

```bash
# 1. Clone the repository
git clone https://github.com/rizzshi/AiInsight.git
cd AiInsight

# 2. Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables (optional for GPT-4)
cp .env.example .env
# Edit .env and add your OpenAI API key
```

---

## 🚀 Quick Start

### Option 1: Streamlit Web UI (Recommended for Beginners)

```bash
streamlit run streamlit_app.py
```

Then open your browser to `http://localhost:8501` and:
1. Upload your dataset (CSV, Excel, or Parquet)
2. Configure settings in the sidebar
3. Click "Generate AI Report"
4. Download your professional PDF report

### Option 2: Command Line Interface

```bash
# Generate sample dataset first (optional)
python -c "from src.utils import generate_sample_sales_data; generate_sample_sales_data(1000).to_csv('data/sample_dataset.csv', index=False)"

# Run analysis on sample data
python main.py data/sample_dataset.csv

# Or analyze your own dataset
python main.py path/to/your/data.csv --author "Your Name"

# With GPT-4 (requires API key)
python main.py data/your_data.csv --api-key sk-your-key-here --verbose
```

### Option 3: Python API

```python
import pandas as pd
from src.eda_engine import perform_eda
from src.kpi_extractor import extract_kpis
from src.ai_narrator import generate_narrative
from src.pdf_generator import generate_pdf_report

# Load your data
df = pd.read_csv('your_data.csv')

# Run automated analysis
eda_summary = perform_eda(df)
kpis = extract_kpis(df, eda_summary['dataset_info']['dataset_type'])
narrative = generate_narrative(eda_summary, kpis)

# Generate PDF report
pdf_path = generate_pdf_report(eda_summary, kpis, narrative)
print(f"Report saved to: {pdf_path}")
```

---

## 📊 Sample Dataset

A synthetic sales dataset with 1,000 records is included for testing:

```bash
# Generate sample data
python src/utils.py

# Analyze sample data
python main.py data/sample_dataset.csv --verbose
```

**Sample Dataset Schema:**
- Transaction ID, Date, Product, Category
- Region, Channel, Quantity, Pricing
- Revenue, Discounts, Profit Margins
- Customer IDs

---

## 🧠 How It Works

### 1. Dataset Type Detection
The system analyzes column names and data patterns to automatically classify datasets:
- **Sales**: Revenue, products, quantities, pricing
- **Finance**: Transactions, balances, debits/credits
- **Customer**: Churn, segments, lifetime value
- **General**: Fallback for other dataset types

### 2. Automated EDA
Comprehensive exploratory data analysis includes:
- Missing value detection and quantification
- Statistical summaries (mean, median, std dev, quartiles)
- Correlation analysis with heatmap visualization
- Distribution plots for numeric and categorical features

### 3. KPI Extraction
Context-aware KPI calculation based on dataset type:

| Dataset Type | Example KPIs |
|--------------|--------------|
| **Sales** | Total Revenue, Average Order Value, Top Products, Margin Analysis |
| **Finance** | Total Balance, Net Position, Transaction Volume, Account Metrics |
| **Customer** | Churn Rate, Retention Rate, Avg Customer Value, Segment Distribution |
| **General** | Data Completeness, Record Count, Feature Diversity |

### 4. AI Narrative Generation
Two-tier intelligent narrative system:

**Tier 1: GPT-4 (when API key provided)**
- Executive summary (3-5 sentences)
- Key findings (4-6 bullet points)
- Actionable recommendations
- Risks and limitations

**Tier 2: Rule-Based Fallback**
- Pattern-based insights
- Statistical observations
- Domain-specific recommendations
- Data quality assessment

### 5. PDF Report Assembly
Professional report generation with:
- Algorzen Research Division branding
- Title page with metadata
- KPI summary tables
- Visualizations (heatmaps, distributions)
- AI-generated narratives
- Data quality appendix

---

## ⚙️ Configuration

### Environment Variables (`.env`)

```bash
# OpenAI Configuration (optional)
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_MODEL=gpt-4-turbo-preview

# Report Branding (optional)
COMPANY_NAME=Algorzen Research Division
AUTHOR_NAME=Rishi Singh
```

### CLI Arguments

```bash
python main.py --help

Arguments:
  input_file              Path to dataset (CSV, Excel, Parquet)
  
Options:
  --output DIR            Output directory (default: reports/)
  --author NAME           Report author (default: Rishi Singh)
  --api-key KEY           OpenAI API key for GPT-4
  --no-pdf                Skip PDF generation
  --verbose               Show detailed progress
```

---

## 📁 Project Structure

```
AiInsight/
├── src/
│   ├── eda_engine.py          # Automated EDA engine
│   ├── kpi_extractor.py       # KPI calculation module
│   ├── ai_narrator.py         # GPT-4 narrative generator
│   ├── pdf_generator.py       # PDF report builder
│   └── utils.py               # Helper functions
├── data/
│   └── sample_dataset.csv     # Sample sales data (1000 records)
├── reports/
│   ├── assets/                # Generated charts and visualizations
│   ├── Algorzen_Insight_Report_YYYYMMDD.pdf
│   └── report_metadata.json   # Report metadata
├── main.py                    # CLI entry point
├── streamlit_app.py           # Web UI application
├── requirements.txt           # Python dependencies
├── .env.example               # Environment variable template
└── README.md                  # This file
```

---

## 🎯 Use Cases

### Business Intelligence Teams
- Automate routine data analysis reports
- Generate executive summaries for stakeholders
- Standardize reporting across departments

### Data Analysts
- Quick exploratory data analysis
- Automated KPI tracking
- Professional report generation

### Consultants
- Client data analysis and reporting
- Strategic insights with AI narratives
- Branded deliverables

### Startups & SMBs
- Cost-effective business intelligence
- No-code analytics for non-technical users
- Scalable reporting infrastructure

---

## 🔧 Advanced Usage

### Custom Dataset Type Detection

```python
from src.eda_engine import EDAEngine

# Force specific dataset type
df = pd.read_csv('your_data.csv')
engine = EDAEngine(df)
engine.dataset_type = 'finance'  # Override auto-detection
summary = engine.run_full_eda()
```

### Integration with Data Pipelines

```python
# Example: Daily automated reporting
import schedule
from src.utils import load_dataset
from main import main

def daily_report():
    # Your ETL pipeline
    df = extract_from_database()
    df.to_csv('temp_data.csv', index=False)
    
    # Generate report
    import sys
    sys.argv = ['main.py', 'temp_data.csv', '--verbose']
    main()

schedule.every().day.at("09:00").do(daily_report)
```

### Custom KPI Definitions

```python
from src.kpi_extractor import KPIExtractor

class CustomKPIExtractor(KPIExtractor):
    def extract_custom_kpis(self):
        kpis = {}
        # Your custom KPI logic here
        kpis['Custom Metric'] = calculate_custom_metric(self.df)
        return kpis
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

```bash
# Clone and setup
git clone https://github.com/rizzshi/AiInsight.git
cd AiInsight

# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8

# Run tests (when available)
pytest tests/

# Format code
black src/ *.py
```

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👨‍💻 Author

**Rishi Singh**  
Algorzen Research Division

- GitHub: [@rizzshi](https://github.com/rizzshi)
- Project: [DataSphere/AiInsight](https://github.com/rizzshi/DataSphere)

---

## 🙏 Acknowledgments

- OpenAI for GPT-4 API
- ReportLab for PDF generation
- Streamlit for web UI framework
- The open-source data science community

---

## 📮 Support

For questions, issues, or feature requests:
- Open an issue on GitHub
- Contact: Rishi Singh via GitHub

---

## 🔮 Roadmap

### Planned Features
- [ ] Multi-language narrative support
- [ ] Custom branding templates
- [ ] Real-time data source connectors (SQL, APIs)
- [ ] Automated email report delivery
- [ ] Interactive dashboard mode
- [ ] Advanced statistical tests
- [ ] Time series forecasting
- [ ] Anomaly detection
- [ ] Collaborative annotations
- [ ] Report version control

---

<div align="center">

**Built with ❤️ by Algorzen Research Division**

*Transforming Data into Strategic Intelligence*

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red?logo=streamlit&logoColor=white)](https://streamlit.io)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-green?logo=openai&logoColor=white)](https://openai.com)

</div>
