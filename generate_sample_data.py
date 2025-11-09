#!/usr/bin/env python3
"""
Generate Sample Dataset - Quick Data Generator
Eviden (Created by Algorzen)

Generates realistic synthetic datasets for testing and demonstration.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.utils import generate_sample_sales_data
import argparse


def main():
    """Generate sample dataset"""
    parser = argparse.ArgumentParser(
        description="Generate synthetic dataset for testing AI Insight Reporter"
    )
    
    parser.add_argument(
        '--records',
        type=int,
        default=1000,
        help='Number of records to generate (default: 1000)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default='data/sample_dataset.csv',
        help='Output file path (default: data/sample_dataset.csv)'
    )
    
    args = parser.parse_args()
    
    print(f"🔄 Generating {args.records:,} sample records...")
    
    # Generate data
    df = generate_sample_sales_data(args.records)
    
    # Save to file
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    
    print(f"✓ Sample dataset saved to: {output_path}")
    print(f"\n📊 Dataset Summary:")
    print(f"  • Records: {len(df):,}")
    print(f"  • Columns: {len(df.columns)}")
    print(f"  • Columns: {', '.join(df.columns[:5])}...")
    print(f"  • File Size: {output_path.stat().st_size / 1024:.2f} KB")
    print(f"\n🚀 Ready to analyze:")
    print(f"   python main.py {output_path}")


if __name__ == "__main__":
    main()
