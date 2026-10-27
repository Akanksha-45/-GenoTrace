import streamlit as st

st.set_page_config(page_title="Learn ACMG - GenoTrace", page_icon="📚", layout="wide")

st.title("📚 Learn ACMG/AMP Guidelines")
st.markdown("A simple guide to understand variant classification for educational purposes.")
st.divider()

st.markdown("## Overview")
st.info("The ACMG/AMP 2015 guidelines use a combination of evidence codes to classify variants as Pathogenic, Likely Pathogenic, Uncertain Significance (VUS), Likely Benign, or Benign.")

tab1, tab2, tab3 = st.tabs(["Pathogenic Evidence", "Benign Evidence", "Classification Rules"])

with tab1:
    st.markdown("### Very Strong / Strong / Moderate / Supporting - Pathogenic")
    data = {
        "Code": ["PVS1", "PS1-PS4", "PM1-PM6", "PP1-PP5"],
        "Strength": ["Very Strong", "Strong", "Moderate", "Supporting"],
        "Example": [
            "Loss of function in a gene where LOF is known mechanism",
            "Same amino acid change as established pathogenic variant",
            "Located in mutational hot spot or critical domain",
            "Co-segregation or multiple lines of computational evidence"
        ]
    }
    st.table(data)

with tab2:
    st.markdown("### Benign Evidence")
    data = {
        "Code": ["BA1", "BS1-BS4", "BP1-BP7"],
        "Strength": ["Stand Alone", "Strong", "Supporting"],
        "Example": [
            "Allele frequency > 5% in population",
            "Allele frequency greater than expected for disorder",
            "In silico predicted benign without other evidence"
        ]
    }
    st.table(data)

with tab3:
    st.markdown("### Simplified Classification (GenoTrace CDS)")
    st.markdown("""
    | Classification | Meaning |
    |----------------|---------|
    | **Pathogenic** | Strong evidence supporting disease causation |
    | **Likely Pathogenic** | >90% certainty of being pathogenic |
    | **Uncertain Significance (VUS)** | Not enough evidence to classify clearly |
    | **Likely Benign** | >90% certainty of not being pathogenic |
    | **Benign** | Strong evidence of no harmful effect |
    """)
    st.warning("**Note:** GenoTrace uses a simplified, explainable version for educational purposes. Real classification requires expert review with full clinical context.")

st.divider()
st.caption("Reference: Richards et al., 2015, Genetics in Medicine. 17:405-424")
