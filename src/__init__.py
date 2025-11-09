"""
Eviden Insight Reporter (Created by Algorzen)
Automated Business Intelligence System

Version: 1.0.0
Author: Rishi Singh
"""

__version__ = "1.0.0"
__author__ = "Rishi Singh"
__email__ = "rishi@algorzen.com"
__license__ = "MIT"

from .eda_engine import perform_eda, EDAEngine
from .kpi_extractor import extract_kpis, KPIExtractor
from .ai_narrator import generate_narrative, AINarrator
from .pdf_generator import generate_pdf_report
from .utils import (
    load_dataset,
    save_summary_json,
    format_number,
    format_currency,
    format_percentage,
    validate_dataframe,
    generate_sample_sales_data
)

__all__ = [
    'perform_eda',
    'EDAEngine',
    'extract_kpis',
    'KPIExtractor',
    'generate_narrative',
    'AINarrator',
    'generate_pdf_report',
    'load_dataset',
    'save_summary_json',
    'format_number',
    'format_currency',
    'format_percentage',
    'validate_dataframe',
    'generate_sample_sales_data'
]
