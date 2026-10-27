# GenoTrace NGS Workflow

This document provides step-by-step instructions for running the complete GenoTrace pipeline.

## Prerequisites

### Software
- [FastQC](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/) - Quality control
- [MultiQC](https://multiqc.info/) - Aggregate QC reports
- [BWA](http://bio-bwa.sourceforge.net/) - Read alignment
- [SAMtools](http://www.htslib.org/) - SAM/BAM manipulation
- [FreeBayes](https://github.com/freebayes/freebayes) - Variant calling
- [bcftools](http://www.htslib.org/) - VCF manipulation (optional)
- Python 3.10+ with dependencies from requirements.txt

### Data
- Paired-end FASTQ reads
- Reference genome in FASTA format (matching build)
- Sample metadata

## Workflow Steps

### Step 1: Data Preparation
```bash
# Create working directories
mkdir -p data/raw data/reference results/qc results/variants

# Place files
# data/raw/sample_R1.fastq.gz
# data/raw/sample_R2.fastq.gz
# data/reference/reference.fasta
```

### Step 2: Quality Control
```bash
# Run FastQC on raw reads
fastqc data/raw/sample_R1.fastq.gz data/raw/sample_R2.fastq.gz -o results/qc/fastqc/

# Aggregate with MultiQC
multiqc results/qc/fastqc/ -o results/qc/multiqc/
```

Review reports and assess quality using GenoTrace:
```bash
python scripts/run_analysis.py --help
```

### Step 3: Reference Genome Preparation
```bash
# Index reference with BWA
bwa index data/reference/reference.fasta

# Create FASTA index (optional but useful)
samtools faidx data/reference/reference.fasta
```

### Step 4: Read Alignment
```bash
# Align with BWA MEM
bwa mem -t 4 -R '@RG\tID:sample\tSM:sample\tPL:ILLUMINA' \
  data/reference/reference.fasta \
  data/raw/sample_R1.fastq.gz \
  data/raw/sample_R2.fastq.gz > results/processed/aligned.sam

# Sort and convert to BAM
samtools sort -@ 4 -o results/processed/aligned.sorted.bam results/processed/aligned.sam

# Index BAM
samtools index results/processed/aligned.sorted.bam

# Get alignment statistics
samtools flagstat results/processed/aligned.sorted.bam > results/processed/alignment_stats.txt
```

### Step 5: Variant Calling
```bash
# Call variants with FreeBayes
freebayes -f data/reference/reference.fasta -p 2 --min-coverage 10 -q 20 \
  results/processed/aligned.sorted.bam > results/variants/raw_variants.vcf

# Filter variants (optional with bcftools)
bcftools filter -i 'QUAL>30 && DP>10' results/variants/raw_variants.vcf > results/variants/filtered_variants.vcf
```

### Step 6: GenoTrace Analysis & Prioritization
```bash
# Parse, filter, and prioritize variants
python scripts/run_analysis.py \
  --vcf results/variants/filtered_variants.vcf \
  --prioritize \
  --min-qual 30 \
  --top-n 50 \
  --output results/reports/variant_candidates.csv
```

### Step 7: Generate Report
Use Python API or extend the script:
```python
from genotrace import report, vcf_parser, prioritization
import pandas as pd

# Load results
df = vcf_parser.parse_vcf('results/variants/filtered_variants.vcf')
prioritized = prioritization.prioritize_variants(df)

# Generate reports
summary = {'total_variants': len(df), 'filtered_variants': len(df), 'chromosomes': df['#CHROM'].nunique()}
report.generate_markdown_report(summary, prioritized)
report.generate_html_report(summary, prioritized)
```

## Tips & Notes

- **Use Galaxy for beginners:** If local installation is difficult, use [Galaxy](https://usegalaxy.org/) following the [Galaxy Variant Analysis Tutorial](https://training.galaxyproject.org/training-material/topics/variant-analysis/tutorials/exome-seq/tutorial.html)
- **Match reference builds:** Ensure reads and reference use same genome build
- **Read groups:** Always add read groups for better compatibility
- **Resource requirements:** Whole genome sequencing needs significant compute; start with small exome/small genome datasets
- **Reproducibility:** Record all tool versions and parameters

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Low mapping rate | Check reference build, adapter contamination |
| Few variants called | Check coverage, ploidy settings |
| Many low-quality variants | Adjust filtering thresholds |
| Out of memory | Use fewer threads or process smaller regions |
