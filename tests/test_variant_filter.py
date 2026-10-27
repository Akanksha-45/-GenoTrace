"""Tests for variant_filter module."""
import pandas as pd
from genotrace import variant_filter


def test_apply_quality_filters():
    df = pd.DataFrame({
        '#CHROM': ['chr1', 'chr1', 'chr2'],
        'POS': [100, 200, 300],
        'REF': ['A', 'G', 'T'],
        'ALT': ['T', 'C', 'A'],
        'QUAL': [50, 25, 60],
        'FILTER': ['PASS', 'LowQual', 'PASS'],
        'INFO': ['DP=30', 'DP=10', 'DP=40']
    })
    filtered = variant_filter.apply_quality_filters(df, min_qual=30, pass_only=True)
    assert len(filtered) == 2


def test_apply_variant_type_filter_snp():
    df = pd.DataFrame({
        '#CHROM': ['chr1', 'chr1', 'chr1'],
        'POS': [100, 200, 300],
        'REF': ['A', 'G', 'AT'],
        'ALT': ['T', 'C', 'A'],
        'QUAL': [50, 60, 40]
    })
    filtered = variant_filter.apply_variant_type_filter(df, include_types=['SNP'])
    assert len(filtered) == 2


def test_get_filter_summary():
    before = pd.DataFrame({'A': [1, 2, 3, 4, 5]})
    after = pd.DataFrame({'A': [1, 2, 3]})
    summary = variant_filter.get_filter_summary(before, after)
    assert summary['variants_before'] == 5
    assert summary['variants_after'] == 3
    assert summary['variants_removed'] == 2
    assert summary['retention_rate'] == 60.0
