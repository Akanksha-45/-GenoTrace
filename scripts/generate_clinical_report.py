#!/usr/bin/env python3
"""
Generate Clinical Decision Support report from VCF
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from genotrace import vcf_parser, acmg_classifier, clinical_report


def main():
    parser = argparse.ArgumentParser(description="GenoTrace Clinical Decision Support Report Generator")
    parser.add_argument('--vcf', required=True, help='Input VCF file')
    parser.add_argument('--patient-id', default='NOT PROVIDED')
    parser.add_argument('--sample-id', default='NOT PROVIDED')
    parser.add_argument('--lab', default='NOT PROVIDED')
    parser.add_argument('--requested-by', default='NOT PROVIDED')
    parser.add_argument('--outdir', default='results/reports/clinical')
    parser.add_argument('--min-qual', type=float, default=30.0)
    
    args = parser.parse_args()
    
    print("Loading VCF...")
    df = vcf_parser.parse_vcf(args.vcf)
    print(f"Parsed {len(df)} variants")
    
    print("Filtering...")
    filtered = vcf_parser.filter_vcf(df, min_qual=args.min_qual)
    print(f"After filtering: {len(filtered)} variants")
    
    print("Running ACMG classification...")
    clf = acmg_classifier.ACMGClassifier()
    acmg_df = clf.classify_dataframe(filtered)
    
    print("Generating clinical report...")
    generator = clinical_report.ClinicalReportGenerator(args.outdir)
    patient_info = {
        'patient_id': args.patient_id,
        'sample_id': args.sample_id,
        'lab': args.lab,
        'requested_by': args.requested_by
    }
    
    files = generator.generate_report(filtered, acmg_df, patient_info)
    
    print("\nReports generated:")
    for k, v in files.items():
        print(f"  {k}: {v}")
    print("\n[WARNING] RESEARCH & EDUCATIONAL PROTOTYPE - NOT A DIAGNOSTIC TOOL")


if __name__ == '__main__':
    main()
