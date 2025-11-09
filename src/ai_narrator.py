"""
AI Narrator - GPT-4 Powered Narrative Generation
Algorzen Research Division

This module generates executive-level business narratives using
OpenAI's GPT-4 API, with intelligent fallback for offline operation.
"""

import os
from typing import Dict, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Try to import OpenAI (optional dependency)
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class AINarrator:
    """
    AI-powered narrative generation engine
    
    Produces executive-level business insights using GPT-4,
    with fallback to rule-based generation when API unavailable.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize AI Narrator
        
        Args:
            api_key: OpenAI API key (optional, will use env var if not provided)
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4-turbo-preview')
        self.client = None
        
        if self.api_key and OPENAI_AVAILABLE:
            try:
                self.client = OpenAI(api_key=self.api_key)
            except Exception as e:
                print(f"Warning: Could not initialize OpenAI client: {e}")
                self.client = None
    
    def _build_analysis_prompt(self, eda_summary: Dict, kpis: Dict) -> str:
        """
        Build comprehensive prompt for GPT-4
        
        Args:
            eda_summary: EDA results dictionary
            kpis: KPI dictionary
            
        Returns:
            Formatted prompt string
        """
        dataset_info = eda_summary.get('dataset_info', {})
        missing_info = eda_summary.get('missing_values', {})
        
        prompt = f"""You are a senior business analyst at Algorzen Research Division. Analyze the following dataset and provide an executive-level business intelligence report.

DATASET OVERVIEW:
- Type: {dataset_info.get('dataset_type', 'general').title()}
- Records: {dataset_info.get('rows', 0):,}
- Columns: {dataset_info.get('columns', 0)}
- Numeric Features: {dataset_info.get('numeric_columns', 0)}
- Categorical Features: {dataset_info.get('categorical_columns', 0)}

DATA QUALITY:
- Total Missing Values: {missing_info.get('total_missing', 0)}
- Columns with Missing Data: {missing_info.get('columns_with_missing', 0)}

KEY PERFORMANCE INDICATORS:
"""
        for key, value in kpis.items():
            prompt += f"- {key}: {value}\n"
        
        prompt += """
Please provide a comprehensive analysis in the following structure:

1. EXECUTIVE SUMMARY (3-5 sentences)
   - High-level overview of the dataset
   - Most critical findings
   - Strategic significance

2. KEY FINDINGS (4-6 bullet points)
   - Data-driven insights
   - Patterns and trends
   - Statistical highlights

3. ACTIONABLE RECOMMENDATIONS (4-6 bullet points)
   - Strategic actions based on data
   - Prioritized by business impact
   - Specific and measurable

4. RISKS & LIMITATIONS (3-4 bullet points)
   - Data quality concerns
   - Analytical limitations
   - Caveats for decision-making

Tone: Professional, executive-level (McKinsey style)
Focus: Business value and strategic insights
Format: Use clear headings and bullet points
"""
        return prompt
    
    def _generate_with_gpt4(self, prompt: str) -> str:
        """
        Generate narrative using GPT-4
        
        Args:
            prompt: Analysis prompt
            
        Returns:
            Generated narrative text
        """
        if not self.client:
            return None
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a senior business analyst at Algorzen Research Division, specialized in data-driven strategic insights."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return None
    
    def _generate_fallback_narrative(self, eda_summary: Dict, kpis: Dict) -> str:
        """
        Generate rule-based narrative when GPT-4 unavailable
        
        Args:
            eda_summary: EDA results dictionary
            kpis: KPI dictionary
            
        Returns:
            Fallback narrative text
        """
        dataset_info = eda_summary.get('dataset_info', {})
        dataset_type = dataset_info.get('dataset_type', 'general')
        rows = dataset_info.get('rows', 0)
        missing_info = eda_summary.get('missing_values', {})
        
        narrative = f"""## EXECUTIVE SUMMARY

This {dataset_type} dataset comprises {rows:,} records across {dataset_info.get('columns', 0)} features, providing a comprehensive view of operational metrics. The analysis reveals key performance indicators with strategic implications for business optimization. Data quality assessment indicates {missing_info.get('total_missing', 0)} missing values across {missing_info.get('columns_with_missing', 0)} columns, requiring attention in downstream analytics.

Our automated analysis identifies critical patterns in {dataset_info.get('numeric_columns', 0)} numeric and {dataset_info.get('categorical_columns', 0)} categorical dimensions, enabling data-driven decision-making.

## KEY FINDINGS

"""
        
        # Add KPI-based findings
        kpi_list = list(kpis.items())
        for i, (key, value) in enumerate(kpi_list[:6]):
            if 'total' in key.lower() or 'average' in key.lower():
                narrative += f"• **{key}**: {value} represents a critical operational metric for performance tracking\n"
            else:
                narrative += f"• **{key}**: {value}\n"
        
        narrative += """
• Statistical analysis reveals distribution patterns requiring strategic attention
• Correlation analysis identifies key interdependencies between business metrics
• Data completeness metrics enable confidence in analytical conclusions

## ACTIONABLE RECOMMENDATIONS

"""
        
        if dataset_type == 'sales':
            narrative += """• **Optimize Revenue Streams**: Focus on high-performing products and channels identified in the analysis
• **Enhance Customer Targeting**: Leverage segmentation insights to improve conversion rates
• **Inventory Management**: Align stock levels with demand patterns observed in quantity metrics
• **Pricing Strategy**: Review pricing elasticity based on revenue and margin correlations
• **Sales Forecasting**: Implement predictive models using historical trend patterns
• **Performance Monitoring**: Establish dashboards for real-time KPI tracking
"""
        elif dataset_type == 'finance':
            narrative += """• **Cash Flow Optimization**: Monitor debit/credit patterns to improve liquidity management
• **Risk Assessment**: Analyze transaction patterns for anomaly detection and fraud prevention
• **Account Segmentation**: Develop targeted strategies for high-value account retention
• **Cost Control**: Identify expense categories with optimization potential
• **Financial Planning**: Use historical patterns for improved budget forecasting
• **Compliance Monitoring**: Ensure transaction data quality for regulatory reporting
"""
        elif dataset_type == 'customer':
            narrative += """• **Churn Prevention**: Implement retention programs targeting at-risk customer segments
• **Customer Lifetime Value Optimization**: Focus resources on high-value customer acquisition
• **Segmentation Strategy**: Develop tailored engagement approaches for each customer tier
• **Experience Enhancement**: Address pain points identified in customer behavior patterns
• **Loyalty Programs**: Design initiatives based on observed retention factors
• **Predictive Analytics**: Build churn prediction models for proactive intervention
"""
        else:
            narrative += """• **Data Quality Improvement**: Address missing values and inconsistencies identified in the analysis
• **Feature Engineering**: Develop new metrics based on correlation insights
• **Automated Monitoring**: Implement systematic tracking of key performance indicators
• **Stakeholder Reporting**: Create executive dashboards for strategic decision support
• **Predictive Modeling**: Leverage historical patterns for forecasting initiatives
• **Process Optimization**: Use data insights to streamline operational workflows
"""
        
        narrative += """
## RISKS & LIMITATIONS

"""
        
        # Dynamic risk assessment
        data_completeness = 100 - (missing_info.get('total_missing', 0) / (rows * dataset_info.get('columns', 1)) * 100)
        
        if data_completeness < 95:
            narrative += f"• **Data Quality**: {missing_info.get('total_missing', 0)} missing values may impact analytical reliability\n"
        
        narrative += f"""• **Sample Size Considerations**: Analysis based on {rows:,} records; trends may vary with additional data
• **Temporal Limitations**: Results reflect current dataset timeframe; market conditions may evolve
• **Correlation vs Causation**: Observed patterns require validation before implementing strategic changes
• **External Factors**: Analysis does not account for exogenous variables affecting business performance
"""
        
        return narrative
    
    def generate_narrative(self, eda_summary: Dict, kpis: Dict, force_fallback: bool = False) -> Dict[str, str]:
        """
        Generate comprehensive business narrative
        
        Args:
            eda_summary: EDA results dictionary
            kpis: KPI dictionary
            force_fallback: Force use of fallback generator (for testing)
            
        Returns:
            Dictionary with narrative sections and metadata
        """
        narrative_text = None
        method_used = "fallback"
        
        # Try GPT-4 first if available
        if not force_fallback and self.client:
            prompt = self._build_analysis_prompt(eda_summary, kpis)
            narrative_text = self._generate_with_gpt4(prompt)
            if narrative_text:
                method_used = "gpt-4"
        
        # Use fallback if GPT-4 failed or unavailable
        if not narrative_text:
            narrative_text = self._generate_fallback_narrative(eda_summary, kpis)
        
        return {
            'narrative': narrative_text,
            'method': method_used,
            'model': self.model if method_used == "gpt-4" else "rule-based",
            'api_available': self.client is not None
        }


def generate_narrative(eda_summary: Dict, kpis: Dict, api_key: Optional[str] = None) -> Dict[str, str]:
    """
    Convenience function to generate AI narrative
    
    Args:
        eda_summary: EDA results dictionary
        kpis: KPI dictionary
        api_key: Optional OpenAI API key
        
    Returns:
        Narrative dictionary
    """
    narrator = AINarrator(api_key)
    return narrator.generate_narrative(eda_summary, kpis)
