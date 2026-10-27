# Clinical Decision Support Workflow

## Purpose
GenoTrace CDS is designed to **assist** qualified medical professionals in reviewing genetic variants. It is **not** a diagnostic tool.

## Research vs Clinical Decision Support

| Aspect | Research Mode | Clinical Decision Support Mode |
|--------|---------------|--------------------------------|
| Purpose | Discovery & learning | Variant review assistance |
| Interpretation | Prioritization ranking | ACMG/AMP classification support |
| Report Style | Summary tables | Hospital-style report with evidence |
| Audience | Students/researchers | Clinicians/geneticists (for review) |
| Approval | None required | Requires institutional oversight for real use |

## ACMG/AMP 2015 (Simplified)
This prototype uses simplified rules based on Richards et al., 2015:

- **PVS1** - Very strong evidence of pathogenicity (loss of function)
- **PM2** - Absent/rare from controls
- **PM1** - Located in mutational hot spot
- **PP3** - Multiple lines of computational evidence
- **BA1** - Allele frequency > 5% in population (standalone benign)
- **BS1** - Allele frequency greater than expected

## Usage

### Generate Clinical Report
```powershell
python scripts/generate_clinical_report.py `
  --vcf data/example/clinical_example.vcf `
  --patient-id PT-XXX-001 `
  --sample-id S-XXX-01 `
  --lab "Your Lab Name" `
  --requested-by "Dr. Name" `
  --outdir results/reports/clinical
```

### Integrated with Pipeline
```powershell
python scripts/run_analysis.py --vcf your.vcf --prioritize --clinical --patient-id PT-XXX-001
```

## Compliance Considerations
- **HIPAA (US)** - Patient data protection
- **DPDP Act 2023 (India)** - Digital personal data protection
- **GDPR (EU)** - Data privacy
- **Local regulations** - Vary by institution/country

## Validation Required
Before any real use: test against GIAB reference samples, review by certified geneticists, audit trail implementation, security assessment.

## Disclaimer
**Final interpretation must be done by qualified professionals. This tool does not diagnose disease.**
