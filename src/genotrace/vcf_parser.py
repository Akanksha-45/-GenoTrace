"""
VCF parsing and basic manipulation utilities for GenoTrace.
Parses VCF files into structured data using pandas.
"""
import os
from typing import Dict, Any, List, Optional
import pandas as pd


class VCFParserError(Exception):
    """Custom exception for VCF parsing errors."""
    pass


# Standard VCF columns
VCF_COLUMNS = [
    '#CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT'
]


def parse_vcf(filepath: str, sample_cols: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Parse a VCF file into a pandas DataFrame.
    
    Args:
        filepath: Path to VCF file
        sample_cols: Optional list of sample column names
        
    Returns:
        DataFrame with VCF records
        
    Raises:
        VCFParserError: If file doesn't exist or parsing fails
    """
    if not os.path.exists(filepath):
        raise VCFParserError(f"File not found: {filepath}")
    
    try:
        # Read VCF, skipping header lines starting with ##
        df = pd.read_csv(filepath, sep='\t', comment='#', header=None)
        
        if df.empty:
            raise VCFParserError(f"No variant records found in {filepath}")
        
        # Assign column names
        if sample_cols:
            cols = VCF_COLUMNS + sample_cols
            df.columns = cols[:len(df.columns)]
        else:
            # Try to infer if there are sample columns
            if len(df.columns) == 8:
                df.columns = VCF_COLUMNS[:8]
            elif len(df.columns) >= 9:
                # Assume FORMAT + samples
                df.columns = VCF_COLUMNS + [f'SAMPLE_{i}' for i in range(len(df.columns) - 9)]
            else:
                df.columns = VCF_COLUMNS[:len(df.columns)]
        
        # Convert POS to numeric
        df['POS'] = pd.to_numeric(df['POS'], errors='coerce')
        df['QUAL'] = pd.to_numeric(df['QUAL'], errors='coerce')
        
        return df
    
    except VCFParserError:
        raise
    except Exception as e:
        raise VCFParserError(f"Error parsing VCF {filepath}: {e}")


def get_vcf_stats(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate basic statistics from VCF DataFrame.
    
    Args:
        df: Parsed VCF DataFrame
        
    Returns:
        Dictionary with statistics
    """
    if df.empty:
        return {}
    
    stats = {
        "total_variants": len(df),
        "chromosomes": df['#CHROM'].nunique(),
        "chrom_counts": df['#CHROM'].value_counts().to_dict(),
        "variant_types": {},
        "qual_stats": {
            "mean": df['QUAL'].mean(),
            "median": df['QUAL'].median(),
            "min": df['QUAL'].min(),
            "max": df['QUAL'].max()
        }
    }
    
    # Classify variant types (SNP, INDEL, etc.)
    for idx, row in df.iterrows():
        ref = str(row['REF'])
        alt = str(row['ALT']).split(',')[0]  # Take first ALT
        if len(ref) == 1 and len(alt) == 1:
            vtype = "SNP"
        elif len(ref) < len(alt):
            vtype = "INS"
        elif len(ref) > len(alt):
            vtype = "DEL"
        else:
            vtype = "MNP/COMPLEX"
        stats["variant_types"][vtype] = stats["variant_types"].get(vtype, 0) + 1
    
    return stats


def extract_info_field(df: pd.DataFrame, field: str) -> pd.Series:
    """
    Extract a specific field from INFO column.
    
    Args:
        df: Parsed VCF DataFrame
        field: INFO field name (e.g., 'DP', 'AF')
        
    Returns:
        Series with extracted values
    """
    def get_field(info_str):
        if pd.isna(info_str):
            return None
        for item in str(info_str).split(';'):
            if '=' in item:
                key, val = item.split('=', 1)
                if key == field:
                    return val
            elif item == field:
                return True
        return None
    
    return df['INFO'].apply(get_field)


def filter_vcf(
    df: pd.DataFrame,
    min_qual: Optional[float] = None,
    min_depth: Optional[int] = None,
    pass_only: bool = False,
    chroms: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Filter VCF DataFrame by various criteria.
    
    Args:
        df: Parsed VCF DataFrame
        min_qual: Minimum QUAL score
        min_depth: Minimum depth (DP) if available
        pass_only: Keep only variants with FILTER == PASS
        chroms: List of chromosomes to keep
        
    Returns:
        Filtered DataFrame
    """
    filtered = df.copy()
    
    if min_qual is not None and 'QUAL' in filtered.columns:
        filtered = filtered[filtered['QUAL'] >= min_qual]
    
    if pass_only and 'FILTER' in filtered.columns:
        filtered = filtered[filtered['FILTER'].isin(['PASS', '.'])]
    
    if chroms is not None and '#CHROM' in filtered.columns:
        filtered = filtered[filtered['#CHROM'].isin(chroms)]
    
    if min_depth is not None:
        dp = extract_info_field(filtered, 'DP')
        dp_numeric = pd.to_numeric(dp, errors='coerce')
        filtered = filtered[dp_numeric >= min_depth]
    
    return filtered.reset_index(drop=True)
