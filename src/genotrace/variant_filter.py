"""
Variant filtering utilities for GenoTrace.
Advanced filtering logic for variant candidates.
"""
from typing import Dict, Any, List, Optional
import pandas as pd


class VariantFilterError(Exception):
    """Custom exception for variant filtering errors."""
    pass


def apply_quality_filters(
    df: pd.DataFrame,
    min_qual: float = 30.0,
    min_depth: Optional[int] = None,
    pass_only: bool = True
) -> pd.DataFrame:
    """
    Apply quality-based filters.
    
    Args:
        df: VCF DataFrame
        min_qual: Minimum QUAL
        min_depth: Minimum depth
        pass_only: Keep only PASS
        
    Returns:
        Filtered DataFrame
    """
    filtered = df.copy()
    
    if 'QUAL' in filtered.columns:
        filtered = filtered[filtered['QUAL'].fillna(0) >= min_qual]
    
    if pass_only and 'FILTER' in filtered.columns:
        filtered = filtered[filtered['FILTER'].isin(['PASS', '.'])]
    
    if min_depth is not None:
        from .vcf_parser import extract_info_field
        dp = extract_info_field(filtered, 'DP')
        dp_num = pd.to_numeric(dp, errors='coerce')
        filtered = filtered[dp_num >= min_depth]
    
    return filtered.reset_index(drop=True)


def apply_variant_type_filter(
    df: pd.DataFrame,
    include_types: Optional[List[str]] = None,
    exclude_types: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Filter by variant type (SNP, INS, DEL).
    
    Args:
        df: VCF DataFrame
        include_types: Types to include
        exclude_types: Types to exclude
        
    Returns:
        Filtered DataFrame
    """
    filtered = df.copy()
    
    def classify_type(row):
        ref = str(row['REF'])
        alt = str(row['ALT']).split(',')[0]
        if len(ref) == 1 and len(alt) == 1:
            return "SNP"
        elif len(ref) < len(alt):
            return "INS"
        elif len(ref) > len(alt):
            return "DEL"
        else:
            return "MNP"
    
    if 'REF' in filtered.columns and 'ALT' in filtered.columns:
        filtered['_var_type'] = filtered.apply(classify_type, axis=1)
        
        if include_types:
            filtered = filtered[filtered['_var_type'].isin(include_types)]
        if exclude_types:
            filtered = filtered[~filtered['_var_type'].isin(exclude_types)]
        
        filtered = filtered.drop('_var_type', axis=1)
    
    return filtered.reset_index(drop=True)


def apply_chromosome_filter(df: pd.DataFrame, chroms: List[str]) -> pd.DataFrame:
    """
    Filter to specific chromosomes.
    
    Args:
        df: VCF DataFrame
        chroms: List of chromosome names
        
    Returns:
        Filtered DataFrame
    """
    filtered = df.copy()
    if '#CHROM' in filtered.columns:
        filtered = filtered[filtered['#CHROM'].isin(chroms)]
    return filtered.reset_index(drop=True)


def get_filter_summary(before_df: pd.DataFrame, after_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Summarize filtering results.
    
    Args:
        before_df: DataFrame before filtering
        after_df: DataFrame after filtering
        
    Returns:
        Summary dictionary
    """
    return {
        "variants_before": len(before_df),
        "variants_after": len(after_df),
        "variants_removed": len(before_df) - len(after_df),
        "retention_rate": (len(after_df) / len(before_df) * 100) if len(before_df) > 0 else 0
    }
