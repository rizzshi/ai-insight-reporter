"""
Streamlit UI - AI Insight Reporter Web Interface
Algorzen Research Division

Interactive web application for uploading datasets, previewing EDA results,
and generating comprehensive AI-powered business intelligence reports.
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path
import json

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.eda_engine import perform_eda
from src.kpi_extractor import extract_kpis
from src.ai_narrator import generate_narrative
from src.pdf_generator import generate_pdf_report


# Page configuration
st.set_page_config(
    page_title="AI Insight Reporter - Algorzen",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1a1a2e;
        text-align: center;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #16213e;
        text-align: center;
        margin-bottom: 2rem;
    }
    .kpi-box {
        background-color: #f0f0f0;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #e94560;
        margin-bottom: 1rem;
    }
    .kpi-value {
        font-size: 1.5rem;
        font-weight: bold;
        color: #0f3460;
    }
    .kpi-label {
        font-size: 0.9rem;
        color: #666666;
    }
    .footer {
        text-align: center;
        color: #666666;
        font-size: 0.85rem;
        margin-top: 3rem;
        padding: 1rem;
        border-top: 1px solid #cccccc;
    }
    </style>
""", unsafe_allow_html=True)


def main():
    """
    Main Streamlit application
    """
    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/200x80/1a1a2e/ffffff?text=ALGORZEN", use_column_width=True)
        st.markdown("### 🎯 AI Insight Reporter")
        st.markdown("**Autonomous Business Intelligence**")
        st.markdown("---")
        
        st.markdown("#### 📋 Features")
        st.markdown("""
        - ✅ Automatic Dataset Detection
        - ✅ Comprehensive EDA
        - ✅ AI-Powered Narratives
        - ✅ Professional PDF Reports
        - ✅ KPI Extraction
        """)
        
        st.markdown("---")
        st.markdown("#### ⚙️ Settings")
        
        use_gpt4 = st.checkbox("Use GPT-4 (requires API key)", value=False)
        if use_gpt4:
            api_key = st.text_input("OpenAI API Key", type="password")
        else:
            api_key = None
        
        author_name = st.text_input("Report Author", value="Om Singh")
        
        st.markdown("---")
        st.markdown("**© 2025 Algorzen Research**")
        st.markdown("*Developed by Om Singh*")
    
    # Main content
    st.markdown('<div class="main-header">🤖 AI Insight Reporter</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Algorzen Research Division — Automated Business Intelligence</div>', unsafe_allow_html=True)
    
    # File upload
    st.markdown("### 📤 Upload Your Dataset")
    uploaded_file = st.file_uploader(
        "Upload CSV or Excel file",
        type=['csv', 'xlsx', 'xls'],
        help="Upload your dataset for automated analysis (Note: Parquet disabled due to PyArrow compatibility)"
    )
    
    if uploaded_file is not None:
        try:
            # Load dataset
            with st.spinner("Loading dataset..."):
                file_extension = Path(uploaded_file.name).suffix.lower()
                
                if file_extension == '.csv':
                    df = pd.read_csv(uploaded_file)
                elif file_extension in ['.xlsx', '.xls']:
                    df = pd.read_excel(uploaded_file)
                else:
                    st.error("Unsupported file format. Please upload CSV or Excel files.")
                    return
            
            st.success(f"✅ Dataset loaded: {len(df):,} rows × {len(df.columns)} columns")
            
            # Dataset preview
            with st.expander("📊 Dataset Preview", expanded=False):
                # Use st.table() instead of st.dataframe() to avoid PyArrow dependency
                st.write(df.head(20))
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Total Rows", f"{len(df):,}")
                col2.metric("Total Columns", f"{len(df.columns)}")
                col3.metric("Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
            
            # Run analysis
            if st.button("🚀 Generate AI Report", type="primary", use_container_width=True):
                with st.spinner("🔬 Performing exploratory data analysis..."):
                    # EDA
                    eda_summary = perform_eda(df)
                    st.session_state['eda_summary'] = eda_summary
                    
                    dataset_type = eda_summary['dataset_info']['dataset_type']
                    st.info(f"📌 Dataset Type Detected: **{dataset_type.title()}**")
                
                with st.spinner("📊 Extracting key performance indicators..."):
                    # KPI Extraction
                    kpis = extract_kpis(df, dataset_type)
                    st.session_state['kpis'] = kpis
                
                with st.spinner("🤖 Generating AI narrative..."):
                    # AI Narrative
                    narrative = generate_narrative(eda_summary, kpis, api_key)
                    st.session_state['narrative'] = narrative
                
                with st.spinner("📄 Creating PDF report..."):
                    # PDF Generation
                    pdf_path = generate_pdf_report(
                        eda_summary,
                        kpis,
                        narrative,
                        author=author_name
                    )
                    st.session_state['pdf_path'] = pdf_path
                
                st.success("✅ Analysis complete!")
            
            # Display results if available
            if 'eda_summary' in st.session_state:
                st.markdown("---")
                st.markdown("## 📈 Analysis Results")
                
                # KPIs
                st.markdown("### 🎯 Key Performance Indicators")
                kpis = st.session_state.get('kpis', {})
                
                # Display KPIs in a grid
                kpi_items = list(kpis.items())
                num_cols = 3
                for i in range(0, len(kpi_items), num_cols):
                    cols = st.columns(num_cols)
                    for j, col in enumerate(cols):
                        if i + j < len(kpi_items):
                            key, value = kpi_items[i + j]
                            col.markdown(f"""
                            <div class="kpi-box">
                                <div class="kpi-label">{key}</div>
                                <div class="kpi-value">{value}</div>
                            </div>
                            """, unsafe_allow_html=True)
                
                # Visualizations
                st.markdown("### 📊 Visualizations")
                
                viz = st.session_state['eda_summary'].get('visualizations', {})
                
                # Correlation heatmap
                if viz.get('correlation_heatmap') and Path(viz['correlation_heatmap']).exists():
                    st.markdown("#### Correlation Matrix")
                    st.image(viz['correlation_heatmap'], use_column_width=True)
                
                # Distributions
                distributions = viz.get('distributions', {})
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if distributions.get('numeric') and Path(distributions['numeric']).exists():
                        st.markdown("#### Numeric Distributions")
                        st.image(distributions['numeric'], use_column_width=True)
                
                with col2:
                    if distributions.get('categorical') and Path(distributions['categorical']).exists():
                        st.markdown("#### Categorical Distributions")
                        st.image(distributions['categorical'], use_column_width=True)
                
                # AI Narrative
                st.markdown("### 🤖 AI-Generated Insights")
                narrative = st.session_state.get('narrative', {})
                
                st.info(f"**Generation Method:** {narrative.get('method', 'N/A').upper()} | "
                       f"**Model:** {narrative.get('model', 'N/A')}")
                
                st.markdown(narrative.get('narrative', 'No narrative generated'))
                
                # Download button
                if 'pdf_path' in st.session_state:
                    st.markdown("---")
                    st.markdown("### 📥 Download Report")
                    
                    with open(st.session_state['pdf_path'], 'rb') as f:
                        pdf_bytes = f.read()
                    
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.download_button(
                            label="📄 Download PDF Report",
                            data=pdf_bytes,
                            file_name=Path(st.session_state['pdf_path']).name,
                            mime="application/pdf",
                            type="primary",
                            use_container_width=True
                        )
                    
                    with col2:
                        # Load metadata
                        metadata_path = Path("reports/report_metadata.json")
                        if metadata_path.exists():
                            with open(metadata_path, 'r') as f:
                                metadata = json.load(f)
                            
                            st.download_button(
                                label="📋 Download Metadata",
                                data=json.dumps(metadata, indent=2),
                                file_name="report_metadata.json",
                                mime="application/json",
                                use_container_width=True
                            )
        
        except Exception as e:
            st.error(f"❌ Error processing dataset: {str(e)}")
            st.exception(e)
    
    else:
        # Instructions when no file uploaded
        st.info("👆 Upload a dataset to begin automated analysis")
        
        st.markdown("### 🎯 How It Works")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### 1️⃣ Upload Data")
            st.markdown("Upload your CSV or Excel dataset")
        
        with col2:
            st.markdown("#### 2️⃣ AI Analysis")
            st.markdown("Automated EDA, KPI extraction, and GPT-4 insights")
        
        with col3:
            st.markdown("#### 3️⃣ Get Report")
            st.markdown("Download professional PDF with visualizations")
        
        st.markdown("---")
        st.markdown("### 🔥 Key Features")
        
        features = """
        - **Intelligent Dataset Detection**: Automatically identifies sales, finance, customer, or general datasets
        - **Comprehensive EDA**: Missing values, statistics, correlations, and distributions
        - **Smart KPI Extraction**: Context-aware metrics based on dataset type
        - **GPT-4 Integration**: Executive-level narratives with actionable recommendations
        - **Professional Reports**: Branded PDFs with Algorzen formatting
        - **Fallback Mode**: Works offline without OpenAI API
        """
        st.markdown(features)
    
    # Footer
    st.markdown("""
    <div class="footer">
        <strong>AI Insight Reporter v1.0</strong> | Algorzen Research Division<br>
        Developed by Om Singh | © 2025 Algorzen Research | Powered by GPT-4 & Python
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
