import streamlit as st
import sys
from pathlib import Path
import os

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))
from app import utils

st.set_page_config(page_title="Reports & Downloads - GenoTrace", page_icon="📊", layout="wide")

st.title("📊 Reports & Downloads")
st.markdown(utils.DISCLAIMER)
st.divider()

st.markdown("## Available Reports")

# List all files in results
reports_dir = utils.REPORTS_DIR
all_files = []
for root, dirs, files in os.walk(reports_dir):
    for file in files:
        if file.endswith(('.csv', '.html', '.md', '.txt')):
            full_path = Path(root) / file
            all_files.append({
                'name': file,
                'path': full_path,
                'size': f"{full_path.stat().st_size / 1024:.2f} KB",
                'type': full_path.suffix
            })

if not all_files:
    st.info("No reports generated yet. Run an analysis to generate reports.")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Go to QC & Analysis"):
            st.switch_page("pages/2_QC_&_Analysis.py")
    with col2:
        if st.button("Go to Clinical CDS"):
            st.switch_page("pages/4_Clinical_Decision_Support.py")
    with col3:
        if st.button("Go to Upload"):
            st.switch_page("pages/1_Upload_Data.py")
    st.stop()

# Group by type
csv_files = [f for f in all_files if f['type'] == '.csv']
html_files = [f for f in all_files if f['type'] == '.html']
md_files = [f for f in all_files if f['type'] == '.md']

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📄 CSV Files")
    for f in csv_files:
        st.markdown(f"**{f['name']}** ({f['size']})")
        with open(f['path'], 'r', encoding='utf-8') as file:
            st.download_button(
                "Download",
                file.read(),
                file_name=f['name'],
                mime="text/csv",
                key=f"csv_{f['name']}"
            )
        st.divider()

with col2:
    st.markdown("### 🌐 HTML Reports")
    for f in html_files:
        st.markdown(f"**{f['name']}** ({f['size']})")
        with open(f['path'], 'r', encoding='utf-8') as file:
            st.download_button(
                "Download",
                file.read(),
                file_name=f['name'],
                mime="text/html",
                key=f"html_{f['name']}"
            )
        st.divider()

with col3:
    st.markdown("### 📝 Markdown Reports")
    for f in md_files:
        st.markdown(f"**{f['name']}** ({f['size']})")
        with open(f['path'], 'r', encoding='utf-8') as file:
            st.download_button(
                "Download",
                file.read(),
                file_name=f['name'],
                mime="text/markdown",
                key=f"md_{f['name']}"
            )
        st.divider()

st.divider()
st.info(f"📁 All reports are stored in: `{reports_dir}`")
