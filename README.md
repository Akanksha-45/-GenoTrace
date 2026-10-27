# GenoTrace – Explainable VCF-to-ACMG Review Assistant

**GenoTrace** is an offline, open-source Clinical Decision Support (CDS) prototype that turns a raw VCF file into a clean, explainable, and review-ready variant report. Built for biotech/bioinformatics students, lab trainees, and researchers who want a simple way to review variants without logging into paid tools or writing complex CLI commands.

> **For research & educational purposes only. Not a clinical diagnostic tool. Final interpretation must be done by a qualified medical geneticist/pathologist.**

## Key Features

- **VCF-to-Report in one place** – Upload a de-identified VCF and go from raw variants to a review-ready report
- **Explainable Prioritization** – Transparent scoring (Quality + Effect + Frequency + Biological relevance) with rationale for every variant
- **ACMG/AMP Classification (Simplified)** – Evidence codes (PVS1, PM2, PP3, BA1 etc.) with clear reasoning shown
- **Card & Table Views** – Review variants in an easy-to-read card layout or switch to table view
- **Clinical Decision Support Reports** – Generate clean reports in **PDF**, **HTML**, **Markdown** and **CSV**
- **Learn ACMG Hub** – Built-in guide to help students understand classification
- **100% Offline & Private** – Runs locally on your laptop. No login, no API keys, no data upload
- **One-Click Launcher** – Just double-click `start_genotrace.bat` to run

## Tech Stack
- **Language:** Python 3.10+
- **Bioinformatics:** Biopython
- **Data:** pandas, NumPy
- **Viz:** Matplotlib, Seaborn
- **NGS tools (external):** FastQC, MultiQC, BWA, SAMtools, FreeBayes/SnpEff (via Galaxy or CLI)

## Installation

```bash
# Clone repo
git clone https://github.com/yourusername/GenoTrace.git
cd GenoTrace

# Create virtual env (recommended)
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/WSL
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration
Edit `config/config.yaml` with dataset paths, reference genome, and analysis parameters. Keep large data out of git (see `.gitignore`).

### Quick start (Python-first)
```bash
# Validate/reference usage example
python scripts/run_analysis.py --help
```

## Demo Flow
1. **Upload** – Add de-identified `.vcf` file
2. **Analyze** – Filter & prioritize variants
3. **Review** – Explore in Card/Table view with explainable scores
4. **Classify** – Run ACMG review with evidence codes & rationale
5. **Report** – Download PDF/HTML/Markdown/CSV review report

## Workflow Overview
1. **Data acquisition** - Get public FASTQ/FASTA + reference + metadata
2. **QC** - FastQC/MultiQC, inspect quality
3. **Alignment** - BWA mem, sort/index with SAMtools
4. **Variant calling** - FreeBayes/compatible caller → VCF
5. **Analysis** - Parse/filter/summarize with Python
6. **Prioritization** - Explainable ranking with documented criteria
7. **Reporting** - Tables, plots, human-readable report

## Limitations
- Educational/research use only; **no clinical diagnosis**
- Prioritization is heuristic and not a validated clinical scoring system
- Results depend on dataset quality, reference, tools, and parameters
- Missing data is not treated as evidence against a variant

## Resources
- [Biopython Tutorial](https://biopython.org/DIST/docs/tutorial/Tutorial.html)
- [Galaxy Variant Analysis Training](https://training.galaxyproject.org/training-material/topics/variant-analysis/)
- [VCF Specification](https://samtools.github.io/hts-specs/VCFv4.2.pdf)

## License
MIT License (see `LICENSE`)
