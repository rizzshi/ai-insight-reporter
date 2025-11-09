# 🚨 Troubleshooting Guide - AI Insight Reporter

Common issues and solutions for the AI Insight Reporter.

---

## 📦 Installation Issues

### Problem: `Import "pandas" could not be resolved`

**Solution:**
```bash
# Make sure you're in the virtual environment
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### Problem: `ModuleNotFoundError: No module named 'reportlab'`

**Solution:**
```bash
pip install reportlab
# Or reinstall all dependencies
pip install -r requirements.txt --upgrade
```

### Problem: Python version incompatibility

**Solution:**
```bash
# Check your Python version
python --version

# Need Python 3.10+
# If using older version, upgrade or use pyenv
pyenv install 3.10.0
pyenv local 3.10.0
```

---

## 🤖 OpenAI API Issues

### Problem: `OpenAI API authentication failed`

**Solution:**
1. Check your API key is valid: https://platform.openai.com/api-keys
2. Ensure `.env` file exists with correct format:
   ```
   OPENAI_API_KEY=sk-your-actual-key-here
   ```
3. Or pass key directly:
   ```bash
   python main.py data.csv --api-key sk-your-key
   ```

### Problem: `Rate limit exceeded`

**Solution:**
- OpenAI has rate limits on API calls
- The system automatically falls back to rule-based narrative
- Wait a few minutes and try again
- Or upgrade your OpenAI plan for higher limits

### Problem: Narrative generation is slow

**Solution:**
- GPT-4 can take 10-30 seconds to generate narratives
- Use `--verbose` flag to see progress
- Consider using fallback mode for faster results:
  ```python
  narrative = generate_narrative(eda, kpis, force_fallback=True)
  ```

---

## 📊 Data Loading Issues

### Problem: `FileNotFoundError: File not found`

**Solution:**
```bash
# Use absolute paths
python main.py /full/path/to/data.csv

# Or relative from project root
python main.py data/sample_dataset.csv

# Check file exists
ls -la data/
```

### Problem: `UnicodeDecodeError` when loading CSV

**Solution:**
```python
# Specify encoding when loading
df = pd.read_csv('data.csv', encoding='utf-8')
# Or
df = pd.read_csv('data.csv', encoding='latin-1')
```

### Problem: Excel file not loading

**Solution:**
```bash
# Install Excel support
pip install openpyxl xlrd

# For older .xls files
pip install xlrd
```

### Problem: Large dataset causes memory error

**Solution:**
```python
# Load only needed columns
df = pd.read_csv('large_file.csv', usecols=['col1', 'col2', 'col3'])

# Or sample the data
df = pd.read_csv('large_file.csv', nrows=10000)

# Use chunks
for chunk in pd.read_csv('large_file.csv', chunksize=10000):
    # Process each chunk
    process_chunk(chunk)
```

---

## 📄 PDF Generation Issues

### Problem: `No module named 'PIL'`

**Solution:**
```bash
pip install Pillow
```

### Problem: PDF fonts look wrong

**Solution:**
- ReportLab uses built-in fonts by default
- For custom fonts, register them:
  ```python
  from reportlab.pdfbase import pdfmetrics
  from reportlab.pdfbase.ttfonts import TTFont
  pdfmetrics.registerFont(TTFont('CustomFont', 'path/to/font.ttf'))
  ```

### Problem: Charts not appearing in PDF

**Solution:**
1. Check charts were generated:
   ```bash
   ls -la reports/assets/
   ```
2. Ensure charts saved successfully:
   ```python
   # Check visualization paths
   print(eda_summary['visualizations'])
   ```
3. Verify file permissions

---

## 📈 Visualization Issues

### Problem: `matplotlib` not creating plots

**Solution:**
```bash
# For headless servers (no display)
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
```

### Problem: Seaborn heatmap is blank

**Solution:**
- Need at least 2 numeric columns for correlation
- Check: `df.select_dtypes(include=[np.number]).columns`
- If < 2 numeric columns, correlation heatmap won't generate

### Problem: Distribution plots are cut off

**Solution:**
```python
# Increase figure size in eda_engine.py
plt.figure(figsize=(14, 10))  # Adjust dimensions
plt.tight_layout()  # Prevent label cutoff
```

---

## 🎯 Streamlit Issues

### Problem: `streamlit: command not found`

**Solution:**
```bash
# Ensure streamlit is installed
pip install streamlit

# Or use python -m
python -m streamlit run streamlit_app.py
```

### Problem: Upload widget not working

**Solution:**
1. Check file size limits in Streamlit config
2. Create `.streamlit/config.toml`:
   ```toml
   [server]
   maxUploadSize = 200
   ```
3. Restart Streamlit

### Problem: Session state errors

**Solution:**
- Clear browser cache
- Restart Streamlit server
- Check for widget key conflicts

---

## 🔧 Analysis Issues

### Problem: Dataset type detection is wrong

**Solution:**
```python
# Override auto-detection
from src.eda_engine import EDAEngine

engine = EDAEngine(df)
engine.dataset_type = 'sales'  # Force specific type
summary = engine.run_full_eda()
```

### Problem: No KPIs extracted

**Solution:**
- Check column names match expected patterns
- View detected columns:
  ```python
  extractor = KPIExtractor(df, 'sales')
  print(extractor._find_column(['revenue', 'sales']))
  ```
- Add custom KPI logic for your domain

### Problem: Missing values warning

**Solution:**
- This is informational, not an error
- Handle missing values before analysis:
  ```python
  # Drop rows with missing values
  df = df.dropna()
  
  # Or fill with defaults
  df = df.fillna(0)
  
  # Or impute
  df['column'] = df['column'].fillna(df['column'].mean())
  ```

---

## 💾 Performance Issues

### Problem: Analysis is very slow

**Solution:**
1. **Sample large datasets:**
   ```python
   df = df.sample(n=10000)  # Random sample
   ```

2. **Skip visualizations:**
   ```python
   # Modify eda_engine.py to skip plot generation
   # Or reduce plot complexity
   ```

3. **Use Polars for large datasets:**
   ```bash
   pip install polars
   ```
   ```python
   import polars as pl
   df = pl.read_csv('large_file.csv')
   df = df.to_pandas()  # Convert to pandas for analysis
   ```

### Problem: Out of memory

**Solution:**
```python
# Use dtypes to reduce memory
df = pd.read_csv('data.csv', dtype={
    'id': 'int32',
    'category': 'category',
    'value': 'float32'
})

# Or load in chunks
chunks = []
for chunk in pd.read_csv('data.csv', chunksize=10000):
    # Process and keep only needed data
    processed = process(chunk)
    chunks.append(processed)
df = pd.concat(chunks)
```

---

## 🐛 Common Errors

### Error: `KeyError: 'dataset_info'`

**Cause:** EDA summary not generated properly

**Solution:**
```python
# Ensure EDA runs successfully
try:
    eda = perform_eda(df)
    print("EDA keys:", eda.keys())
except Exception as e:
    print(f"EDA failed: {e}")
```

### Error: `AttributeError: 'NoneType' object has no attribute`

**Cause:** Dataset or result is None

**Solution:**
```python
# Add validation
if df is None or len(df) == 0:
    raise ValueError("DataFrame is empty")

# Check EDA result
if eda is None:
    raise ValueError("EDA failed to generate results")
```

### Error: `TypeError: Object of type int64 is not JSON serializable`

**Cause:** NumPy types in JSON output

**Solution:**
```python
import json

# Use default=str when saving JSON
json.dump(data, f, indent=2, default=str)

# Or convert explicitly
data = {k: str(v) if isinstance(v, (np.int64, np.float64)) else v 
        for k, v in data.items()}
```

---

## 📞 Getting Help

If you're still experiencing issues:

1. **Check documentation**: `README.md` and `examples/README.md`

2. **Enable verbose mode**:
   ```bash
   python main.py data.csv --verbose
   ```

3. **Check logs**: Look for error messages in terminal output

4. **Minimal reproducible example**:
   ```python
   import pandas as pd
   from src import perform_eda
   
   # Simple test
   df = pd.DataFrame({'A': [1,2,3], 'B': [4,5,6]})
   eda = perform_eda(df)
   print(eda)
   ```

5. **Open an issue on GitHub**:
   - Include Python version
   - Include error traceback
   - Include minimal code to reproduce
   - Include sample data if possible

6. **Community support**:
   - GitHub Discussions
   - Stack Overflow with tag `ai-insight-reporter`

---

## 🔍 Debug Mode

Enable detailed debugging:

```python
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Add debug prints
from src.eda_engine import EDAEngine
engine = EDAEngine(df)
logger.debug(f"Dataset shape: {df.shape}")
logger.debug(f"Columns: {df.columns.tolist()}")
```

---

## ✅ System Check Script

Create `check_system.py`:

```python
#!/usr/bin/env python3
"""System check for AI Insight Reporter"""

import sys
import importlib

def check_python():
    version = sys.version_info
    print(f"Python: {version.major}.{version.minor}.{version.micro}")
    return version.major >= 3 and version.minor >= 10

def check_module(module_name):
    try:
        importlib.import_module(module_name)
        print(f"✓ {module_name}")
        return True
    except ImportError:
        print(f"✗ {module_name} - MISSING")
        return False

print("="*50)
print("AI Insight Reporter - System Check")
print("="*50)

modules = [
    'pandas', 'numpy', 'matplotlib', 'seaborn',
    'reportlab', 'streamlit', 'dotenv'
]

all_ok = check_python()
for module in modules:
    all_ok = check_module(module) and all_ok

print("="*50)
if all_ok:
    print("✅ All checks passed!")
else:
    print("❌ Some checks failed. Run: pip install -r requirements.txt")
```

---

**Still stuck? Contact Rishi Singh via GitHub Issues!**

© 2025 Algorzen Research Division
