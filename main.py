"""
Main CLI - Command Line Interface for Eviden Insight Reporter
Created by Algorzen

Run automated analysis from the command line.
"""

import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.utils import load_dataset, create_directory_structure
from src.eda_engine import perform_eda
from src.kpi_extractor import extract_kpis
from src.ai_narrator import generate_narrative
from src.pdf_generator import generate_pdf_report


def main():
    """
    Main CLI entry point
    """
    parser = argparse.ArgumentParser(
        description="Eviden Insight Reporter - Automated Business Intelligence (Created by Algorzen)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py data/sample_dataset.csv
  python main.py sales_data.xlsx --author "John Doe"
  python main.py customer_data.csv --api-key sk-xxx --output custom_reports/

© 2025 Algorzen | Developed by Rishi Singh
        """
    )
    
    parser.add_argument(
        'input_file',
        type=str,
        help='Path to input dataset (CSV, Excel, or Parquet)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default='reports',
        help='Output directory for reports (default: reports/)'
    )
    
    parser.add_argument(
        '--author',
        type=str,
    default='Rishi Singh',
    help='Report author name (default: Rishi Singh)'
    )
    
    parser.add_argument(
        '--api-key',
        type=str,
        default=None,
        help='OpenAI API key for GPT-4 narrative generation'
    )
    
    parser.add_argument(
        '--no-pdf',
        action='store_true',
        help='Skip PDF generation (for testing)'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Print detailed progress information'
    )
    
    args = parser.parse_args()
    
    # Setup
    create_directory_structure(Path.cwd())
    
    try:
        # Load dataset
        if args.verbose:
            print(f"📁 Loading dataset from: {args.input_file}")
        
        df = load_dataset(args.input_file)
        
        print(f"✓ Dataset loaded: {len(df):,} rows × {len(df.columns)} columns")
        
        # Perform EDA
        if args.verbose:
            print("🔬 Performing exploratory data analysis...")
        
        eda_summary = perform_eda(df)
        dataset_type = eda_summary['dataset_info']['dataset_type']
        
        print(f"✓ EDA complete. Dataset type: {dataset_type.title()}")
        
        # Extract KPIs
        if args.verbose:
            print("📊 Extracting key performance indicators...")
        
        kpis = extract_kpis(df, dataset_type)
        
        print(f"✓ Extracted {len(kpis)} KPIs")
        
        # Generate narrative
        if args.verbose:
            print("🤖 Generating AI narrative...")
        
        narrative = generate_narrative(eda_summary, kpis, args.api_key)
        
        print(f"✓ Narrative generated using: {narrative['method'].upper()}")
        
        # Generate PDF
        if not args.no_pdf:
            if args.verbose:
                print("📄 Creating PDF report...")
            
            pdf_path = generate_pdf_report(
                eda_summary,
                kpis,
                narrative,
                output_dir=args.output,
                author=args.author
            )
            
            print(f"✓ PDF report saved to: {pdf_path}")
            print(f"✓ Metadata saved to: {Path(args.output) / 'report_metadata.json'}")
        
        print("\n" + "="*60)
        print("🎉 Analysis complete!")
        print("="*60)
        
        # Print summary KPIs
        print("\n📊 KEY PERFORMANCE INDICATORS:\n")
        for key, value in list(kpis.items())[:8]:
            print(f"  • {key}: {value}")
        
        if len(kpis) > 8:
            print(f"  ... and {len(kpis) - 8} more KPIs in the PDF report")
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
