# Limitations and Disclaimers

## Important Disclaimers

**RESEARCH AND EDUCATIONAL USE ONLY**  
GenoTrace is designed solely for learning, research, and portfolio purposes. It is **NOT** intended for:
- Clinical diagnosis
- Medical decision making
- Treatment recommendations
- Direct-to-consumer genetic testing interpretation
- Any application where human health decisions depend on results

## Technical Limitations

### Pipeline Limitations
- **Simplified workflow:** Does not implement all best practices from GATK or other gold standards
- **Tool dependencies:** Relies on external command-line tools for alignment/calling
- **Limited error handling:** May not gracefully handle all edge cases
- **No parallel processing optimization:** Basic implementation

### Variant Calling Limitations
- **Germline focus:** Optimized for diploid germline variants, not somatic
- **No structural variants:** Cannot detect large insertions/deletions, inversions, translocations
- **No CNV calling:** Copy number variations not analyzed
- **Limited filtering:** Basic filtering compared to production pipelines

### Prioritization Limitations
- **Heuristic scoring:** Weights are arbitrary defaults, not validated
- **Limited annotation:** Basic effect scoring without full VEP/SnpEff integration
- **No population databases:** Doesn't query gnomAD, dbSNP, ClinVar automatically
- **Missing context:** Doesn't consider inheritance patterns without family data
- **No pathogenicity prediction:** Doesn't use CADD, PolyPhen, SIFT scores
- **Treats unknown as neutral:** Missing data doesn't penalize but also doesn't help prioritize

### Data Limitations
- **Reference dependence:** Results depend heavily on reference genome choice and build
- **Coverage dependent:** Low coverage regions may have unreliable calls
- **Read length/technology:** Designed for short-read Illumina data primarily
- **Batch effects:** No correction for batch effects

## Validation
This tool has not been validated against clinical standards or certified for diagnostic use. Always validate findings with appropriate experimental methods and consult qualified professionals.

## Liability
The authors and contributors accept no liability for any use of this software. Use at your own risk.
