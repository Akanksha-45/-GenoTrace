"""
Variant prioritization module for GenoTrace.
Implements explainable scoring and ranking of candidate variants.
"""
from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np


class PrioritizationError(Exception):
    """Custom exception for prioritization errors."""
    pass


# Effect severity scores (higher = more severe)
EFFECT_SCORES = {
    "stop_gained": 1.0,
    "stop_lost": 0.95,
    "start_lost": 0.95,
    "splice_donor_variant": 0.95,
    "splice_acceptor_variant": 0.95,
    "frameshift_variant": 0.9,
    "missense_variant": 0.6,
    "inframe_insertion": 0.5,
    "inframe_deletion": 0.5,
    "protein_altering_variant": 0.5,
    "synonymous_variant": 0.1,
    "intron_variant": 0.05,
    "intergenic_variant": 0.01,
    "upstream_gene_variant": 0.02,
    "downstream_gene_variant": 0.02,
    "5_prime_UTR_variant": 0.1,
    "3_prime_UTR_variant": 0.1,
    "unknown": 0.0
}


def normalize_qual(qual: float, max_qual: float = 100.0) -> float:
    """
    Normalize QUAL score to 0-1 range.
    
    Args:
        qual: Raw QUAL value
        max_qual: Maximum expected QUAL for normalization
        
    Returns:
        Normalized score (0-1)
    """
    if pd.isna(qual) or qual < 0:
        return 0.0
    score = qual / max_qual
    return min(max(score, 0.0), 1.0)


def score_effect(consequence: str) -> float:
    """
    Score variant effect based on predicted consequence.
    
    Args:
        consequence: Variant consequence/annotation
        
    Returns:
        Effect score (0-1)
    """
    if pd.isna(consequence) or consequence == "":
        return 0.0
    
    consequence_lower = str(consequence).lower()
    
    # Check for exact matches
    for key, score in EFFECT_SCORES.items():
        if key in consequence_lower:
            return score
    
    return 0.0


def score_frequency(af: Optional[float]) -> float:
    """
    Score based on population allele frequency.
    Rare variants get higher scores (potentially more interesting).
    
    Args:
        af: Allele frequency (0-1)
        
    Returns:
        Frequency score (0-1), higher for rarer variants
    """
    if af is None or pd.isna(af):
        return 0.5  # Unknown - neutral score (not penalized)
    
    af = float(af)
    if af < 0 or af > 1:
        return 0.5
    
    # Inverse scoring: rarer = higher score
    if af < 0.001:  # Very rare
        return 1.0
    elif af < 0.01:  # Rare
        return 0.8
    elif af < 0.05:  # Low frequency
        return 0.6
    elif af < 0.1:   # Common
        return 0.3
    else:  # Very common
        return 0.1


def score_biological_relevance(gene: Optional[str], evidence: Optional[Dict] = None) -> float:
    """
    Score biological relevance based on gene/pathway information.
    
    Args:
        gene: Gene symbol
        evidence: Additional evidence dictionary
        
    Returns:
        Biological relevance score (0-1)
    """
    if gene is None or pd.isna(gene) or gene == "":
        return 0.0
    
    # Basic scoring - can be extended with known gene lists
    score = 0.3  # Base score for having gene annotation
    
    if evidence:
        if evidence.get("known_disease_gene"):
            score += 0.4
        if evidence.get("pathway_relevant"):
            score += 0.3
    
    return min(score, 1.0)


def prioritize_variants(
    df: pd.DataFrame,
    weights: Optional[Dict[str, float]] = None,
    top_n: Optional[int] = None
) -> pd.DataFrame:
    """
    Prioritize variants using explainable scoring.
    
    Args:
        df: DataFrame with variant information
        weights: Scoring weights dict
        top_n: Return only top N variants
        
    Returns:
        DataFrame with prioritization scores and rankings
    """
    if df.empty:
        return df.copy()
    
    # Default weights
    if weights is None:
        weights = {
            "quality": 0.30,
            "effect": 0.40,
            "frequency": 0.20,
            "biological": 0.10
        }
    
    result = df.copy()
    
    # Calculate component scores
    result['score_quality'] = result['QUAL'].apply(normalize_qual)
    
    # Effect score - look for common annotation columns
    if 'consequence' in result.columns:
        result['score_effect'] = result['consequence'].apply(score_effect)
    elif 'INFO' in result.columns:
        # Try to extract effect from INFO if annotated
        result['score_effect'] = 0.3  # Default moderate score
    else:
        result['score_effect'] = 0.0
    
    # Frequency score
    if 'AF' in result.columns:
        af_vals = pd.to_numeric(result['AF'], errors='coerce')
        result['score_frequency'] = af_vals.apply(score_frequency)
    elif 'MAF' in result.columns:
        maf_vals = pd.to_numeric(result['MAF'], errors='coerce')
        result['score_frequency'] = maf_vals.apply(score_frequency)
    else:
        result['score_frequency'] = 0.5  # Unknown
    
    # Biological relevance
    if 'GENE' in result.columns or 'gene' in result.columns:
        gene_col = 'GENE' if 'GENE' in result.columns else 'gene'
        result['score_biological'] = result[gene_col].apply(
            lambda g: score_biological_relevance(g)
        )
    else:
        result['score_biological'] = 0.0
    
    # Calculate weighted total score
    result['prioritization_score'] = (
        weights.get('quality', 0.3) * result['score_quality'] +
        weights.get('effect', 0.4) * result['score_effect'] +
        weights.get('frequency', 0.2) * result['score_frequency'] +
        weights.get('biological', 0.1) * result['score_biological']
    )
    
    # Sort by score descending
    result = result.sort_values('prioritization_score', ascending=False).reset_index(drop=True)
    result['rank'] = result.index + 1
    
    # Add explanation
    result['rationale'] = result.apply(_generate_rationale, axis=1)
    
    if top_n is not None:
        result = result.head(top_n)
    
    return result


def _generate_rationale(row) -> str:
    """
    Generate human-readable rationale for prioritization.
    
    Args:
        row: DataFrame row with scores
        
    Returns:
        Rationale string
    """
    reasons = []
    
    if row['score_quality'] >= 0.7:
        reasons.append("high variant quality")
    if row['score_effect'] >= 0.7:
        reasons.append("potentially high-impact effect")
    elif row['score_effect'] >= 0.5:
        reasons.append("moderate predicted effect")
    if row['score_frequency'] >= 0.8:
        reasons.append("rare in population")
    elif row['score_frequency'] <= 0.2:
        reasons.append("common variant (lower priority)")
    if row['score_biological'] >= 0.5:
        reasons.append("gene annotation present")
    
    if not reasons:
        reasons.append("moderate scores across criteria")
    
    return "; ".join(reasons)
