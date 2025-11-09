# AI Insight Reporter - Usage Examples

This directory contains examples demonstrating different ways to use the AI Insight Reporter.

## 📚 Examples Included

### 1. Basic CLI Usage
```bash
# Generate sample dataset
python generate_sample_data.py --records 1000

# Run basic analysis
python main.py data/sample_dataset.csv

# Run with custom author
python main.py data/sample_dataset.csv --author "John Doe"

# Verbose output
python main.py data/sample_dataset.csv --verbose
```

### 2. Web UI Usage
```bash
# Launch Streamlit app
streamlit run streamlit_app.py

# Then:
# 1. Upload your CSV/Excel/Parquet file
# 2. Configure settings in sidebar
# 3. Click "Generate AI Report"
# 4. Download PDF and metadata
```

### 3. Python API Usage

```python
import pandas as pd
from src import (
    perform_eda,
    extract_kpis,
    generate_narrative,
    generate_pdf_report
)

# Load your data
df = pd.read_csv('your_data.csv')

# Run comprehensive analysis
eda_summary = perform_eda(df)
dataset_type = eda_summary['dataset_info']['dataset_type']
kpis = extract_kpis(df, dataset_type)
narrative = generate_narrative(eda_summary, kpis)

# Generate PDF report
pdf_path = generate_pdf_report(
    eda_summary, 
    kpis, 
    narrative,
    author="Your Name"
)

print(f"Report saved: {pdf_path}")
```

### 4. Advanced: Custom KPI Extraction

```python
from src.kpi_extractor import KPIExtractor

class CustomKPIExtractor(KPIExtractor):
    """Custom KPI extractor with domain-specific metrics"""
    
    def extract_custom_metrics(self):
        kpis = {}
        
        # Your custom logic
        if 'conversion_rate' in self.df.columns:
            kpis['Avg Conversion Rate'] = f"{self.df['conversion_rate'].mean():.2f}%"
        
        return kpis

# Use custom extractor
extractor = CustomKPIExtractor(df, 'sales')
custom_kpis = extractor.extract_custom_metrics()
```

### 5. Batch Processing

```python
from pathlib import Path
from src import load_dataset, perform_eda, generate_pdf_report

# Process multiple files
data_dir = Path('data/monthly_reports')
for file in data_dir.glob('*.csv'):
    print(f"Processing {file.name}...")
    
    df = load_dataset(file)
    eda = perform_eda(df)
    kpis = extract_kpis(df, eda['dataset_info']['dataset_type'])
    narrative = generate_narrative(eda, kpis)
    
    pdf_path = generate_pdf_report(
        eda, kpis, narrative,
        output_dir=f"reports/{file.stem}"
    )
    
    print(f"✓ Report saved: {pdf_path}")
```

### 6. With GPT-4 API

```python
import os
from src import generate_narrative

# Set API key
os.environ['OPENAI_API_KEY'] = 'sk-your-key-here'

# Or pass directly
narrative = generate_narrative(
    eda_summary, 
    kpis,
    api_key='sk-your-key-here'
)

print(f"Generation method: {narrative['method']}")  # Should be 'gpt-4'
print(narrative['narrative'])
```

### 7. Scheduled Reporting (Cron/Task Scheduler)

```bash
# Add to crontab (Linux/Mac)
# Daily report at 9 AM
0 9 * * * cd /path/to/AiInsight && /path/to/python main.py data/daily_data.csv

# Or create a shell script
#!/bin/bash
cd /path/to/AiInsight
source venv/bin/activate
python main.py data/latest_data.csv --author "Automated System"
```

### 8. Integration with Data Pipelines

```python
# Example: Airflow DAG integration
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys
sys.path.insert(0, '/path/to/AiInsight')

from src import perform_eda, generate_pdf_report

def generate_daily_report(**context):
    # Your data extraction logic
    df = extract_data_from_warehouse()
    
    # Generate report
    eda = perform_eda(df)
    kpis = extract_kpis(df, eda['dataset_info']['dataset_type'])
    narrative = generate_narrative(eda, kpis)
    pdf_path = generate_pdf_report(eda, kpis, narrative)
    
    return pdf_path

dag = DAG(
    'daily_insight_report',
    start_date=datetime(2025, 1, 1),
    schedule_interval='0 9 * * *'
)

report_task = PythonOperator(
    task_id='generate_insight_report',
    python_callable=generate_daily_report,
    dag=dag
)
```

### 9. Export to Different Formats

```python
import json
from src import perform_eda

# Run analysis
eda = perform_eda(df)
kpis = extract_kpis(df, eda['dataset_info']['dataset_type'])

# Save as JSON
with open('analysis_results.json', 'w') as f:
    json.dump({
        'eda': eda,
        'kpis': kpis
    }, f, indent=2, default=str)

# Or use the utility function
from src.utils import save_summary_json
save_summary_json(eda, 'reports/eda_summary.json')
```

### 10. Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run as web service
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]

# Or as CLI tool
# CMD ["python", "main.py", "data/sample_dataset.csv"]
```

```bash
# Build and run
docker build -t ai-insight-reporter .
docker run -p 8501:8501 ai-insight-reporter
```

## 🎯 Common Use Cases

### Use Case 1: Quick Dataset Analysis
```bash
# Just want to see what's in your data?
python main.py your_data.csv --verbose
```

### Use Case 2: Executive Presentation
```bash
# Need a professional report for stakeholders?
python main.py quarterly_data.csv --author "Data Team" --api-key sk-xxx
# Use the generated PDF in your presentation
```

### Use Case 3: Data Quality Check
```python
from src.utils import validate_dataframe
import pandas as pd

df = pd.read_csv('your_data.csv')
quality = validate_dataframe(df)

print(f"Data Completeness: {quality['completeness_pct']:.2f}%")
print(f"Missing Cells: {quality['missing_cells']:,}")
```

## 📖 More Resources

- **Full Documentation**: See `../README.md`
- **API Reference**: See docstrings in `src/` modules
- **Web UI**: Run `streamlit run streamlit_app.py`
- **Support**: Open an issue on GitHub
