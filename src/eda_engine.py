"""
EDA Engine - Automated Exploratory Data Analysis
Eviden (Created by Algorzen)

This module performs comprehensive automated EDA including:
- Dataset type detection
- Missing values analysis
- Statistical summaries
- Correlation analysis
- Distribution visualizations
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import warnings

warnings.filterwarnings('ignore')

# Set professional style
sns.set_style("whitegrid")
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'


class EDAEngine:
    """
    Automated Exploratory Data Analysis Engine
    
    Detects dataset characteristics and generates comprehensive
    statistical analysis and visualizations.
    """
    
    def __init__(self, df: pd.DataFrame, output_dir: str = "reports/assets"):
        """
        Initialize EDA Engine
        
        Args:
            df: Input pandas DataFrame
            output_dir: Directory to save charts and visualizations
        """
        self.df = df
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        self.datetime_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
        
        self.dataset_type = self._detect_dataset_type()
        self.eda_summary = {}
        
    def _detect_dataset_type(self) -> str:
        """
        Detect dataset type based on column names and structure
        
        Returns:
            Dataset type: 'sales', 'finance', 'customer', or 'general'
        """
        cols_lower = [col.lower() for col in self.df.columns]
        
        # Sales indicators
        sales_keywords = ['sales', 'revenue', 'price', 'quantity', 'product', 'order']
        sales_score = sum(any(kw in col for kw in sales_keywords) for col in cols_lower)
        
        # Finance indicators
        finance_keywords = ['balance', 'debit', 'credit', 'transaction', 'account', 'profit', 'margin']
        finance_score = sum(any(kw in col for kw in finance_keywords) for col in cols_lower)
        
        # Customer indicators
        customer_keywords = ['customer', 'churn', 'retention', 'lifetime', 'segment', 'age']
        customer_score = sum(any(kw in col for kw in customer_keywords) for col in cols_lower)
        
        scores = {
            'sales': sales_score,
            'finance': finance_score,
            'customer': customer_score
        }
        
        max_score = max(scores.values())
        if max_score >= 2:
            return max(scores, key=scores.get)
        return 'general'
    
    def analyze_missing_values(self) -> Dict:
        """
        Analyze missing values across all columns
        
        Returns:
            Dictionary with missing value statistics
        """
        missing = self.df.isnull().sum()
        missing_pct = (missing / len(self.df)) * 100
        
        missing_df = pd.DataFrame({
            'Missing_Count': missing,
            'Missing_Percentage': missing_pct
        })
        missing_df = missing_df[missing_df['Missing_Count'] > 0].sort_values(
            'Missing_Percentage', ascending=False
        )
        
        return {
            'total_missing': int(missing.sum()),
            'columns_with_missing': len(missing_df),
            'missing_details': missing_df.to_dict('index') if len(missing_df) > 0 else {}
        }
    
    def get_column_statistics(self) -> Dict:
        """
        Generate comprehensive column statistics
        
        Returns:
            Dictionary with numeric and categorical statistics
        """
        stats = {
            'numeric': {},
            'categorical': {},
            'datetime': {}
        }
        
        # Numeric statistics
        if self.numeric_cols:
            numeric_stats = self.df[self.numeric_cols].describe().T
            stats['numeric'] = numeric_stats.to_dict('index')
        
        # Categorical statistics
        for col in self.categorical_cols[:10]:  # Limit to top 10
            stats['categorical'][col] = {
                'unique_values': int(self.df[col].nunique()),
                'top_value': str(self.df[col].mode()[0]) if len(self.df[col].mode()) > 0 else 'N/A',
                'top_frequency': int(self.df[col].value_counts().iloc[0]) if len(self.df[col]) > 0 else 0
            }
        
        # DateTime statistics
        for col in self.datetime_cols:
            stats['datetime'][col] = {
                'min_date': str(self.df[col].min()),
                'max_date': str(self.df[col].max()),
                'date_range_days': (self.df[col].max() - self.df[col].min()).days
            }
        
        return stats
    
    def generate_correlation_heatmap(self) -> Optional[str]:
        """
        Generate correlation heatmap for numeric columns
        
        Returns:
            Path to saved heatmap image, or None if insufficient numeric columns
        """
        if len(self.numeric_cols) < 2:
            return None
        
        plt.figure(figsize=(12, 10))
        
        # Calculate correlation matrix
        corr_matrix = self.df[self.numeric_cols].corr()
        
        # Create mask for upper triangle
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        
        # Generate heatmap
        sns.heatmap(
            corr_matrix,
            mask=mask,
            annot=True,
            fmt='.2f',
            cmap='coolwarm',
            center=0,
            square=True,
            linewidths=1,
            cbar_kws={"shrink": 0.8}
        )
        
    plt.title('Correlation Matrix - Eviden Analysis', fontsize=16, fontweight='bold', pad=20)
        plt.tight_layout()
        
        output_path = self.output_dir / "correlation_heatmap.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(output_path)
    
    def generate_distribution_plots(self) -> Dict[str, str]:
        """
        Generate distribution plots for top numeric and categorical columns
        
        Returns:
            Dictionary mapping plot type to file path
        """
        plots = {}
        
        # Top 4 numeric distributions
        if self.numeric_cols:
            top_numeric = self.numeric_cols[:4]
            fig, axes = plt.subplots(2, 2, figsize=(14, 10))
            axes = axes.flatten()
            
            for idx, col in enumerate(top_numeric):
                if idx < len(axes):
                    axes[idx].hist(
                        self.df[col].dropna(),
                        bins=30,
                        color='#2E86AB',
                        alpha=0.7,
                        edgecolor='black'
                    )
                    axes[idx].set_title(f'{col} Distribution', fontweight='bold')
                    axes[idx].set_xlabel(col)
                    axes[idx].set_ylabel('Frequency')
                    axes[idx].grid(alpha=0.3)
            
            # Hide unused subplots
            for idx in range(len(top_numeric), len(axes)):
                axes[idx].axis('off')
            
            plt.suptitle('Numeric Distributions - Eviden Analysis', 
                        fontsize=16, fontweight='bold', y=1.00)
            plt.tight_layout()
            
            numeric_path = self.output_dir / "numeric_distributions.png"
            plt.savefig(numeric_path, dpi=300, bbox_inches='tight')
            plt.close()
            plots['numeric'] = str(numeric_path)
        
        # Top 4 categorical distributions
        if self.categorical_cols:
            # Select columns with reasonable number of categories
            valid_cats = [col for col in self.categorical_cols 
                         if self.df[col].nunique() <= 20][:4]
            
            if valid_cats:
                fig, axes = plt.subplots(2, 2, figsize=(14, 10))
                axes = axes.flatten()
                
                for idx, col in enumerate(valid_cats):
                    if idx < len(axes):
                        top_values = self.df[col].value_counts().head(10)
                        axes[idx].barh(
                            range(len(top_values)),
                            top_values.values,
                            color='#A23B72',
                            alpha=0.7
                        )
                        axes[idx].set_yticks(range(len(top_values)))
                        axes[idx].set_yticklabels(top_values.index)
                        axes[idx].set_title(f'{col} Distribution', fontweight='bold')
                        axes[idx].set_xlabel('Count')
                        axes[idx].grid(alpha=0.3)
                
                # Hide unused subplots
                for idx in range(len(valid_cats), len(axes)):
                    axes[idx].axis('off')
                
                plt.suptitle('Categorical Distributions - Eviden Analysis', 
                            fontsize=16, fontweight='bold', y=1.00)
                plt.tight_layout()
                
                cat_path = self.output_dir / "categorical_distributions.png"
                plt.savefig(cat_path, dpi=300, bbox_inches='tight')
                plt.close()
                plots['categorical'] = str(cat_path)
        
        return plots
    
    def run_full_eda(self) -> Dict:
        """
        Execute complete EDA pipeline
        
        Returns:
            Comprehensive EDA summary dictionary
        """
        summary = {
            'dataset_info': {
                'rows': len(self.df),
                'columns': len(self.df.columns),
                'dataset_type': self.dataset_type,
                'numeric_columns': len(self.numeric_cols),
                'categorical_columns': len(self.categorical_cols),
                'datetime_columns': len(self.datetime_cols)
            },
            'missing_values': self.analyze_missing_values(),
            'statistics': self.get_column_statistics(),
            'visualizations': {
                'correlation_heatmap': self.generate_correlation_heatmap(),
                'distributions': self.generate_distribution_plots()
            }
        }
        
        self.eda_summary = summary
        return summary


def perform_eda(df: pd.DataFrame, output_dir: str = "reports/assets") -> Dict:
    """
    Convenience function to perform full EDA
    
    Args:
        df: Input DataFrame
        output_dir: Output directory for visualizations
        
    Returns:
        EDA summary dictionary
    """
    engine = EDAEngine(df, output_dir)
    return engine.run_full_eda()
