"""
Clinical Decision Support report generator.
Educational prototype only.
"""
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
import pandas as pd

try:
    from fpdf import FPDF
    PDF_AVAILABLE = True
except Exception:
    PDF_AVAILABLE = False


class ClinicalReportGenerator:
    def __init__(self, output_dir: str = "results/reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_report(self, variants_df: pd.DataFrame, acmg_df: pd.DataFrame,
                       patient_info: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        patient_info = patient_info or {}
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        md_file = self.output_dir / f"GenoTrace_Clinical_Decision_Support_Report_{timestamp}.md"
        html_file = self.output_dir / f"GenoTrace_Clinical_Decision_Support_Report_{timestamp}.html"
        csv_file = self.output_dir / f"clinical_variants_with_acmg_{timestamp}.csv"
        pdf_file = self.output_dir / f"GenoTrace_Clinical_Decision_Support_Report_{timestamp}.pdf"
        
        merged = variants_df.copy()
        if not acmg_df.empty:
            acmg_df = acmg_df.copy()
            acmg_df['POS'] = acmg_df['POS'].astype(str)
            merged['POS'] = merged['POS'].astype(str)
            merged = merged.merge(acmg_df[['POS', 'classification', 'evidence_codes', 'rationale']], 
                                on='POS', how='left')
        
        merged.to_csv(csv_file, index=False)
        
        # Markdown report
        md_content = []
        md_content.append("# GenoTrace Clinical Decision Support (CDS) Report")
        md_content.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        md_content.append("\n---\n")
        md_content.append("## IMPORTANT DISCLAIMER")
        md_content.append("\n**RESEARCH & EDUCATIONAL PROTOTYPE - NOT A DIAGNOSTIC TOOL**")
        md_content.append("\n- This is a Clinical Decision Support prototype for educational/research purposes only.")
        md_content.append("- It is NOT intended for clinical diagnosis, treatment, or medical decision making.")
        md_content.append("- Final interpretation and reporting MUST be performed by a qualified medical geneticist/pathologist.")
        md_content.append("- ACMG classification shown is simplified and requires expert review with full clinical context.\n")
        md_content.append("## Patient & Sample Information")
        md_content.append(f"- **Patient ID:** {patient_info.get('patient_id', 'NOT PROVIDED')}")
        md_content.append(f"- **Sample ID:** {patient_info.get('sample_id', 'NOT PROVIDED')}")
        md_content.append(f"- **Requested By:** {patient_info.get('requested_by', 'NOT PROVIDED')}")
        md_content.append(f"- **Laboratory:** {patient_info.get('lab', 'NOT PROVIDED')}\n")
        md_content.append("## Variants with ACMG Classification")
        display_cols = ['#CHROM', 'POS', 'REF', 'ALT', 'QUAL', 'classification', 'evidence_codes', 'rationale']
        available = [c for c in display_cols if c in merged.columns]
        if available and not merged.empty:
            try:
                md_content.append(merged[available].to_markdown(index=False))
            except:
                md_content.append(merged[available].to_string(index=False))
        else:
            md_content.append("*No variants to display.*")
        md_content.append("\n")
        
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(md_content))
        
        # HTML
        html_content = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><title>GenoTrace CDS Report</title>
        <style>body{{font-family:Arial;margin:40px;background:#f9f9f9}}.container{{max-width:1200px;margin:auto;background:white;padding:30px;box-shadow:0 0 10px #ccc}}
        h1{{color:#d32f2f;border-bottom:3px solid #d32f2f}}h2{{color:#1976d2;border-bottom:2px solid #eee}}.disc{{background:#ffebee;padding:15px;border-left:4px solid #d32f2f}}
        table{{border-collapse:collapse;width:100%}}th{{background:#1976d2;color:white;padding:10px}}td{{padding:8px;border-bottom:1px solid #ddd}}</style>
        </head><body><div class="container">
        <h1>GenoTrace Clinical Decision Support Report</h1>
        <p><b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <div class="disc"><b>RESEARCH & EDUCATIONAL PROTOTYPE - NOT A DIAGNOSTIC TOOL</b><br>Final interpretation must be done by a qualified medical geneticist/pathologist.</div>
        <h2>Patient & Sample</h2><ul><li>Patient ID: {patient_info.get('patient_id')}</li><li>Sample ID: {patient_info.get('sample_id')}</li><li>Lab: {patient_info.get('lab')}</li><li>Requested By: {patient_info.get('requested_by')}</li></ul>
        <h2>Variants</h2>{merged[available].to_html(index=False) if available and not merged.empty else '<p>No variants</p>'}
        </div></body></html>"""
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # PDF
        if PDF_AVAILABLE and available and not merged.empty:
            try:
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Helvetica", "B", 16)
                pdf.cell(0, 10, "GenoTrace Clinical Decision Support Report", ln=True, align='C')
                pdf.set_font("Helvetica", "", 9)
                pdf.cell(0, 6, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='C')
                pdf.ln(4)
                pdf.set_font("Helvetica", "B", 10)
                pdf.cell(0, 6, "RESEARCH & EDUCATIONAL PROTOTYPE - NOT A DIAGNOSTIC TOOL", ln=True)
                pdf.set_font("Helvetica", "", 8)
                pdf.multi_cell(0, 4, "Not for clinical diagnosis. Final interpretation by qualified medical geneticist/pathologist.")
                pdf.ln(4)
                pdf.set_font("Helvetica", "B", 11)
                pdf.cell(0, 6, "Variants", ln=True)
                pdf.set_font("Helvetica", size=7)
                # Simple table
                for idx, row in merged[available].head(30).iterrows():
                    pdf.multi_cell(0, 4, f"{row.get('#CHROM','')}:{row.get('POS','')} {row.get('REF','')}>{row.get('ALT','')} | {row.get('classification','')} | {row.get('evidence_codes','')} | {str(row.get('rationale',''))[:80]}")
                    pdf.ln(1)
                pdf.output(str(pdf_file))
            except Exception as e:
                print(f"PDF error: {e}")
        
        return {"markdown": str(md_file), "html": str(html_file), "csv": str(csv_file), "pdf": str(pdf_file) if PDF_AVAILABLE and pdf_file.exists() else None}
