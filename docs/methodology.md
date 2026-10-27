# GenoTrace Methodology

## Overview
This document outlines the methodology and rationale behind GenoTrace's approach to NGS analysis and variant prioritization.

## Pipeline Stages

### 1. Quality Control
- **Tools:** FastQC, MultiQC
- **Metrics:** Per-base quality, per-sequence quality, adapter content, GC content, sequence length distribution
- **Goal:** Identify issues before alignment (adapters, low quality reads)

### 2. Read Alignment
- **Tool:** BWA-MEM
- **Process:** Map short reads to reference genome, generate SAM/BAM
- **Post-processing:** Sort and index with SAMtools
- **Metrics:** Mapping rate, properly paired reads, coverage

### 3. Variant Calling
- **Tool:** FreeBayes (recommended for germline)
- **Output:** VCF format containing SNPs, indels, and other variants
- **Considerations:** Use appropriate ploidy, quality thresholds

### 4. Variant Filtering
Technical filters applied:
- **QUAL:** Minimum variant quality score
- **DP:** Minimum read depth
- **FILTER:** Keep PASS variants when available
- **AO:** Alternate allele observations

### 5. Variant Prioritization
Explainable scoring system:

$$S(v) = w_q Q_{norm}(v) + w_e E(v) + w_f F(v) + w_b B(v)$$

**Components:**
- **Q_norm:** Normalized QUAL score (technical quality)
- **E:** Effect severity based on predicted consequence (LoF > missense > synonymous)
- **F:** Population frequency score (rarer variants scored higher, unknown treated as neutral)
- **B:** Biological relevance (gene annotation presence)

**Weights (default):** quality=0.30, effect=0.40, frequency=0.20, biological=0.10

**Important:** Missing data is treated as unknown/neutral, not penalized. Weights are configurable and must be justified.

## Limitations
- Heuristic prioritization, not validated for clinical use
- Effect predictions depend on annotation quality
- Population frequency data may not be available
- No consideration of compound heterozygosity or complex inheritance without family data
- Tool versions and parameters significantly impact results

## Reproducibility
- All parameters in `config/config.yaml`
- Tool versions should be recorded
- Use checksums for input data
- Document workflow in `workflows/`
- Version control with Git
