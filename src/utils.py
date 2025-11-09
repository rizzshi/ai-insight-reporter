"""
Utility Functions - Helper functions for AI Insight Reporter
Algorzen Research Division

Common utility functions used across the application.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional, Union
import json


def load_dataset(file_path: Union[str, Path]) -> pd.DataFrame:
    """
    Load dataset from various file formats
    
    Args:
        file_path: Path to dataset file
        
    Returns:
        Loaded pandas DataFrame
        
    Raises:
        ValueError: If file format is unsupported
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    extension = file_path.suffix.lower()
    
    if extension == '.csv':
        return pd.read_csv(file_path)
    elif extension in ['.xlsx', '.xls']:
        return pd.read_excel(file_path)
    elif extension == '.parquet':
        return pd.read_parquet(file_path)
    elif extension == '.json':
        return pd.read_json(file_path)
    else:
        raise ValueError(f"Unsupported file format: {extension}")


def save_summary_json(summary: dict, output_path: Union[str, Path]):
    """
    Save analysis summary to JSON file
    
    Args:
        summary: Summary dictionary to save
        output_path: Output file path
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(summary, f, indent=2, default=str)


def format_number(value: Union[int, float], decimals: int = 2) -> str:
    """
    Format number with thousands separator
    
    Args:
        value: Number to format
        decimals: Number of decimal places
        
    Returns:
        Formatted string
    """
    if isinstance(value, int):
        return f"{value:,}"
    else:
        return f"{value:,.{decimals}f}"


def format_currency(value: Union[int, float], symbol: str = "$") -> str:
    """
    Format value as currency
    
    Args:
        value: Value to format
        symbol: Currency symbol
        
    Returns:
        Formatted currency string
    """
    return f"{symbol}{value:,.2f}"


def format_percentage(value: float, decimals: int = 2) -> str:
    """
    Format value as percentage
    
    Args:
        value: Value to format (0-100 or 0-1)
        decimals: Number of decimal places
        
    Returns:
        Formatted percentage string
    """
    if value <= 1:
        value = value * 100
    return f"{value:.{decimals}f}%"


def create_directory_structure(base_path: Union[str, Path]):
    """
    Create standard directory structure for the project
    
    Args:
        base_path: Base directory path
    """
    base_path = Path(base_path)
    
    directories = [
        base_path / "data",
        base_path / "reports",
        base_path / "reports" / "assets",
        base_path / "src"
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


def validate_dataframe(df: pd.DataFrame) -> dict:
    """
    Validate DataFrame and return quality metrics
    
    Args:
        df: DataFrame to validate
        
    Returns:
        Dictionary with validation results
    """
    if df is None or len(df) == 0:
        return {
            'valid': False,
            'error': 'DataFrame is empty'
        }
    
    total_cells = len(df) * len(df.columns)
    missing_cells = df.isnull().sum().sum()
    
    return {
        'valid': True,
        'rows': len(df),
        'columns': len(df.columns),
        'total_cells': total_cells,
        'missing_cells': int(missing_cells),
        'completeness_pct': ((total_cells - missing_cells) / total_cells) * 100,
        'memory_mb': df.memory_usage(deep=True).sum() / 1024 / 1024
    }


def get_column_info(df: pd.DataFrame) -> dict:
    """
    Get detailed information about DataFrame columns
    
    Args:
        df: Input DataFrame
        
    Returns:
        Dictionary with column information
    """
    info = {
        'numeric': [],
        'categorical': [],
        'datetime': [],
        'boolean': []
    }
    
    for col in df.columns:
        dtype = df[col].dtype
        
        if pd.api.types.is_numeric_dtype(dtype):
            info['numeric'].append({
                'name': col,
                'dtype': str(dtype),
                'unique': int(df[col].nunique()),
                'missing': int(df[col].isnull().sum())
            })
        elif pd.api.types.is_datetime64_any_dtype(dtype):
            info['datetime'].append({
                'name': col,
                'dtype': str(dtype),
                'min': str(df[col].min()),
                'max': str(df[col].max()),
                'missing': int(df[col].isnull().sum())
            })
        elif pd.api.types.is_bool_dtype(dtype):
            info['boolean'].append({
                'name': col,
                'dtype': str(dtype),
                'true_count': int(df[col].sum()),
                'false_count': int((~df[col]).sum()),
                'missing': int(df[col].isnull().sum())
            })
        else:
            info['categorical'].append({
                'name': col,
                'dtype': str(dtype),
                'unique': int(df[col].nunique()),
                'missing': int(df[col].isnull().sum())
            })
    
    return info


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and standardize column names
    
    Args:
        df: Input DataFrame
        
    Returns:
        DataFrame with cleaned column names
    """
    df = df.copy()
    
    # Replace spaces with underscores
    df.columns = df.columns.str.replace(' ', '_')
    
    # Remove special characters
    df.columns = df.columns.str.replace('[^A-Za-z0-9_]', '', regex=True)
    
    # Convert to lowercase
    df.columns = df.columns.str.lower()
    
    return df


def generate_sample_sales_data(n_records: int = 1000) -> pd.DataFrame:
    """
    Generate synthetic sales dataset for testing
    
    Args:
        n_records: Number of records to generate
        
    Returns:
        DataFrame with synthetic sales data
    """
    np.random.seed(42)
    
    products = ['Laptop', 'Phone', 'Tablet', 'Monitor', 'Keyboard', 'Mouse', 'Headphones', 'Webcam']
    regions = ['North', 'South', 'East', 'West', 'Central']
    channels = ['Online', 'Retail', 'Wholesale', 'Partner']
    
    data = {
        'transaction_id': [f'TXN-{i:06d}' for i in range(1, n_records + 1)],
        'date': pd.date_range(start='2024-01-01', periods=n_records, freq='4H'),
        'product': np.random.choice(products, n_records),
        'category': np.random.choice(['Electronics', 'Accessories', 'Peripherals'], n_records),
        'region': np.random.choice(regions, n_records),
        'channel': np.random.choice(channels, n_records),
        'quantity': np.random.randint(1, 50, n_records),
        'unit_price': np.random.uniform(10, 2000, n_records).round(2),
        'discount_pct': np.random.uniform(0, 25, n_records).round(2),
        'customer_id': [f'CUST-{np.random.randint(1, 500):04d}' for _ in range(n_records)]
    }
    
    df = pd.DataFrame(data)
    
    # Calculate derived fields
    df['subtotal'] = (df['quantity'] * df['unit_price']).round(2)
    df['discount_amount'] = (df['subtotal'] * df['discount_pct'] / 100).round(2)
    df['total_revenue'] = (df['subtotal'] - df['discount_amount']).round(2)
    df['profit_margin'] = np.random.uniform(10, 40, n_records).round(2)
    
    # Add some missing values randomly
    missing_indices = np.random.choice(df.index, size=int(n_records * 0.02), replace=False)
    df.loc[missing_indices, 'discount_pct'] = np.nan
    
    return df


if __name__ == "__main__":
    # Generate sample dataset when run directly
    print("Generating sample sales dataset...")
    df = generate_sample_sales_data(1000)
    
    output_path = Path(__file__).parent.parent / "data" / "sample_dataset.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    df.to_csv(output_path, index=False)
    print(f"✓ Sample dataset saved to: {output_path}")
    print(f"  Rows: {len(df):,}")
    print(f"  Columns: {len(df.columns)}")
    print(f"  Size: {output_path.stat().st_size / 1024:.2f} KB")
