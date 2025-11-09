# 🏗️ System Architecture - AI Insight Reporter

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                     AI INSIGHT REPORTER SYSTEM                       │
│                    Algorzen Research Division                        │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACES                              │
├──────────────────────────┬──────────────────────────────────────────┤
│   🌐 Streamlit Web UI   │       💻 Command Line Interface         │
│   • File upload          │       • Script automation               │
│   • Interactive preview  │       • Batch processing                │
│   • Report download      │       • CI/CD integration               │
└──────────────────────────┴──────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│                        CORE ENGINE LAYER                             │
├─────────────────┬──────────────────┬────────────────┬──────────────┤
│  📊 EDA Engine  │  🎯 KPI Extract  │  🤖 AI Narrator │ 📄 PDF Gen   │
│                 │                  │                 │              │
│  • Detect type  │  • Sales KPIs    │  • GPT-4 API   │ • Branding   │
│  • Statistics   │  • Finance KPIs  │  • Fallback    │ • Layout     │
│  • Missing vals │  • Customer KPIs │  • Executive   │ • Charts     │
│  • Correlation  │  • General KPIs  │  • Insights    │ • Metadata   │
│  • Visualize    │  • Smart detect  │  • Recommend   │ • Export     │
└─────────────────┴──────────────────┴────────────────┴──────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│                      UTILITIES & HELPERS                             │
├─────────────────────────────────────────────────────────────────────┤
│  • Data loading (CSV, Excel, Parquet)                               │
│  • Format helpers (currency, percentage)                            │
│  • Validation & quality checks                                      │
│  • Sample data generation                                           │
│  • Directory management                                             │
└─────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│                        EXTERNAL SERVICES                             │
├──────────────────────────┬──────────────────────────────────────────┤
│    🔌 OpenAI GPT-4 API   │         📦 Python Libraries             │
│    • Narrative generation│         • Pandas, NumPy                 │
│    • Executive insights  │         • Matplotlib, Seaborn           │
│    • Optional service    │         • ReportLab, Streamlit          │
└──────────────────────────┴──────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────┐
│                            OUTPUTS                                   │
├──────────────────────┬──────────────────────┬─────────────────────┤
│   📄 PDF Reports     │   📊 Visualizations  │   📋 Metadata       │
│   • Executive format │   • Heatmaps         │   • JSON format     │
│   • Branded layout   │   • Distributions    │   • Traceability    │
│   • Multi-page       │   • High-res charts  │   • Audit trail     │
└──────────────────────┴──────────────────────┴─────────────────────┘
```

---

## Data Flow Diagram

```
┌─────────────┐
│  Input Data │
│ (CSV/Excel) │
└──────┬──────┘
       │
       ↓
┌─────────────────────────────────────┐
│      1. LOAD & VALIDATE             │
│  • Read file format                 │
│  • Validate structure               │
│  • Check data quality               │
└──────────────┬──────────────────────┘
               │
               ↓
┌─────────────────────────────────────┐
│     2. EXPLORATORY ANALYSIS         │
│  • Detect dataset type              │
│  • Calculate statistics             │
│  • Identify missing values          │
│  • Generate correlations            │
└──────────────┬──────────────────────┘
               │
               ├──────────┐
               │          │
               ↓          ↓
     ┌─────────────┐  ┌─────────────┐
     │3a. VISUALIZE│  │3b. EXTRACT  │
     │             │  │    KPIs     │
     │• Heatmaps   │  │             │
     │• Distrib.   │  │• Sales      │
     │• Charts     │  │• Finance    │
     └──────┬──────┘  │• Customer   │
            │         └──────┬──────┘
            │                │
            └────────┬───────┘
                     │
                     ↓
           ┌─────────────────┐
           │ 4. AI NARRATIVE │
           │                 │
           │ GPT-4? ┌──Yes──→ OpenAI API
           │        │         │
           │        └──No───→ Fallback
           │                 │
           └────────┬────────┘
                    │
                    ↓
           ┌─────────────────┐
           │ 5. PDF ASSEMBLY │
           │                 │
           │• Title page     │
           │• KPI tables     │
           │• Narratives     │
           │• Charts         │
           │• Branding       │
           └────────┬────────┘
                    │
                    ↓
           ┌─────────────────┐
           │   6. OUTPUT     │
           │                 │
           │• PDF Report     │
           │• Metadata JSON  │
           │• Chart files    │
           └─────────────────┘
```

---

## Component Interaction

```
┌────────────────────────────────────────────────────────────────┐
│                    Component Dependencies                       │
└────────────────────────────────────────────────────────────────┘

main.py / streamlit_app.py
    │
    ├─→ utils.py (load_dataset)
    │
    ├─→ eda_engine.py (perform_eda)
    │       │
    │       └─→ Generates visualizations
    │
    ├─→ kpi_extractor.py (extract_kpis)
    │       │
    │       └─→ Uses dataset_type from EDA
    │
    ├─→ ai_narrator.py (generate_narrative)
    │       │
    │       ├─→ OpenAI API (optional)
    │       └─→ Fallback generator
    │
    └─→ pdf_generator.py (generate_pdf_report)
            │
            ├─→ Embeds charts from EDA
            ├─→ Formats KPIs
            ├─→ Includes narrative
            └─→ Adds branding
```

---

## File Organization

```
AiInsight/
│
├─ 📱 INTERFACES
│   ├─ main.py                    # CLI application
│   └─ streamlit_app.py           # Web UI application
│
├─ 🧠 CORE LOGIC (src/)
│   ├─ eda_engine.py              # Analysis engine
│   ├─ kpi_extractor.py           # Metrics calculator
│   ├─ ai_narrator.py             # Narrative generator
│   ├─ pdf_generator.py           # Report builder
│   ├─ utils.py                   # Helper functions
│   └─ __init__.py                # Package exports
│
├─ 📊 DATA
│   ├─ data/                      # Input datasets
│   │   └─ sample_dataset.csv
│   └─ reports/                   # Output reports
│       ├─ assets/                # Generated charts
│       ├─ *.pdf                  # PDF reports
│       └─ report_metadata.json
│
├─ 📚 DOCUMENTATION
│   ├─ README.md                  # Main documentation
│   ├─ GETTING_STARTED.md         # Setup guide
│   ├─ QUICK_REFERENCE.md         # Command reference
│   ├─ TROUBLESHOOTING.md         # Issue resolution
│   ├─ CONTRIBUTING.md            # Contribution guide
│   ├─ ARCHITECTURE.md            # This file
│   └─ PROJECT_SUMMARY.md         # Project overview
│
├─ 🎯 EXAMPLES
│   └─ examples/
│       └─ README.md              # Usage examples
│
├─ ⚙️ CONFIGURATION
│   ├─ requirements.txt           # Dependencies
│   ├─ .env.example               # Config template
│   ├─ .gitignore                 # Git ignore rules
│   └─ .vscode/                   # IDE settings
│
├─ 🛠️ UTILITIES
│   ├─ setup.py                   # Setup wizard
│   └─ generate_sample_data.py    # Data generator
│
└─ 📄 PROJECT META
    ├─ LICENSE                    # MIT License
    └─ PROJECT_SUMMARY.md         # Status summary
```

---

## Technology Stack

```
┌─────────────────────────────────────────────────────────────┐
│                     TECHNOLOGY LAYERS                        │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  PRESENTATION LAYER                                          │
│  • Streamlit (Web UI)                                        │
│  • argparse (CLI)                                            │
│  • ReportLab (PDF)                                           │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│  APPLICATION LAYER                                           │
│  • Python 3.10+                                              │
│  • Custom modules (src/)                                     │
│  • Modular architecture                                      │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│  DATA PROCESSING LAYER                                       │
│  • Pandas (DataFrames)                                       │
│  • NumPy (Numerical)                                         │
│  • SciPy (Statistics)                                        │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│  VISUALIZATION LAYER                                         │
│  • Matplotlib (Plotting)                                     │
│  • Seaborn (Statistical plots)                               │
│  • Pillow (Image processing)                                 │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│  AI/ML LAYER                                                 │
│  • OpenAI API (GPT-4)                                        │
│  • Rule-based fallback                                       │
└─────────────────────────────────────────────────────────────┘
```

---

## Processing Pipeline

```
INPUT → VALIDATE → ANALYZE → VISUALIZE → NARRATE → REPORT → OUTPUT

Where:
• INPUT      = Load CSV/Excel/Parquet file
• VALIDATE   = Check structure, quality, completeness
• ANALYZE    = EDA + Statistics + KPIs
• VISUALIZE  = Heatmaps + Distributions
• NARRATE    = GPT-4 or Fallback narrative
• REPORT     = Assemble PDF with branding
• OUTPUT     = Save PDF + Metadata + Charts
```

---

## Scalability Considerations

### Current Design (Single Machine)
```
Dataset Size Support:
• Small (<10k rows)     → Excellent performance
• Medium (10k-100k)     → Good performance
• Large (100k-1M)       → Acceptable with sampling
• Very Large (>1M)      → Requires optimization
```

### Future Scalability Options
```
┌──────────────────────────────────────┐
│   Horizontal Scaling Options         │
├──────────────────────────────────────┤
│  1. Batch Processing                 │
│     • Process multiple files         │
│     • Queue-based architecture       │
│                                      │
│  2. Distributed Computing            │
│     • Apache Spark integration       │
│     • Dask for parallel processing   │
│                                      │
│  3. Cloud Deployment                 │
│     • AWS Lambda (serverless)        │
│     • Docker containers              │
│     • Kubernetes orchestration       │
│                                      │
│  4. Database Integration             │
│     • PostgreSQL connector           │
│     • BigQuery support               │
│     • Real-time data streams         │
└──────────────────────────────────────┘
```

---

## Security Architecture

```
┌────────────────────────────────────────┐
│        Security Measures               │
├────────────────────────────────────────┤
│  • API keys in .env (not committed)    │
│  • Input validation on all data        │
│  • No code execution from data         │
│  • Sandboxed file operations           │
│  • HTTPS for API communication         │
│  • No sensitive data in logs           │
└────────────────────────────────────────┘
```

---

## Error Handling Strategy

```
┌───────────────────────────────────────────────┐
│           Error Handling Flow                 │
└───────────────────────────────────────────────┘

User Input
    │
    ↓
[Try] Load Data
    │
    ├─[Success]──→ Continue
    │
    └─[Fail]─────→ Log error
                   Show user-friendly message
                   Suggest solutions

[Try] Perform EDA
    │
    ├─[Success]──→ Continue
    │
    └─[Fail]─────→ Use safe defaults
                   Log warning
                   Continue with partial results

[Try] GPT-4 Narrative
    │
    ├─[Success]──→ Use GPT-4 output
    │
    └─[Fail]─────→ Automatic fallback
                   No user intervention needed

[Try] Generate PDF
    │
    ├─[Success]──→ Return PDF path
    │
    └─[Fail]─────→ Log error
                   Save raw results
                   Notify user
```

---

## Extension Points

### Areas Designed for Extension

1. **Dataset Type Detection**
   - Add new type in `eda_engine.py`
   - Add KPIs in `kpi_extractor.py`
   - Add narrative templates in `ai_narrator.py`

2. **KPI Calculation**
   - Extend `KPIExtractor` class
   - Add domain-specific metrics
   - Custom aggregations

3. **Visualizations**
   - Add methods to `EDAEngine`
   - Custom plot types
   - Interactive charts

4. **Report Templates**
   - Customize `pdf_generator.py`
   - New branding themes
   - Custom layouts

5. **Data Sources**
   - Add loaders in `utils.py`
   - Database connectors
   - API integrations

---

## Performance Optimization

```
Current Optimizations:
✓ Efficient pandas operations
✓ Vectorized NumPy calculations
✓ Lazy evaluation where possible
✓ Matplotlib backend optimization
✓ ReportLab caching

Future Optimizations:
○ Polars for large datasets
○ Multiprocessing for batch jobs
○ Caching of repeated operations
○ Progressive PDF rendering
○ Async API calls
```

---

## Deployment Options

```
┌─────────────────────────────────────────┐
│         Deployment Patterns              │
├─────────────────────────────────────────┤
│  1. Local Development                   │
│     python main.py data.csv             │
│                                         │
│  2. Web Service                         │
│     streamlit run streamlit_app.py      │
│     (Deploy on Streamlit Cloud)         │
│                                         │
│  3. Docker Container                    │
│     docker build -t ai-insight .        │
│     docker run -p 8501:8501 ai-insight  │
│                                         │
│  4. Serverless Function                 │
│     AWS Lambda + API Gateway            │
│     Triggered by S3 uploads             │
│                                         │
│  5. Scheduled Job                       │
│     Cron job / Task Scheduler           │
│     Automated daily reports             │
└─────────────────────────────────────────┘
```

---

## System Requirements

```
Minimum:
• Python 3.10+
• 2 GB RAM
• 500 MB disk space
• Internet (for GPT-4 only)

Recommended:
• Python 3.11+
• 4 GB RAM
• 2 GB disk space
• SSD for better I/O
• Internet connection
```

---

**Architecture designed for extensibility, maintainability, and performance.**

Built with ❤️ by Algorzen Research Division

© 2025 Algorzen Research | Om Singh
