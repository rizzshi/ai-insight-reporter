# 🚀 Quick Reference - AI Insight Reporter

## ⚡ Quick Start (30 seconds)

```bash
# 1. Setup (one time)
pip install -r requirements.txt

# 2. Generate sample data
python generate_sample_data.py

# 3. Run analysis
python main.py data/sample_dataset.csv
```

---

## 📋 Common Commands

### CLI Usage
```bash
# Basic analysis
python main.py data/mydata.csv

# With custom author
python main.py data/mydata.csv --author "Your Name"

# Verbose output
python main.py data/mydata.csv --verbose

# With GPT-4
python main.py data/mydata.csv --api-key sk-xxx

# Custom output directory
python main.py data/mydata.csv --output reports/custom/

# Skip PDF (testing only)
python main.py data/mydata.csv --no-pdf
```

### Web UI
```bash
# Launch Streamlit app
streamlit run streamlit_app.py

# Custom port
streamlit run streamlit_app.py --server.port 8080
```

### Generate Sample Data
```bash
# Default 1000 records
python generate_sample_data.py

# Custom size
python generate_sample_data.py --records 5000

# Custom output
python generate_sample_data.py --output data/custom.csv
```

---

## 🐍 Python API

### Basic Usage
```python
from src import perform_eda, extract_kpis, generate_narrative, generate_pdf_report
import pandas as pd

df = pd.read_csv('data.csv')
eda = perform_eda(df)
kpis = extract_kpis(df, eda['dataset_info']['dataset_type'])
narrative = generate_narrative(eda, kpis)
pdf = generate_pdf_report(eda, kpis, narrative)
```

### Load Different File Types
```python
from src.utils import load_dataset

df = load_dataset('data.csv')      # CSV
df = load_dataset('data.xlsx')     # Excel
df = load_dataset('data.parquet')  # Parquet
```

### Generate Sample Data
```python
from src.utils import generate_sample_sales_data

df = generate_sample_sales_data(1000)
df.to_csv('sample.csv', index=False)
```

### Validate Data Quality
```python
from src.utils import validate_dataframe

quality = validate_dataframe(df)
print(f"Completeness: {quality['completeness_pct']:.2f}%")
```

---

## 🎯 Dataset Type Detection

The system auto-detects based on column names:

| Type | Keywords |
|------|----------|
| **Sales** | sales, revenue, price, quantity, product, order |
| **Finance** | balance, debit, credit, transaction, account |
| **Customer** | customer, churn, retention, lifetime, segment |
| **General** | Everything else |

### Override Detection
```python
from src.eda_engine import EDAEngine

engine = EDAEngine(df)
engine.dataset_type = 'sales'  # Force type
summary = engine.run_full_eda()
```

---

## 📊 KPI Examples

### Sales KPIs
- Total Revenue
- Average Order Value  
- Total Units Sold
- Top Product
- Average Margin

### Finance KPIs
- Total Balance
- Net Position
- Total Credits/Debits
- Transaction Types

### Customer KPIs
- Churn Rate
- Retention Rate
- Average Customer Value
- Customer Segments

---

## 🤖 AI Narrative Options

### Use GPT-4
```python
narrative = generate_narrative(eda, kpis, api_key='sk-xxx')
```

### Use Fallback (No API)
```python
narrative = generate_narrative(eda, kpis)  # No key = fallback
```

### Force Fallback (Testing)
```python
narrative = generate_narrative(eda, kpis, force_fallback=True)
```

### Check Method Used
```python
print(narrative['method'])  # 'gpt-4' or 'fallback'
print(narrative['model'])   # Model name
```

---

## 📁 File Structure

```
AiInsight/
├── src/                   # Core modules
│   ├── eda_engine.py     # EDA automation
│   ├── kpi_extractor.py  # KPI extraction
│   ├── ai_narrator.py    # AI narratives
│   ├── pdf_generator.py  # PDF reports
│   └── utils.py          # Utilities
├── data/                  # Input datasets
├── reports/               # Output reports
│   ├── assets/           # Charts/plots
│   └── *.pdf             # Generated PDFs
├── main.py               # CLI entry
├── streamlit_app.py      # Web UI
└── requirements.txt      # Dependencies
```

---

## ⚙️ Environment Variables

Create `.env` file:

```bash
# Optional - for GPT-4
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4-turbo-preview

# Optional - branding
COMPANY_NAME=Algorzen Research Division
AUTHOR_NAME=Om Singh
```

---

## 🎨 Output Files

After running analysis:

```
reports/
├── Algorzen_Insight_Report_YYYYMMDD.pdf  # Main report
├── report_metadata.json                   # Metadata
└── assets/
    ├── correlation_heatmap.png
    ├── numeric_distributions.png
    └── categorical_distributions.png
```

---

## 🔧 Customization

### Custom KPIs
```python
from src.kpi_extractor import KPIExtractor

class MyKPIExtractor(KPIExtractor):
    def extract_custom_kpis(self):
        return {'My KPI': 'Value'}

extractor = MyKPIExtractor(df, 'sales')
kpis = extractor.extract_all_kpis()
```

### Custom Report Branding
Edit `src/pdf_generator.py`:
- Line 90-100: Header/footer text
- Line 60-70: Color scheme
- Line 120-130: Title page layout

---

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Import errors | `pip install -r requirements.txt` |
| No API key | System uses fallback automatically |
| Large dataset slow | Sample first: `df.sample(10000)` |
| PDF missing charts | Check `reports/assets/` exists |
| Upload fails (Streamlit) | Check file size < 200MB |

See `TROUBLESHOOTING.md` for more details.

---

## 📚 Documentation

- **Full Docs**: `README.md`
- **Examples**: `examples/README.md`
- **Troubleshooting**: `TROUBLESHOOTING.md`
- **API Docs**: Docstrings in `src/` modules

---

## 🚀 Keyboard Shortcuts (Streamlit)

| Key | Action |
|-----|--------|
| `R` | Rerun app |
| `C` | Clear cache |
| `?` | Show keyboard shortcuts |

---

## 💡 Pro Tips

1. **Always use virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. **Sample large datasets first**
   ```python
   df = pd.read_csv('big.csv', nrows=10000)
   ```

3. **Use verbose mode for debugging**
   ```bash
   python main.py data.csv --verbose
   ```

4. **Check data quality first**
   ```python
   from src.utils import validate_dataframe
   print(validate_dataframe(df))
   ```

5. **Start with fallback, add GPT-4 later**
   ```bash
   # First run without API
   python main.py data.csv
   
   # Then add GPT-4
   python main.py data.csv --api-key sk-xxx
   ```

---

## 📞 Support

- **Issues**: GitHub Issues
- **Questions**: GitHub Discussions  
- **Author**: Om Singh (@rizzshi)
- **Project**: https://github.com/rizzshi/DataSphere

---

**Built with ❤️ by Algorzen Research Division**

© 2025 Algorzen Research | Om Singh
