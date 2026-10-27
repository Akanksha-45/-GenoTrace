"""
Shared utilities for GenoTrace Streamlit UI
"""
import sys
from pathlib import Path
import os
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from genotrace import sequence_io, vcf_parser, prioritization, acmg_classifier, clinical_report, visualization, report, quality_control, alignment, variant_calling, variant_filter

DATA_DIR = ROOT / "data"
UPLOAD_DIR = DATA_DIR / "uploads"
RESULTS_DIR = ROOT / "results"
REPORTS_DIR = RESULTS_DIR / "reports"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

DISCLAIMER = """
⚠️ **RESEARCH & EDUCATIONAL PROTOTYPE - NOT A DIAGNOSTIC TOOL**  
GenoTrace is a Clinical Decision Support prototype for research and educational purposes only. 
It is NOT intended for clinical diagnosis, treatment, or medical decision making. 
Final interpretation must be performed by a qualified medical geneticist/pathologist.
"""
