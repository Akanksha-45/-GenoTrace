#!/usr/bin/env python3
"""
GenoTrace analysis runner script.
Main entry point for running the analysis pipeline.
"""
import argparse
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from genotrace import sequence_io, vcf_parser, prioritization
from genotrace.sequence_io import SequenceIOError
from genotrace.vcf_parser import VCFParserError


def main():
    parser = argparse.ArgumentParser(
        description="GenoTrace: NGS Analysis and Variant Prioritization",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate reference FASTA
  python scripts/run_analysis.py --validate-fasta data/reference/reference.fasta
  
  # Parse and prioritize VCF
  python scripts/run_analysis.py --vcf results/variants/variants.vcf --prioritize
  
  # Get sequence stats
  python scripts/run_analysis.py --fasta data/example/example.fasta --stats
        """
    )
    
    parser.add_argument('--validate-fasta', type=str, help='Validate reference FASTA file')
    parser.add_argument('--fasta', type=str, help='FASTA file to analyze')
    parser.add_argument('--vcf', type=str, help='VCF file to parse')
    parser.add_argument('--prioritize', action='store_true', help='Prioritize variants')
    parser.add_argument('--min-qual', type=float, default=30.0, help='Minimum QUAL for filtering')
    parser.add_argument('--top-n', type=int, default=50, help='Number of top candidates to report')
    parser.add_argument('--output', type=str, help='Output CSV file')
    parser.add_argument('--stats', action='store_true', help='Show statistics')
    
    args = parser.parse_args()
    
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    try:
        # Validate FASTA
        if args.validate_fasta:
            print(f"Validating {args.validate_fasta}...")
            report = sequence_io.validate_reference_fasta(args.validate_fasta)
            print(f"Valid: {report['valid']}")
            if report['stats']:
                print(f"Sequences: {report['stats']['num_sequences']}")
                print(f"Total bases: {report['stats']['total_bases']}")
            if report['errors']:
                for e in report['errors']:
                    print(f"ERROR: {e}")
            if report['warnings']:
                for w in report['warnings']:
                    print(f"WARNING: {w}")
            return
        
        # Analyze FASTA
        if args.fasta and args.stats:
            print(f"Reading {args.fasta}...")
            records = sequence_io.read_fasta(args.fasta)
            stats = sequence_io.get_sequence_stats(records)
            print(f"Sequences: {stats['num_sequences']}")
            print(f"Total bases: {stats['total_bases']}")
            print(f"Length range: {stats['min_length']} - {stats['max_length']}")
            print(f"Mean length: {stats['mean_length']:.2f}")
            return
        
        # Analyze VCF
        if args.vcf:
            print(f"Parsing {args.vcf}...")
            df = vcf_parser.parse_vcf(args.vcf)
            print(f"Parsed {len(df)} variants")
            
            if args.stats:
                stats = vcf_parser.get_vcf_stats(df)
                print(f"\nStatistics:")
                print(f"  Total variants: {stats['total_variants']}")
                print(f"  Chromosomes: {stats['chromosomes']}")
                print(f"  Variant types: {stats['variant_types']}")
                print(f"  Mean QUAL: {stats['qual_stats']['mean']:.2f}")
            
            # Filter
            print(f"\nFiltering (min QUAL={args.min_qual})...")
            filtered = vcf_parser.filter_vcf(df, min_qual=args.min_qual)
            print(f"After filtering: {len(filtered)} variants")
            
            # Prioritize
            if args.prioritize:
                print(f"\nPrioritizing variants...")
                prioritized = prioritization.prioritize_variants(filtered, top_n=args.top_n)
                print(f"Top {len(prioritized)} candidates:\n")
                
                # Display top results
                display_cols = ['rank', '#CHROM', 'POS', 'REF', 'ALT', 'QUAL', 
                               'prioritization_score', 'rationale']
                available_cols = [c for c in display_cols if c in prioritized.columns]
                print(prioritized[available_cols].to_string(index=False))
                
                # Save output
                if args.output:
                    output_path = Path(args.output)
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    prioritized.to_csv(output_path, index=False)
                    print(f"\nSaved results to {output_path}")
                else:
                    default_out = Path("results/reports/variant_candidates.csv")
                    default_out.parent.mkdir(parents=True, exist_ok=True)
                    prioritized.to_csv(default_out, index=False)
                    print(f"\nSaved results to {default_out}")
            return
        
    except (SequenceIOError, VCFParserError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
