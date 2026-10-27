import streamlit as st
import sys
from pathlib import Path
from PIL import Image
import os

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

st.set_page_config(
    page_title="GenoTrace - Explainable Variant Review",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .block-container {
        padding-top: 1.4rem;
        padding-bottom: 2.5rem;
        max-width: 1150px;
    }
    .hero {
        text-align: center;
        padding: 1.8rem 1rem 1.2rem 1rem;
    }
    .hero-title {
        font-size: 2.6rem;
        font-weight: 700;
        color: #1f3b73;
        letter-spacing: -0.5px;
    }
    .hero-subtitle {
        font-size: 1.15rem;
        color: #4f5d75;
        margin-top: -0.3rem;
    }
    .hero-tagline {
        font-size: 0.95rem;
        color: #6c757d;
        margin-top: 0.4rem;
    }
    .disclaimer {
        background-color: #fff7f7;
        border: 1px solid #f5c2c7;
        padding: 0.7rem 1rem;
        border-radius: 8px;
        color: #842029;
        font-size: 0.9rem;
        margin: 1rem 0 1.2rem 0;
    }
    .feature-card {
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        padding: 1.2rem 1.4rem;
        background: #ffffff;
        height: 100%;
        transition: all 0.2s ease-in-out;
    }
    .feature-card:hover {
        border-color: #b6d4fe;
        box-shadow: 0 4px 12px rgba(31, 59, 115, 0.05);
    }
    .feature-title {
        font-size: 1.15rem;
        font-weight: 600;
        color: #1f3b73;
        margin-bottom: 0.3rem;
    }
    .feature-text {
        color: #5f6b7a;
        font-size: 0.95rem;
        margin-bottom: 0.8rem;
    }
    .stButton > button {
        border-radius: 8px;
        height: 2.7rem;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# Banner if exists
banner_path = os.path.join("app", "assets", "genotrace_banner.png")
if os.path.exists(banner_path):
    st.image(Image.open(banner_path), use_container_width=True)
else:
    st.markdown('<div class="hero"><div class="hero-title">🧬 GenoTrace</div><div class="hero-subtitle">Explainable Variant Review for Education & Research</div><div>VCF → Prioritization → ACMG Review → Review-Ready Report | Offline & Open-Source</div></div>', unsafe_allow_html=True)

st.markdown("""
<div class="disclaimer">
<b>⚠️ RESEARCH & EDUCATIONAL PROTOTYPE - NOT A DIAGNOSTIC TOOL</b> &nbsp;|&nbsp; For research & educational use only &nbsp;|&nbsp; Not for clinical diagnosis or treatment &nbsp;|&nbsp; Final interpretation by a qualified medical geneticist/pathologist
</div>
""", unsafe_allow_html=True)

st.divider()

st.markdown("### Workflow")
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown("**1)** Upload de-identified VCF")
with c2:
    st.markdown("**2)** Filter & Prioritize")
with c3:
    st.markdown("**3)** Review with ACMG")
with c4:
    st.markdown("**4)** Download Report (PDF / HTML / CSV)")

st.divider()

col1, col2, col3, col4 = st.columns(4, gap="medium")

with col1:
    st.markdown('<div class="feature-card"><div class="feature-title">📁 Upload Data</div><div class="feature-text">Upload de-identified VCF or FASTA files to begin your review.</div></div>', unsafe_allow_html=True)
    if st.button("Get Started", use_container_width=True, key="home_upload"):
        st.switch_page("pages/1_Upload_Data.py")

with col2:
    st.markdown('<div class="feature-card"><div class="feature-title">🧬 Variant Explorer</div><div class="feature-text">Review prioritized variants in clean Card or Table view with rationale.</div></div>', unsafe_allow_html=True)
    if st.button("Review Variants", use_container_width=True, key="home_explore"):
        st.switch_page("pages/3_Variant_Explorer.py")

with col3:
    st.markdown('<div class="feature-card"><div class="feature-title">🏥 Clinical Decision Support</div><div class="feature-text">Run explainable ACMG classification and generate review-ready reports.</div></div>', unsafe_allow_html=True)
    if st.button("ACMG Review", use_container_width=True, key="home_cds"):
        st.switch_page("pages/4_Clinical_Decision_Support.py")

with col4:
    st.markdown('<div class="feature-card"><div class="feature-title">📚 Learn ACMG</div><div class="feature-text">Understand evidence codes with simple, student-friendly explanations.</div></div>', unsafe_allow_html=True)
    if st.button("Learn Now", use_container_width=True, key="home_learn"):
        st.switch_page("pages/7_Learn_ACMG.py")

st.divider()

st.markdown("### Highlights")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**🔒 Offline & Private**  \nRuns locally, no login required")
with col2:
    st.markdown("**💡 Explainable**  \nClear rationale for scores & ACMG evidence")
with col3:
    st.markdown("**🎓 Student-Friendly**  \nLearn while reviewing variants")
