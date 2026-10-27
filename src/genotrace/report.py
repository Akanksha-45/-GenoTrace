"""
Report generation for GenoTrace.
Creates HTML and Markdown reports with results and visualizations.
"""
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List
import pandas as pd


class ReportError(Exception):
    """Custom exception for report generation errors."""
    pass


def generate_markdown_report(
    summary_stats: Dict[str, Any],
    prioritized_df: pd.DataFrame,
    qc_summary: Optional[Dict[str, Any]] = None,
    output_file: str = "results/reports/genotrace_report.md"
) -> None:
    """
    Generate a Markdown report.
    
    Args:
        summary_stats: Summary statistics dictionary
        prioritized_df: Prioritized variants DataFrame
        qc_summary: Optional QC summary
        output_file: Output file path
    """
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    
    report_lines = []
    report_lines.append("# GenoTrace Analysis Report")
    report_lines.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append(f"\n**Report Version:** 1.0")
    report_lines.append("\n---\n")
    
    # Disclaimer
    report_lines.append("## Disclaimer")
    report_lines.append("\n> **Research Use Only:** GenoTrace is an educational and research tool. ")
    report_lines.append("It is not intended for clinical diagnosis or treatment decisions. ")
    report_lines.append("Variant prioritization is heuristic and requires further experimental validation.\n")
    
    # Summary
    report_lines.append("## Analysis Summary\n")
    report_lines.append(f"- **Total variants analyzed:** {summary_stats.get('total_variants', 'N/A')}")
    report_lines.append(f"- **Variants after filtering:** {summary_stats.get('filtered_variants', 'N/A')}")
    report_lines.append(f"- **Top candidates reported:** {len(prioritized_df)}")
    report_lines.append(f"- **Chromosomes covered:** {summary_stats.get('chromosomes', 'N/A')}\n")
    
    # QC Summary
    if qc_summary:
        report_lines.append("## Quality Control\n")
        report_lines.append(f"- **Overall Status:** {qc_summary.get('overall_status', 'N/A')}")
        if qc_summary.get('issues'):
            report_lines.append("- **Issues:**")
            for issue in qc_summary['issues']:
                report_lines.append(f"  - {issue}")
        if qc_summary.get('recommendations'):
            report_lines.append("- **Recommendations:**")
            for rec in qc_summary['recommendations']:
                report_lines.append(f"  - {rec}")
        report_lines.append("\n")
    
    # Top Candidates
    report_lines.append("## Top Prioritized Candidates\n")
    if not prioritized_df.empty:
        # Show top 20
        top_show = prioritized_df.head(20).copy()
        display_cols = ['rank', '#CHROM', 'POS', 'REF', 'ALT', 'QUAL', 
                       'prioritization_score', 'rationale']
        available = [c for c in display_cols if c in top_show.columns]
        report_lines.append(top_show[available].to_markdown(index=False))
        report_lines.append("\n")
    else:
        report_lines.append("*No variants to report.*\n")
    
    # Methodology
    report_lines.append("## Methodology\n")
    report_lines.append("Variants were prioritized using an explainable scoring system:")
    report_lines.append("- **Quality (30%):** Normalized variant quality score")
    report_lines.append("- **Effect (40%):** Predicted molecular impact severity")
    report_lines.append("- **Frequency (20%):** Population allele frequency (rarer = higher priority)")
    report_lines.append("- **Biological (10%):** Gene annotation and relevance\n")
    report_lines.append("*Missing data is treated as unknown (neutral), not penalized.*\n")
    
    # Limitations
    report_lines.append("## Limitations\n")
    report_lines.append("- Heuristic scoring system, not clinically validated")
    report_lines.append("- Results depend on reference genome, tools, and parameters used")
    report_lines.append("- Annotation quality affects effect predictions")
    report_lines.append("- Population frequency data may be incomplete")
    report_lines.append("- No clinical interpretation or pathogenicity assessment\n")
    
    # References
    report_lines.append("## References\n")
    report_lines.append("- [Biopython](https://biopython.org/)")
    report_lines.append("- [Galaxy Training: Variant Analysis](https://training.galaxyproject.org/training-material/topics/variant-analysis/)")
    report_lines.append("- [VCF Format Specification](https://samtools.github.io/hts-specs/VCFv4.2.pdf)\n")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    print(f"Markdown report generated: {output_file}")


def generate_html_report(
    summary_stats: Dict[str, Any],
    prioritized_df: pd.DataFrame,
    figures: Optional[List[str]] = None,
    output_file: str = "results/reports/genotrace_report.html"
) -> None:
    """
    Generate an HTML report.
    
    Args:
        summary_stats: Summary statistics
        prioritized_df: Prioritized variants
        figures: List of figure paths
        output_file: Output file path
    """
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    
    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GenoTrace Analysis Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f9f9f9; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; margin-top: 30px; border-bottom: 2px solid #ecf0f1; padding-bottom: 5px; }}
        .disclaimer {{ background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; }}
        .summary {{ background-color: #e8f4f8; padding: 15px; border-radius: 5px; }}
        table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
        th {{ background-color: #3498db; color: white; padding: 12px; text-align: left; }}
        td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
        tr:hover {{ background-color: #f5f5f5; }}
        .footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; text-align: center; color: #7f8c8d; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🧬 GenoTrace Analysis Report</h1>
        <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <div class="disclaimer">
            <strong>⚠️ Research Use Only</strong><br>
            GenoTrace is an educational and research tool. It is not intended for clinical diagnosis or treatment decisions.
        </div>
        
        <h2>Analysis Summary</h2>
        <div class="summary">
            <ul>
                <li><strong>Total variants analyzed:</strong> {summary_stats.get('total_variants', 'N/A')}</li>
                <li><strong>Variants after filtering:</strong> {summary_stats.get('filtered_variants', 'N/A')}</li>
                <li><strong>Top candidates reported:</strong> {len(prioritized_df)}</li>
                <li><strong>Chromosomes covered:</strong> {summary_stats.get('chromosomes', 'N/A')}</li>
            </ul>
        </div>
        
        <h2>Top Prioritized Candidates</h2>
        {prioritized_df.head(30).to_html(index=False, classes='table') if not prioritized_df.empty else '<p><em>No variants to report.</em></p>'}
        
        <h2>Methodology</h2>
        <p>Variants were prioritized using an explainable weighted scoring system:</p>
        <ul>
            <li><strong>Quality (30%):</strong> Normalized variant quality score</li>
            <li><strong>Effect (40%):</strong> Predicted molecular impact severity</li>
            <li><strong>Frequency (20%):</strong> Population allele frequency</li>
            <li><strong>Biological (10%):</strong> Gene annotation and relevance</li>
        </ul>
        <p><em>Missing data is treated as unknown (neutral), not penalized.</em></p>
        
        <h2>Limitations</h2>
        <ul>
            <li>Heuristic scoring system, not clinically validated</li>
            <li>Results depend on reference genome, tools, and parameters used</li>
            <li>Annotation quality affects effect predictions</li>
            <li>Population frequency data may be incomplete</li>
            <li>No clinical interpretation or pathogenicity assessment</li>
        </ul>
        
        <div class="footer">
            <p>Generated by <strong>GenoTrace</strong> v0.1.0 | Research and Educational Use Only</p>
        </div>
    </div>
</body>
</html>
"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"HTML report generated: {output_file}")
