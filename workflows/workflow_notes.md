# Workflow Notes

## Design Decisions

### Why this structure?
- **Modular design:** Each step in separate module for maintainability and testing
- **Explainable prioritization:** Transparency is key - users see why variants are ranked
- **Research-focused:** Clear disclaimers, limitations documented
- **Python-first:** Easy to extend and integrate with data science tools
- **Hybrid approach:** Uses external NGS tools (industry standard) + Python analysis layer

### Tool Choices

| Tool | Rationale |
|------|-----------|
| BWA | Fast, accurate for short reads, widely used |
| FreeBayes | Good for germline variant calling, easy to use, open source |
| Biopython | Excellent for sequence manipulation in Python |
| pandas | Great for tabular variant data manipulation |

### Prioritization Philosophy
- **Technical quality matters:** Low-quality variants filtered first
- **Effect severity weighted heavily:** LoF variants get highest effect scores
- **Rarity considered:** Rare variants often more interesting for investigation
- **Uncertainty acknowledged:** Missing data doesn't penalize
- **Not diagnostic:** Explicitly not for clinical use

## Known Limitations
- No structural variant calling
- No CNV analysis
- Limited annotation integration (can be extended)
- Prioritization weights are arbitrary defaults
- No haplotype phasing
- Population frequency requires external databases

## Future Improvements
- Integrate VEP/SnpEff annotations
- Add population frequency from gnomAD API
- Implement more sophisticated scoring
- Add support for multi-sample VCFs
- Create interactive visualizations
- Add automated testing with real data

## Learning Resources
- [Galaxy Training Network](https://training.galaxyproject.org/) - Hands-on tutorials
- [Biostars](https://www.biostars.org/) - Q&A community
- [GATK Best Practices](https://gatk.broadinstitute.org/hc/en-us/sections/360007226651-Best-Practices) - Industry standards
- [VCFtools](https://vcftools.github.io/) - VCF manipulation reference
