import streamlit as st
import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))
from app import utils

st.set_page_config(page_title="Variant Explorer - GenoTrace", page_icon="🧬", layout="wide")

st.title("🧬 Variant Explorer | Explainable Review")
st.markdown(utils.DISCLAIMER)
st.divider()

if 'prioritized_df' not in st.session_state:
    st.warning("No analysis results found. Please run analysis first.")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Go to QC & Analysis"):
            st.switch_page("pages/2_QC_&_Analysis.py")
    with col2:
        if st.button("Go to Upload"):
            st.switch_page("pages/1_Upload_Data.py")
    st.stop()

df = st.session_state['prioritized_df']

# Filters
col1, col2, col3, col4 = st.columns(4)
with col1:
    chroms = ['All'] + sorted(df['#CHROM'].unique().tolist())
    selected_chrom = st.selectbox("Chromosome", chroms)
with col2:
    if 'FILTER' in df.columns:
        filters = ['All'] + sorted(df['FILTER'].unique().tolist())
        selected_filter = st.selectbox("Filter", filters)
    else:
        selected_filter = 'All'
with col3:
    min_qual = st.number_input("Min QUAL", value=0.0)
with col4:
    top_n = st.number_input("Show Top N", value=min(50, len(df)), min_value=1, max_value=len(df))

# Apply filters
filtered_df = df.copy()
if selected_chrom != 'All':
    filtered_df = filtered_df[filtered_df['#CHROM'] == selected_chrom]
if selected_filter != 'All' and 'FILTER' in filtered_df.columns:
    filtered_df = filtered_df[filtered_df['FILTER'] == selected_filter]
if 'QUAL' in filtered_df.columns:
    filtered_df = filtered_df[pd.to_numeric(filtered_df['QUAL'], errors='coerce') >= min_qual]
filtered_df = filtered_df.head(int(top_n))

st.markdown(f"**Showing {len(filtered_df)} of {len(df)} variants**")

view = st.radio("View Mode", ["Card View (Recommended)", "Table View"], horizontal=True)

if view == "Card View (Recommended)":
    for idx, row in filtered_df.iterrows():
        with st.container():
            st.markdown(f"### Variant #{row.get('rank', idx+1)} | {row.get('#CHROM')}:{row.get('POS')} {row.get('REF')} > {row.get('ALT')}")
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.metric("QUAL", row.get('QUAL'))
            with c2:
                st.metric("Prioritization Score", f"{row.get('prioritization_score', 0):.3f}")
            with c3:
                st.metric("FILTER", row.get('FILTER'))
            with c4:
                st.metric("Type", "SNP/INDEL")
            st.markdown(f"**Why prioritized:** {row.get('rationale', 'N/A')}")
            st.markdown("**Scores:** Quality: %.2f | Effect: %.2f | Frequency: %.2f | Biological: %.2f" % 
                       (row.get('score_quality',0), row.get('score_effect',0), row.get('score_frequency',0), row.get('score_biological',0)))
            st.divider()
else:
    display_cols = ['rank', '#CHROM', 'POS', 'REF', 'ALT', 'QUAL', 'FILTER', 
                    'prioritization_score', 'rationale']
    available_cols = [c for c in display_cols if c in filtered_df.columns]
    st.dataframe(filtered_df[available_cols], use_container_width=True, hide_index=True)

st.divider()
col1, col2 = st.columns(2)
with col1:
    csv = filtered_df.to_csv(index=False)
    st.download_button("📥 Download Filtered Results (CSV)", csv, "genotrace_filtered_variants.csv", "text/csv", use_container_width=True)
with col2:
    if st.button("Proceed to Clinical Decision Support", use_container_width=True):
        st.switch_page("pages/4_Clinical_Decision_Support.py")
