"""
KPI Extractor - Automatic Key Performance Indicator Calculation
Algorzen Research Division

This module automatically detects and calculates relevant KPIs
based on the dataset type and available columns.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional


class KPIExtractor:
    """
    Automated KPI extraction engine
    
    Intelligently identifies and calculates business metrics
    based on dataset characteristics.
    """
    
    def __init__(self, df: pd.DataFrame, dataset_type: str = 'general'):
        """
        Initialize KPI Extractor
        
        Args:
            df: Input pandas DataFrame
            dataset_type: Type of dataset ('sales', 'finance', 'customer', 'general')
        """
        self.df = df
        self.dataset_type = dataset_type
        self.kpis = {}
        
    def _find_column(self, keywords: List[str]) -> Optional[str]:
        """
        Find column matching any of the keywords (case-insensitive)
        
        Args:
            keywords: List of keyword patterns to search
            
        Returns:
            Matched column name or None
        """
        cols_lower = {col.lower(): col for col in self.df.columns}
        for keyword in keywords:
            for col_lower, col_original in cols_lower.items():
                if keyword in col_lower:
                    return col_original
        return None
    
    def extract_sales_kpis(self) -> Dict:
        """
        Extract sales-specific KPIs
        
        Returns:
            Dictionary of sales KPIs
        """
        kpis = {}
        
        # Find relevant columns
        revenue_col = self._find_column(['revenue', 'sales', 'total', 'amount'])
        quantity_col = self._find_column(['quantity', 'qty', 'units'])
        product_col = self._find_column(['product', 'item', 'sku'])
        margin_col = self._find_column(['margin', 'profit'])
        date_col = self._find_column(['date', 'time', 'timestamp'])
        
        # Total Revenue/Sales
        if revenue_col and pd.api.types.is_numeric_dtype(self.df[revenue_col]):
            kpis['Total Revenue'] = f"${self.df[revenue_col].sum():,.2f}"
            kpis['Average Order Value'] = f"${self.df[revenue_col].mean():,.2f}"
            kpis['Revenue Std Dev'] = f"${self.df[revenue_col].std():,.2f}"
        
        # Quantity Metrics
        if quantity_col and pd.api.types.is_numeric_dtype(self.df[quantity_col]):
            kpis['Total Units Sold'] = f"{self.df[quantity_col].sum():,.0f}"
            kpis['Avg Units per Transaction'] = f"{self.df[quantity_col].mean():.2f}"
        
        # Product Metrics
        if product_col:
            kpis['Unique Products'] = f"{self.df[product_col].nunique():,}"
            top_product = self.df[product_col].value_counts().iloc[0]
            top_product_name = self.df[product_col].value_counts().index[0]
            kpis['Top Product'] = f"{top_product_name} ({top_product} sales)"
        
        # Profit Margin
        if margin_col and pd.api.types.is_numeric_dtype(self.df[margin_col]):
            kpis['Average Margin'] = f"{self.df[margin_col].mean():.2f}%"
            kpis['Margin Range'] = f"{self.df[margin_col].min():.2f}% - {self.df[margin_col].max():.2f}%"
        
        # Time-based metrics
        if date_col and pd.api.types.is_datetime64_any_dtype(self.df[date_col]):
            date_range = (self.df[date_col].max() - self.df[date_col].min()).days
            kpis['Data Period'] = f"{date_range} days"
            if date_range > 0:
                kpis['Avg Transactions per Day'] = f"{len(self.df) / date_range:.2f}"
        
        return kpis
    
    def extract_finance_kpis(self) -> Dict:
        """
        Extract finance-specific KPIs
        
        Returns:
            Dictionary of finance KPIs
        """
        kpis = {}
        
        # Find relevant columns
        balance_col = self._find_column(['balance', 'amount', 'value'])
        debit_col = self._find_column(['debit', 'expense', 'withdrawal'])
        credit_col = self._find_column(['credit', 'income', 'deposit'])
        account_col = self._find_column(['account', 'customer', 'id'])
        transaction_col = self._find_column(['transaction', 'type', 'category'])
        
        # Balance metrics
        if balance_col and pd.api.types.is_numeric_dtype(self.df[balance_col]):
            kpis['Total Balance'] = f"${self.df[balance_col].sum():,.2f}"
            kpis['Average Balance'] = f"${self.df[balance_col].mean():,.2f}"
            kpis['Median Balance'] = f"${self.df[balance_col].median():,.2f}"
        
        # Debit/Credit analysis
        if debit_col and pd.api.types.is_numeric_dtype(self.df[debit_col]):
            kpis['Total Debits'] = f"${self.df[debit_col].sum():,.2f}"
            kpis['Average Debit'] = f"${self.df[debit_col].mean():,.2f}"
        
        if credit_col and pd.api.types.is_numeric_dtype(self.df[credit_col]):
            kpis['Total Credits'] = f"${self.df[credit_col].sum():,.2f}"
            kpis['Average Credit'] = f"${self.df[credit_col].mean():,.2f}"
        
        # Net position
        if debit_col and credit_col:
            net_position = self.df[credit_col].sum() - self.df[debit_col].sum()
            kpis['Net Position'] = f"${net_position:,.2f}"
        
        # Account metrics
        if account_col:
            kpis['Total Accounts'] = f"{self.df[account_col].nunique():,}"
        
        # Transaction types
        if transaction_col:
            kpis['Transaction Types'] = f"{self.df[transaction_col].nunique()}"
            top_transaction = self.df[transaction_col].value_counts().index[0]
            kpis['Most Common Transaction'] = str(top_transaction)
        
        return kpis
    
    def extract_customer_kpis(self) -> Dict:
        """
        Extract customer-specific KPIs
        
        Returns:
            Dictionary of customer KPIs
        """
        kpis = {}
        
        # Find relevant columns
        customer_col = self._find_column(['customer', 'user', 'client', 'id'])
        churn_col = self._find_column(['churn', 'churned', 'status'])
        age_col = self._find_column(['age', 'tenure', 'duration'])
        segment_col = self._find_column(['segment', 'category', 'tier', 'group'])
        value_col = self._find_column(['value', 'ltv', 'lifetime', 'revenue'])
        
        # Customer count
        if customer_col:
            kpis['Total Customers'] = f"{self.df[customer_col].nunique():,}"
        
        # Churn analysis
        if churn_col:
            if pd.api.types.is_numeric_dtype(self.df[churn_col]):
                churn_rate = (self.df[churn_col].sum() / len(self.df)) * 100
            else:
                # Assume binary (Yes/No, True/False, 1/0)
                churned_count = self.df[churn_col].astype(str).str.lower().isin(['yes', 'true', '1', 'churned']).sum()
                churn_rate = (churned_count / len(self.df)) * 100
            
            kpis['Churn Rate'] = f"{churn_rate:.2f}%"
            kpis['Retention Rate'] = f"{100 - churn_rate:.2f}%"
        
        # Age/Tenure metrics
        if age_col and pd.api.types.is_numeric_dtype(self.df[age_col]):
            kpis['Average Age/Tenure'] = f"{self.df[age_col].mean():.1f}"
            kpis['Age/Tenure Range'] = f"{self.df[age_col].min():.0f} - {self.df[age_col].max():.0f}"
        
        # Segmentation
        if segment_col:
            kpis['Customer Segments'] = f"{self.df[segment_col].nunique()}"
            top_segment = self.df[segment_col].value_counts().index[0]
            top_segment_pct = (self.df[segment_col].value_counts().iloc[0] / len(self.df)) * 100
            kpis['Largest Segment'] = f"{top_segment} ({top_segment_pct:.1f}%)"
        
        # Customer value
        if value_col and pd.api.types.is_numeric_dtype(self.df[value_col]):
            kpis['Avg Customer Value'] = f"${self.df[value_col].mean():,.2f}"
            kpis['Total Customer Value'] = f"${self.df[value_col].sum():,.2f}"
            kpis['Median Customer Value'] = f"${self.df[value_col].median():,.2f}"
        
        return kpis
    
    def extract_general_kpis(self) -> Dict:
        """
        Extract general dataset KPIs
        
        Returns:
            Dictionary of general KPIs
        """
        kpis = {}
        
        # Basic dataset info
        kpis['Total Records'] = f"{len(self.df):,}"
        kpis['Total Columns'] = f"{len(self.df.columns)}"
        
        # Missing data
        total_cells = len(self.df) * len(self.df.columns)
        missing_cells = self.df.isnull().sum().sum()
        completeness = ((total_cells - missing_cells) / total_cells) * 100
        kpis['Data Completeness'] = f"{completeness:.2f}%"
        
        # Numeric column summary
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            # Find column with highest mean
            means = self.df[numeric_cols].mean()
            top_numeric = means.idxmax()
            kpis[f'Highest Avg ({top_numeric})'] = f"{means[top_numeric]:,.2f}"
        
        # Categorical diversity
        categorical_cols = self.df.select_dtypes(include=['object', 'category']).columns
        if len(categorical_cols) > 0:
            diversity_scores = {col: self.df[col].nunique() / len(self.df) 
                              for col in categorical_cols}
            most_diverse = max(diversity_scores, key=diversity_scores.get)
            kpis['Most Diverse Column'] = f"{most_diverse} ({self.df[most_diverse].nunique()} unique)"
        
        return kpis
    
    def extract_all_kpis(self) -> Dict:
        """
        Extract all relevant KPIs based on dataset type
        
        Returns:
            Comprehensive KPI dictionary
        """
        if self.dataset_type == 'sales':
            self.kpis = self.extract_sales_kpis()
        elif self.dataset_type == 'finance':
            self.kpis = self.extract_finance_kpis()
        elif self.dataset_type == 'customer':
            self.kpis = self.extract_customer_kpis()
        else:
            self.kpis = self.extract_general_kpis()
        
        # Always add data quality metrics
        self.kpis['Dataset Type'] = self.dataset_type.title()
        
        return self.kpis


def extract_kpis(df: pd.DataFrame, dataset_type: str = 'general') -> Dict:
    """
    Convenience function to extract KPIs
    
    Args:
        df: Input DataFrame
        dataset_type: Type of dataset
        
    Returns:
        KPI dictionary
    """
    extractor = KPIExtractor(df, dataset_type)
    return extractor.extract_all_kpis()
