import streamlit as st
import sys
from pathlib import Path
import os
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))
from app import utils

st.set_page_config(page_title="Upload Data - GenoTrace", page_icon="📁", layout="wide")

st.title("📁 Upload Data")
st.markdown(utils.DISCLAIMER)
st.divider()

st.markdown("## Supported File Formats")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.success("**VCF (.vcf)**\n✅ Fully Supported")
with col2:
    st.info("**FASTA (.fasta)**\n✅ Supported")
with col3:
    st.warning("**FASTQ (.fastq, .fq)**\n⚠️ Needs external tools")
with col4:
    st.warning("**BAM/SAM**\n⚠️ Convert to VCF first")

st.divider()

st.markdown("## Upload Your Files")
st.info("**Note:** Use de-identified data only. Files are stored locally in `data/uploads/`")

uploaded_files = st.file_uploader(
    "Choose files",
    type=['vcf', 'fasta', 'fa', 'fastq', 'fq', 'gz'],
    accept_multiple_files=True,
    help="Upload VCF files for analysis. FASTQ/BAM require external processing first."
)

if uploaded_files:
    st.markdown("### Uploaded Files")
    for uploaded_file in uploaded_files:
        file_details = {
            "Filename": uploaded_file.name,
            "File type": uploaded_file.type,
            "File size": f"{uploaded_file.size / 1024:.2f} KB"
        }
        st.json(file_details)
        
        # Save file
        save_path = utils.UPLOAD_DIR / uploaded_file.name
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"✅ Saved to {save_path}")
    
    st.divider()
    st.markdown("### Next Steps")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Go to QC & Analysis", use_container_width=True):
            st.switch_page("pages/2_QC_&_Analysis.py")
    with col2:
        if st.button("Go to Variant Explorer", use_container_width=True):
            st.switch_page("pages/3_Variant_Explorer.py")
    with col3:
        if st.button("Go to Clinical CDS", use_container_width=True):
            st.switch_page("pages/4_Clinical_Decision_Support.py")

st.divider()

st.markdown("## Guidelines")
st.markdown("""
- **VCF files are recommended** - Best for direct analysis with GenoTrace
- **Use de-identified data** - Remove patient names, MRNs, and identifying information
- **Single-sample VCFs work best** - Multi-sample VCFs are supported but ACMG reports are optimized for single samples
- **FASTQ files** - Need QC, alignment (BWA), and variant calling (FreeBayes/GATK) first. See [workflows/ngs_workflow.md](../workflows/ngs_workflow.md)
- **All processing is local** - Files never leave your computer
""")
