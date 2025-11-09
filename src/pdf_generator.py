"""
PDF Report Generator - Professional Business Intelligence Reports
Algorzen Research Division

This module generates branded PDF reports combining EDA visualizations,
KPIs, and AI-generated narratives with executive-level presentation quality.
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak,
    Table, TableStyle, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import json


class EvidenReportTemplate:
    """
    Custom PDF template with Eviden branding
    """
    
    def __init__(self, filename: str, author: str = "Rishi Singh"):
        """
        Initialize report template
        
        Args:
            filename: Output PDF filename
            author: Report author name
        """
        self.filename = filename
        self.author = author
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.date_readable = datetime.now().strftime("%B %d, %Y")
        self.logo_path = str(Path(__file__).parent.parent / "assets" / "eviden_logo.png")
        # Create document
        self.doc = SimpleDocTemplate(
            filename,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=1*inch,
            bottomMargin=0.75*inch
        )
        self.story = []
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """
        Setup custom paragraph styles
        """
        # Title Style
        self.styles.add(ParagraphStyle(
            name='AlgorzenTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a2e'),
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Title Style
        self.styles.add(ParagraphStyle(
            name='EvidenTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a2e'),
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        # Subtitle Style
        self.styles.add(ParagraphStyle(
            name='EvidenSubtitle',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#16213e'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica'
        ))
        # Section Header
        self.styles.add(ParagraphStyle(
            name='EvidenSection',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#0f3460'),
            spaceAfter=12,
            spaceBefore=20,
            fontName='Helvetica-Bold',
            borderWidth=1,
            borderColor=colors.HexColor('#e94560'),
            borderPadding=5,
            backColor=colors.HexColor('#f0f0f0')
        ))
        # Body Text
        self.styles.add(ParagraphStyle(
            name='EvidenBody',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#222222'),
            spaceAfter=8,
            fontName='Helvetica'
        ))
        # KPI Table
        self.styles.add(ParagraphStyle(
            name='EvidenKPI',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#e94560'),
            fontName='Helvetica-Bold'
        ))
            logo_height = 0.45 * inch
            canvas_obj.drawImage(self.logo_path, 0.75*inch, letter[1] - 0.7*inch, width=logo_width, height=logo_height, mask='auto')
        except Exception:
            # fallback to text if logo missing
            canvas_obj.setFont('Helvetica-Bold', 12)
            canvas_obj.setFillColor(colors.HexColor('#1a1a2e'))
            canvas_obj.drawString(0.75*inch, letter[1] - 0.5*inch, "Eviden — Insight Reporter")
        # Footer
        canvas_obj.setFont('Helvetica', 8)
        canvas_obj.setFillColor(colors.HexColor('#666666'))
        canvas_obj.drawString(
            0.75*inch,
            0.5*inch,
            f"© 2025 Eviden | Author: {self.author}"
        )
        canvas_obj.drawRightString(
            letter[0] - 0.75*inch,
            0.5*inch,
            f"Page {doc.page} | Generated: {self.date_readable}"
        )
        canvas_obj.restoreState()
    
    def add_title_page(self, dataset_type: str, record_count: int):
        """
        Add title page
        
        Args:
            dataset_type: Type of dataset analyzed
            record_count: Number of records
        """
        # Logo at top
        if self.logo_path and Path(self.logo_path).exists():
            self.story.append(Image(self.logo_path, width=2.5*inch, height=0.9*inch))
            self.story.append(Spacer(1, 0.05*inch))
            # Add 'Created by Algorzen' under logo
            self.story.append(Paragraph('<b>Created by Algorzen</b>', self.styles['EvidenSubtitle']))
            self.story.append(Spacer(1, 0.15*inch))
        # Title
        title = Paragraph(
            "Eviden Insight Report",
            self.styles['EvidenTitle']
        )
        self.story.append(title)
        self.story.append(Spacer(1, 0.3*inch))
        # Subtitle
        subtitle = Paragraph(
            f"Automated Analysis of {dataset_type.title()} Dataset<br/>"
            f"{record_count:,} Records Analyzed",
            self.styles['EvidenSubtitle']
        )
        self.story.append(subtitle)
        self.story.append(Spacer(1, 0.5*inch))
        
        # Metadata table
        metadata = [
            ['Report Generated:', self.date_readable],
            ['Analysis Type:', 'Comprehensive EDA + AI Narrative'],
            ['Dataset Type:', dataset_type.title()],
            ['Record Count:', f"{record_count:,}"],
            ['Author:', self.author],
            ['Division:', 'Eviden']
        ]
        
        metadata_table = Table(metadata, colWidths=[2.5*inch, 3.5*inch])
        metadata_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica', 10),
            ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 10),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#0f3460')),
            ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#2a2a2a')),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
            ('PADDING', (0, 0), (-1, -1), 8),
        ]))
        
        self.story.append(metadata_table)
        self.story.append(PageBreak())
    
    def add_section(self, title: str, content: str):
        """
        Add a report section
        
        Args:
            title: Section title
            content: Section content (can include HTML-like markup)
        """
    section_title = Paragraph(title, self.styles['EvidenSection'])
        self.story.append(section_title)
        self.story.append(Spacer(1, 0.15*inch))
        
        # Split content into paragraphs
        paragraphs = content.split('\n\n')
        for para in paragraphs:
            if para.strip():
                p = Paragraph(para.strip(), self.styles['EvidenBody'])
                self.story.append(p)
                self.story.append(Spacer(1, 0.1*inch))
    
    def add_kpi_section(self, kpis: Dict):
        """
        Add KPI section with formatted table
        
        Args:
            kpis: Dictionary of KPIs
        """
    section_title = Paragraph("Key Performance Indicators", self.styles['EvidenSection'])
        self.story.append(section_title)
        self.story.append(Spacer(1, 0.15*inch))
        
        # Convert KPIs to table format
        kpi_data = [['Metric', 'Value']]
        for key, value in kpis.items():
            kpi_data.append([str(key), str(value)])
        
        kpi_table = Table(kpi_data, colWidths=[3.5*inch, 3*inch])
        kpi_table.setStyle(TableStyle([
            # Header
            ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 11),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0f3460')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('PADDING', (0, 0), (-1, 0), 10),
            
            # Body
            ('FONT', (0, 1), (-1, -1), 'Helvetica', 10),
            ('FONT', (0, 1), (0, -1), 'Helvetica-Bold', 10),
            ('TEXTCOLOR', (0, 1), (0, -1), colors.HexColor('#0f3460')),
            ('TEXTCOLOR', (1, 1), (1, -1), colors.HexColor('#2a2a2a')),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),
            ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')]),
            ('PADDING', (0, 1), (-1, -1), 8),
        ]))
        
        self.story.append(kpi_table)
        self.story.append(Spacer(1, 0.3*inch))
    
    def add_image(self, image_path: str, width: float = 6.5, caption: Optional[str] = None):
        """
        Add image to report
        
        Args:
            image_path: Path to image file
            width: Image width in inches
            caption: Optional image caption
        """
        if Path(image_path).exists():
            img = Image(image_path, width=width*inch, height=width*0.75*inch)
            self.story.append(img)
            
            if caption:
                cap = Paragraph(
                    f"<i>{caption}</i>",
                    ParagraphStyle(
                        'ImageCaption',
                        parent=self.styles['Normal'],
                        fontSize=9,
                        textColor=colors.HexColor('#666666'),
                        alignment=TA_CENTER,
                        spaceAfter=12
                    )
                )
                self.story.append(cap)
            
            self.story.append(Spacer(1, 0.2*inch))
    
    def build(self):
        """
        Build the final PDF
        """
        self.doc.build(self.story, onFirstPage=self._header_footer, onLaterPages=self._header_footer)


def generate_pdf_report(
    eda_summary: Dict,
    kpis: Dict,
    narrative: Dict,
    output_dir: str = "reports",
    author: str = "Rishi Singh"
) -> str:
    """
    Generate comprehensive PDF report
    
    Args:
        eda_summary: EDA results dictionary
        kpis: KPI dictionary
        narrative: AI-generated narrative dictionary
        output_dir: Output directory for PDF
        author: Report author name
        
    Returns:
        Path to generated PDF file
    """
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d")
    filename = output_path / f"Eviden_Insight_Report_{timestamp}.pdf"
    
    # Initialize report
    report = EvidenReportTemplate(str(filename), author)
    
    # Add title page
    dataset_info = eda_summary.get('dataset_info', {})
    report.add_title_page(
        dataset_type=dataset_info.get('dataset_type', 'general'),
        record_count=dataset_info.get('rows', 0)
    )
    
    # Add Executive Summary & KPIs
    report.add_kpi_section(kpis)
    
    # Add AI Narrative
    narrative_text = narrative.get('narrative', '')
    report.add_section("AI-Generated Business Analysis", narrative_text)
    
    # Add visualizations
    visualizations = eda_summary.get('visualizations', {})
    
    # Correlation heatmap
    heatmap_path = visualizations.get('correlation_heatmap')
    if heatmap_path and Path(heatmap_path).exists():
        report.story.append(PageBreak())
        report.add_section("Correlation Analysis", 
                          "The following heatmap illustrates relationships between numeric variables, "
                          "identifying potential dependencies and optimization opportunities.")
        report.add_image(heatmap_path, caption="Feature Correlation Matrix")
    
    # Distribution plots
    distributions = visualizations.get('distributions', {})
    
    if distributions.get('numeric') and Path(distributions['numeric']).exists():
        report.story.append(PageBreak())
        report.add_section("Numeric Distributions",
                          "Distribution analysis of key numeric features reveals patterns in "
                          "central tendency, spread, and potential outliers.")
        report.add_image(distributions['numeric'], caption="Numeric Feature Distributions")
    
    if distributions.get('categorical') and Path(distributions['categorical']).exists():
        report.add_section("Categorical Distributions",
                          "Categorical feature analysis identifies dominant segments and "
                          "distribution imbalances requiring strategic attention.")
        report.add_image(distributions['categorical'], caption="Categorical Feature Distributions")
    
    # Add data quality section
    report.story.append(PageBreak())
    missing_info = eda_summary.get('missing_values', {})
    quality_text = f"""
    <b>Data Completeness Assessment:</b><br/>
    • Total Missing Values: {missing_info.get('total_missing', 0):,}<br/>
    • Affected Columns: {missing_info.get('columns_with_missing', 0)}<br/>
    • Dataset Integrity: {((dataset_info.get('rows', 0) * dataset_info.get('columns', 1) - missing_info.get('total_missing', 0)) / (dataset_info.get('rows', 1) * dataset_info.get('columns', 1)) * 100):.2f}% Complete<br/>
    <br/>
    <b>Analysis Methodology:</b><br/>
    • Engine: Eviden Insight Reporter v1.0 (Created by Algorzen)<br/>
    • AI Model: {narrative.get('model', 'N/A')}<br/>
    • Generation Method: {narrative.get('method', 'N/A')}<br/>
    """
    report.add_section("Technical Appendix", quality_text)
    
    # Build PDF
    report.build()
    
    # Generate metadata JSON
    metadata = {
        "project": "AI Insight Reporter",
        "report_id": f"AIR-2025-Q4-{timestamp}",
        "generated_by": author,
        "created_at": datetime.now().isoformat(),
        "tone": "Executive Business",
        "openai_used": narrative.get('method') == 'gpt-4',
        "dataset_type": dataset_info.get('dataset_type', 'general'),
        "record_count": dataset_info.get('rows', 0),
        "pdf_file": str(filename)
    }
    
    metadata_file = output_path / "report_metadata.json"
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    return str(filename)
