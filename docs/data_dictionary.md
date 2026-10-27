# Data Dictionary

## Input Files

### FASTA (Reference/Sequences)
| Field | Description | Example |
|-------|-------------|---------|
| Header | Sequence identifier | `>chr1` or `>scaffold_1` |
| Sequence | Nucleotide sequence (A, T, G, C, N) | `ATGC...` |

### FASTQ (Reads)
| Field | Description | Example |
|-------|-------------|---------|
| @header | Read identifier with optional info | `@SRR123456.1` |
| Sequence | Read sequence | `ATGCNN...` |
| + | Separator | `+` |
| Quality | Phred quality scores | `IIIIII...` |

### VCF (Variants)
| Column | Description | Values |
|--------|-------------|--------|
| #CHROM | Chromosome/scaffold | `chr1`, `1`, etc. |
| POS | 1-based position | Integer |
| ID | Variant identifier | `rs123` or `.` |
| REF | Reference allele | A, T, G, C |
| ALT | Alternate allele(s) | Comma-separated |
| QUAL | Phred-scaled quality score | Float or `.` |
| FILTER | Filter status | `PASS`, `LowQual`, etc. |
| INFO | Semicolon-separated key=value pairs | `DP=50;AF=0.5` |
| FORMAT | Genotype format fields | `GT:DP:AO` |
| SAMPLE | Sample genotype data | `0/1:30:15` |

## Output Files

### variant_candidates.csv
| Column | Description |
|--------|-------------|
| rank | Prioritization rank (1 = highest priority) |
| #CHROM | Chromosome |
| POS | Position |
| REF | Reference allele |
| ALT | Alternate allele |
| QUAL | Variant quality |
| FILTER | Filter status |
| INFO | Original INFO field |
| score_quality | Normalized quality score (0-1) |
| score_effect | Effect severity score (0-1) |
| score_frequency | Frequency score (0-1, higher = rarer) |
| score_biological | Biological relevance score (0-1) |
| prioritization_score | Weighted total score (0-1) |
| rationale | Human-readable explanation |

### QC Summary
| Field | Description |
|-------|-------------|
| sample | Sample name |
| total_sequences | Number of reads |
| sequence_length | Read length |
| %gc | GC content percentage |
| per_base_quality | pass/warn/fail |
| adapter_content | pass/warn/fail |
| overrepresented | pass/warn/fail |

## Configuration Parameters

See `config/config.yaml` for all configurable parameters with descriptions.
