import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))
from app import utils

st.set_page_config(page_title="About & Limitations - GenoTrace", page_icon="ℹ️", layout="wide")

st.title("ℹ️ About & Limitations")
st.markdown(utils.DISCLAIMER)
st.divider()

st.markdown("## About GenoTrace")
st.markdown("""
**GenoTrace** is an End-to-End NGS Analysis and Genomic Variant Prioritization Platform with Clinical Decision Support capabilities. 

It is designed for:
- **Learning** - Understanding NGS workflows and variant analysis
- **Research** - Exploring and prioritizing genetic variants
- **Portfolio** - Demonstrating bioinformatics skills
- **Clinical Decision Support (Prototype)** - Assisting experts in variant review
""")

st.divider()

st.markdown("## Research vs Clinical Decision Support")
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    ### Research Mode
    - Variant parsing and filtering
    - Explainable prioritization scoring
    - Ranked candidate lists
    - CSV/summary outputs
    - For learning and exploration
    """)
with col2:
    st.markdown("""
    ### Clinical Decision Support Mode
    - ACMG/AMP 2015 classification (simplified)
    - Evidence code assignment
    - Hospital-style clinical reports
    - Patient/sample tracking
    - For assisting qualified experts only
    """)

st.divider()

st.markdown("## Privacy & Security")
st.markdown("""
- **Local Processing** - All data is processed on your local machine
- **De-identified Data Only** - Never use real patient names or MRNs
- **No Cloud Upload** - Files are not sent to external servers
- **Git Ignored** - Uploads and results are excluded from version control
""")

st.divider()

st.markdown("## Limitations")
st.markdown("""
- **Not Diagnostic** - Cannot diagnose diseases or make treatment decisions
- **Simplified ACMG** - Educational implementation, not complete per guidelines
- **Limited Annotation** - No full ClinVar/gnomAD integration
- **External Tools Required** - FASTQ/BAM need BWA/SAMtools/variant callers
- **Single-sample Focused** - Best for single-sample VCF analysis
- **Requires Expert Review** - All results must be interpreted by qualified professionals
""")

st.divider()

st.markdown("## Resources")
st.markdown("""
- [Biopython Documentation](https://biopython.org/)
- [Galaxy Variant Analysis Tutorials](https://training.galaxyproject.org/training-material/topics/variant-analysis/)
- [ACMG/AMP Guidelines](https://www.acmg.net/)
- [VCF Format Specification](https://samtools.github.io/hts-specs/VCFv4.2.pdf)
""")

st.divider()
st.markdown("**Version:** 0.2.0 | **License:** MIT | **For Research & Educational Use Only**")
