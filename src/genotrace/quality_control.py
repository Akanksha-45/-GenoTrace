"""
Quality control utilities for GenoTrace.
Provides helpers for summarizing FastQC reports and QC metrics.
"""
import os
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
import pandas as pd


class QCError(Exception):
    """Custom exception for QC errors."""
    pass


def summarize_fastqc_data(fastqc_data_file: str) -> Dict[str, Any]:
    """
    Parse FastQC data.txt file and extract key metrics.
    
    Args:
        fastqc_data_file: Path to fastqc_data.txt
        
    Returns:
        Dictionary with QC summary
    """
    if not os.path.exists(fastqc_data_file):
        raise QCError(f"File not found: {fastqc_data_file}")
    
    summary = {
        "basic_stats": {},
        "per_base_quality": "unknown",
        "per_sequence_quality": "unknown",
        "per_base_n_content": "unknown",
        "sequence_length_distribution": "unknown",
        "sequence_duplication_levels": "unknown",
        "overrepresented_sequences": "unknown",
        "adapter_content": "unknown"
    }
    
    try:
        with open(fastqc_data_file, 'r') as f:
            content = f.read()
        
        # Extract basic statistics
        if ">>Basic Statistics" in content:
            lines = content.split(">>Basic Statistics")[1].split(">>")[0]
            for line in lines.split('\n'):
                if '\t' in line and not line.startswith('>>'):
                    parts = line.split('\t')
                    if len(parts) >= 2:
                        key = parts[0].strip()
                        val = parts[1].strip()
                        summary["basic_stats"][key] = val
        
        # Extract module statuses
        modules = [
            "Per base sequence quality",
            "Per sequence quality scores",
            "Per base N content",
            "Sequence Length Distribution",
            "Sequence Duplication Levels",
            "Overrepresented sequences",
            "Adapter Content"
        ]
        
        for mod in modules:
            if f">>{mod}" in content:
                section = content.split(f">>{mod}")[1].split(">>END_MODULE")[0]
                # Look for pass/warn/fail
                for line in section.split('\n'):
                    if line.strip() in ['pass', 'warn', 'fail']:
                        key = mod.lower().replace(' ', '_')
                        summary[key] = line.strip()
                        break
        
        return summary
    
    except Exception as e:
        raise QCError(f"Error parsing FastQC data: {e}")


def generate_qc_summary_table(qc_results: List[Dict[str, Any]], output_file: str) -> None:
    """
    Generate a summary table from multiple QC results.
    
    Args:
        qc_results: List of QC result dictionaries
        output_file: Path to output CSV
    """
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    
    rows = []
    for qc in qc_results:
        row = {
            "sample": qc.get("sample_name", "unknown"),
            "total_sequences": qc.get("basic_stats", {}).get("Total Sequences", "N/A"),
            "sequence_length": qc.get("basic_stats", {}).get("Sequence length", "N/A"),
            "%gc": qc.get("basic_stats", {}).get("%GC", "N/A"),
            "per_base_quality": qc.get("per_base_sequence_quality", "unknown"),
            "adapter_content": qc.get("adapter_content", "unknown"),
            "overrepresented": qc.get("overrepresented_sequences", "unknown")
        }
        rows.append(row)
    
    df = pd.DataFrame(rows)
    df.to_csv(output_file, index=False)


def assess_read_quality(qc_summary: Dict[str, Any]) -> Dict[str, Any]:
    """
    Assess overall read quality and provide recommendations.
    
    Args:
        qc_summary: QC summary dictionary
        
    Returns:
        Assessment with status and recommendations
    """
    assessment = {
        "overall_status": "pass",
        "issues": [],
        "recommendations": []
    }
    
    # Check critical modules
    if qc_summary.get("per_base_sequence_quality") == "fail":
        assessment["issues"].append("Per-base sequence quality failed")
        assessment["recommendations"].append("Consider trimming low-quality bases")
        assessment["overall_status"] = "fail"
    elif qc_summary.get("per_base_sequence_quality") == "warn":
        assessment["issues"].append("Per-base sequence quality warning")
        assessment["recommendations"].append("Review trimming options")
        if assessment["overall_status"] == "pass":
            assessment["overall_status"] = "warn"
    
    if qc_summary.get("adapter_content") in ["fail", "warn"]:
        assessment["issues"].append(f"Adapter content: {qc_summary.get('adapter_content')}")
        assessment["recommendations"].append("Perform adapter trimming")
        if assessment["overall_status"] == "pass":
            assessment["overall_status"] = "warn"
    
    if qc_summary.get("overrepresented_sequences") == "fail":
        assessment["issues"].append("Overrepresented sequences detected")
        assessment["recommendations"].append("Investigate contamination or adapters")
        if assessment["overall_status"] == "pass":
            assessment["overall_status"] = "warn"
    
    if not assessment["issues"]:
        assessment["recommendations"].append("Quality looks good - proceed to alignment")
    
    return assessment
