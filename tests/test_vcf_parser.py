"""Tests for vcf_parser module."""
import os
import tempfile
import pandas as pd
from genotrace import vcf_parser


def test_filter_vcf_pass_only():
    # Create a simple VCF DataFrame
    df = pd.DataFrame({
        '#CHROM': ['chr1', 'chr1', 'chr2'],
        'POS': [100, 200, 300],
        'ID': ['.', '.', '.'],
        'REF': ['A', 'G', 'T'],
        'ALT': ['T', 'C', 'A'],
        'QUAL': [50, 25, 60],
        'FILTER': ['PASS', 'LowQual', 'PASS'],
        'INFO': ['DP=30', 'DP=10', 'DP=40']
    })
    filtered = vcf_parser.filter_vcf(df, pass_only=True)
    assert len(filtered) == 2
    assert all(f == 'PASS' for f in filtered['FILTER'])


def test_filter_vcf_min_qual():
    df = pd.DataFrame({
        '#CHROM': ['chr1', 'chr1'],
        'POS': [100, 200],
        'ID': ['.', '.'],
        'REF': ['A', 'G'],
        'ALT': ['T', 'C'],
        'QUAL': [50, 25],
        'FILTER': ['PASS', 'PASS'],
        'INFO': ['DP=30', 'DP=20']
    })
    filtered = vcf_parser.filter_vcf(df, min_qual=30)
    assert len(filtered) == 1
    assert filtered.iloc[0]['POS'] == 100


def test_get_vcf_stats():
    df = pd.DataFrame({
        '#CHROM': ['chr1', 'chr1', 'chr2'],
        'POS': [100, 200, 300],
        'ID': ['.', '.', '.'],
        'REF': ['A', 'G', 'AT'],
        'ALT': ['T', 'C', 'A'],
        'QUAL': [50, 60, 40],
        'FILTER': ['PASS', 'PASS', 'PASS'],
        'INFO': ['DP=30', 'DP=40', 'DP=20']
    })
    stats = vcf_parser.get_vcf_stats(df)
    assert stats['total_variants'] == 3
    assert stats['chromosomes'] == 2
    assert 'SNP' in stats['variant_types']
    assert 'DEL' in stats['variant_types']
