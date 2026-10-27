import streamlit as st
import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))
from app import utils
from genotrace import vcf_parser, prioritization

st.set_page_config(page_title="QC & Analysis - GenoTrace", page_icon="🔍", layout="wide")

st.title("🔍 Quality Control & Analysis")
st.markdown(utils.DISCLAIMER)
st.divider()

st.markdown("## Select VCF File for Analysis")

# List available VCF files
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
    st.info(f"Selected: {selected_file}")
    
    try:
        df = vcf_parser.parse_vcf(selected_file)
        st.success(f"✅ Parsed {len(df)} variants")
        
        # Stats
        st.markdown("## Variant Statistics")
        stats = vcf_parser.get_vcf_stats(df)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Variants", stats['total_variants'])
        with col2:
            st.metric("Chromosomes", stats['chromosomes'])
        with col3:
            st.metric("Mean QUAL", f"{stats['qual_stats']['mean']:.2f}")
        with col4:
            st.metric("Variant Types", len(stats['variant_types']))
        
        st.markdown("### Variant Type Distribution")
        st.json(stats['variant_types'])
        
        st.divider()
        
        # Filtering
        st.markdown("## Filtering Options")
        col1, col2, col3 = st.columns(3)
        with col1:
            min_qual = st.slider("Minimum QUAL", 0, 100, 30)
        with col2:
            pass_only = st.checkbox("Keep only PASS variants", value=True)
        with col3:
            min_depth = st.number_input("Minimum Depth (DP)", value=10, min_value=0)
        
        filtered = vcf_parser.filter_vcf(df, min_qual=min_qual, pass_only=pass_only)
        if min_depth > 0:
            from genotrace.vcf_parser import extract_info_field
            dp = extract_info_field(filtered, 'DP')
            dp_num = pd.to_numeric(dp, errors='coerce')
            filtered = filtered[dp_num >= min_depth]
        
        st.success(f"After filtering: {len(filtered)} variants (removed {len(df) - len(filtered)})")
        
        st.divider()
        
        # Prioritization
        st.markdown("## Prioritization")
        if st.button("Run Prioritization", type="primary"):
            with st.spinner("Prioritizing variants..."):
                prioritized = prioritization.prioritize_variants(filtered)
                st.session_state['prioritized_df'] = prioritized
                st.session_state['original_df'] = df
                st.session_state['filtered_df'] = filtered
            st.success("✅ Prioritization complete!")
            st.info("Go to **Variant Explorer** to view results")
        
    except Exception as e:
        st.error(f"Error: {e}")
        st.info("Make sure the file is a valid VCF format")
