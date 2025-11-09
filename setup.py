#!/usr/bin/env python3
"""
Quick Setup Script for AI Insight Reporter
Algorzen Research Division

This script helps you get started quickly by:
1. Creating necessary directories
2. Generating sample dataset
3. Verifying dependencies
4. Running a test analysis
"""

import subprocess
import sys
from pathlib import Path


def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")


def check_python_version():
    """Check if Python version is compatible"""
    print_header("🐍 Checking Python Version")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print(f"❌ Python {version.major}.{version.minor} detected")
        print("⚠️  Python 3.10+ required")
        print("   Please upgrade Python and try again")
        return False
    
    print(f"✓ Python {version.major}.{version.minor}.{version.micro} detected")
    return True


def create_directories():
    """Create necessary directories"""
    print_header("📁 Creating Directory Structure")
    
    directories = [
        "data",
        "reports",
        "reports/assets",
        "src"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created: {directory}/")
    
    return True


def install_dependencies():
    """Install required packages"""
    print_header("📦 Installing Dependencies")
    
    print("Installing packages from requirements.txt...")
    print("This may take a few minutes...\n")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "-q"
        ])
        print("\n✓ All dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("\n❌ Error installing dependencies")
        print("   Try running manually: pip install -r requirements.txt")
        return False


def generate_sample_data():
    """Generate sample dataset"""
    print_header("📊 Generating Sample Dataset")
    
    try:
        from src.utils import generate_sample_sales_data
        
        df = generate_sample_sales_data(1000)
        output_path = Path("data/sample_dataset.csv")
        df.to_csv(output_path, index=False)
        
        print(f"✓ Sample dataset created: {output_path}")
        print(f"  • Records: {len(df):,}")
        print(f"  • Columns: {len(df.columns)}")
        print(f"  • Size: {output_path.stat().st_size / 1024:.2f} KB")
        return True
    except Exception as e:
        print(f"❌ Error generating sample data: {e}")
        return False


def setup_environment():
    """Setup environment file"""
    print_header("⚙️  Setting Up Environment")
    
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        print("✓ .env file already exists")
    elif env_example.exists():
        env_example.rename(env_file)
        print("✓ Created .env from template")
        print("  💡 Edit .env to add your OpenAI API key (optional)")
    else:
        print("⚠️  .env.example not found")
    
    return True


def run_test_analysis():
    """Run a test analysis"""
    print_header("🧪 Running Test Analysis")
    
    print("Analyzing sample dataset...\n")
    
    try:
        subprocess.check_call([
            sys.executable, "main.py", 
            "data/sample_dataset.csv",
            "--verbose"
        ])
        print("\n✓ Test analysis completed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("\n⚠️  Test analysis encountered an error")
        print("   This is normal if dependencies aren't fully installed")
        return False


def show_next_steps():
    """Show next steps to user"""
    print_header("🚀 Setup Complete!")
    
    print("Next steps:\n")
    
    print("1️⃣  Run the Streamlit Web UI:")
    print("   streamlit run streamlit_app.py\n")
    
    print("2️⃣  Or use the CLI:")
    print("   python main.py data/sample_dataset.csv\n")
    
    print("3️⃣  Analyze your own data:")
    print("   python main.py path/to/your/data.csv --author \"Your Name\"\n")
    
    print("4️⃣  Enable GPT-4 (optional):")
    print("   • Get API key from: https://platform.openai.com/api-keys")
    print("   • Add to .env file: OPENAI_API_KEY=sk-your-key-here")
    print("   • Run with: python main.py data.csv --api-key sk-your-key\n")
    
    print("📚 Documentation: README.md")
    print("🐛 Issues: https://github.com/rizzshi/DataSphere/issues\n")
    
    print("="*60)
    print("  Built with ❤️  by Algorzen Research Division")
    print("  Author: Rishi Singh")
    print("="*60 + "\n")


def main():
    """Main setup function"""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║         🤖 AI INSIGHT REPORTER - SETUP WIZARD           ║
    ║                                                          ║
    ║              Algorzen Research Division                  ║
    ║                   by Rishi Singh                         ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Setup environment
    setup_environment()
    
    # Ask about dependency installation
    print("\n" + "="*60)
    response = input("Install Python dependencies? (y/n): ").strip().lower()
    
    if response == 'y':
        if not install_dependencies():
            print("\n⚠️  Setup incomplete - dependency installation failed")
            print("   Please install manually: pip install -r requirements.txt")
            sys.exit(1)
        
        # Generate sample data
        generate_sample_data()
        
        # Ask about test run
        print("\n" + "="*60)
        response = input("Run test analysis on sample data? (y/n): ").strip().lower()
        
        if response == 'y':
            run_test_analysis()
    else:
        print("\n⚠️  Skipping dependency installation")
        print("   Install manually before running: pip install -r requirements.txt")
    
    # Show next steps
    show_next_steps()


if __name__ == "__main__":
    main()
