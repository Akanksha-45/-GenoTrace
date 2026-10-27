import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))
from app import utils
from genotrace import vcf_parser, acmg_classifier, clinical_report

st.set_page_config(page_title="Clinical Decision Support - GenoTrace", page_icon="🏥", layout="wide")

st.title("🏥 Clinical Decision Support (CDS)")
st.markdown(utils.DISCLAIMER)
st.divider()

st.markdown("## Patient & Sample Information")
col1, col2, col3, col4 = st.columns(4)
with col1:
    patient_id = st.text_input("Patient ID", value="DEMO-001", help="Use de-identified ID only")
with col2:
    sample_id = st.text_input("Sample ID", value="S-001")
with col3:
    lab = st.text_input("Laboratory", value="Demo Genetics Lab")
with col4:
    requested_by = st.text_input("Requested By", value="Dr. Demo")

st.divider()

st.markdown("## Select VCF File")

vcf_files = []
for pattern in ['*.vcf']:
    vcf_files.extend(list(utils.UPLOAD_DIR.glob(pattern)))
    vcf_files.extend(list((Path(__file__).parent.parent.parent / 'data/example').glob(pattern)))
    vcf_files.extend(list((Path(__file__).parent.parent.parent / 'data/own').glob(pattern)))

vcf_files = sorted(set(vcf_files))
file_options = {str(f): f.name for f in vcf_files}

if not file_options:
    st.warning("No VCF files found. Please upload a VCF file first.")
    if st.button("Go to Upload"):
        st.switch_page("pages/1_Upload_Data.py")
    st.stop()

selected_file = st.selectbox("Choose VCF file", options=list(file_options.keys()), format_func=lambda x: file_options[x])

if selected_file:
    if st.button("Run ACMG Classification & Generate Clinical Report", type="primary", use_container_width=True):
        with st.spinner("Processing... This may take a moment"):
            try:
                df = vcf_parser.parse_vcf(selected_file)
                filtered = vcf_parser.filter_vcf(df, min_qual=30)
                
                clf = acmg_classifier.ACMGClassifier()
                acmg_df = clf.classify_dataframe(filtered)
                
                generator = clinical_report.ClinicalReportGenerator(str(utils.REPORTS_DIR / "clinical"))
                patient_info = {
                    'patient_id': patient_id,
                    'sample_id': sample_id,
                    'lab': lab,
                    'requested_by': requested_by
                }
                
                files = generator.generate_report(filtered, acmg_df, patient_info)
                
                st.session_state['acmg_df'] = acmg_df
                st.session_state['clinical_files'] = files
                st.session_state['clinical_merged'] = filtered.merge(
                    acmg_df[['POS', 'classification', 'evidence_codes', 'rationale']], 
                    on='POS', how='left'
                )
                
                st.success("✅ Clinical report generated successfully!")
            except Exception as e:
                st.error(f"Error: {e}")

if 'clinical_merged' in st.session_state:
    st.divider()
    st.markdown("## ACMG Classification Results")
    
    acmg_merged = st.session_state['clinical_merged']
    st.dataframe(acmg_merged, use_container_width=True, hide_index=True)
    
    st.divider()
    st.markdown("## Download Reports")
    
    if 'clinical_files' in st.session_state:
        files = st.session_state['clinical_files']
        col1, col2, col3 = st.columns(3)
        with col1:
            with open(files['html'], 'r', encoding='utf-8') as f:
                st.download_button(
                    "📥 Download HTML Report",
                    f.read(),
                    file_name=Path(files['html']).name,
                    mime="text/html",
                    use_container_width=True
                )
        with col2:
            with open(files['markdown'], 'r', encoding='utf-8') as f:
                st.download_button(
                    "📥 Download Markdown Report",
                    f.read(),
                    file_name=Path(files['markdown']).name,
                    mime="text/markdown",
                    use_container_width=True
                )
        with col3:
            with open(files['csv'], 'r', encoding='utf-8') as f:
                st.download_button(
                    "📥 Download CSV with ACMG",
                    f.read(),
                    file_name=Path(files['csv']).name,
                    mime="text/csv",
                    use_container_width=True
                )
        
        st.info(f"Reports saved to: {utils.REPORTS_DIR / 'clinical'}")
    
    st.warning("**Remember:** Final interpretation must be performed by a qualified medical geneticist/pathologist. This is not a diagnostic tool.")
