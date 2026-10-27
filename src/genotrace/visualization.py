"""
Visualization utilities for GenoTrace.
Create plots for QC, variants, and prioritization results.
"""
import os
from pathlib import Path
from typing import Optional, List
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns


class VisualizationError(Exception):
    """Custom exception for visualization errors."""
    pass


def plot_variant_types(df: pd.DataFrame, output_file: str, figsize: tuple = (8, 6)) -> None:
    """
    Plot distribution of variant types.
    
    Args:
        df: VCF DataFrame
        output_file: Output image path
        figsize: Figure size
    """
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    
    if df.empty or 'REF' not in df.columns or 'ALT' not in df.columns:
        raise VisualizationError("Invalid data for variant type plot")
    
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
    
    types = df.apply(classify_type, axis=1)
    type_counts = types.value_counts()
    
    plt.figure(figsize=figsize)
    type_counts.plot(kind='bar', color=sns.color_palette("Set2"))
    plt.title('Variant Type Distribution', fontsize=14, fontweight='bold')
    plt.xlabel('Variant Type')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()


def plot_qual_distribution(df: pd.DataFrame, output_file: str, figsize: tuple = (10, 6)) -> None:
    """
    Plot QUAL score distribution.
    
    Args:
        df: VCF DataFrame
        output_file: Output image path
        figsize: Figure size
    """
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    
    if df.empty or 'QUAL' not in df.columns:
        raise VisualizationError("No QUAL data available")
    
    qual = pd.to_numeric(df['QUAL'], errors='coerce').dropna()
    
    plt.figure(figsize=figsize)
    plt.hist(qual, bins=50, color='skyblue', edgecolor='black', alpha=0.7)
    plt.axvline(qual.mean(), color='red', linestyle='--', label=f'Mean: {qual.mean():.2f}')
    plt.title('Variant Quality Distribution', fontsize=14, fontweight='bold')
    plt.xlabel('QUAL Score')
    plt.ylabel('Frequency')
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()


def plot_chromosome_distribution(df: pd.DataFrame, output_file: str, figsize: tuple = (12, 6)) -> None:
    """
    Plot variants per chromosome.
    
    Args:
        df: VCF DataFrame
        output_file: Output image path
        figsize: Figure size
    """
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    
    if df.empty or '#CHROM' not in df.columns:
        raise VisualizationError("No chromosome data available")
    
    chrom_counts = df['#CHROM'].value_counts().sort_index()
    
    plt.figure(figsize=figsize)
    chrom_counts.plot(kind='bar', color='coral')
    plt.title('Variants per Chromosome', fontsize=14, fontweight='bold')
    plt.xlabel('Chromosome')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()


def plot_prioritization_scores(df: pd.DataFrame, output_file: str, top_n: int = 20, figsize: tuple = (10, 8)) -> None:
    """
    Plot top prioritized variants.
    
    Args:
        df: Prioritized DataFrame
        output_file: Output image path
        top_n: Number of top variants to plot
        figsize: Figure size
    """
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    
    if df.empty or 'prioritization_score' not in df.columns:
        raise VisualizationError("No prioritization scores available")
    
    top_df = df.head(top_n).copy()
    top_df['label'] = top_df.apply(
        lambda r: f"{r.get('#CHROM','')}:{r.get('POS','')} {r.get('REF','')}>{r.get('ALT','')}",
        axis=1
    )
    
    plt.figure(figsize=figsize)
    plt.barh(range(len(top_df)), top_df['prioritization_score'], color='teal')
    plt.yticks(range(len(top_df)), top_df['label'])
    plt.xlabel('Prioritization Score')
    plt.title(f'Top {top_n} Prioritized Variants', fontsize=14, fontweight='bold')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
