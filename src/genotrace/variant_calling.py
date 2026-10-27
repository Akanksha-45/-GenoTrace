"""
Variant calling utilities for GenoTrace.
Provides command generation for FreeBayes and other callers.
"""
from typing import Dict, Any, Optional


class VariantCallingError(Exception):
    """Custom exception for variant calling errors."""
    pass


def generate_freebayes_command(
    reference_fasta: str,
    input_bam: str,
    output_vcf: str = "variants.vcf",
    ploidy: int = 2,
    min_qual: int = 20,
    min_depth: int = 10,
    use_population_model: bool = True
) -> str:
    """
    Generate FreeBayes variant calling command.
    
    Args:
        reference_fasta: Reference FASTA path
        input_bam: Input sorted BAM
        output_vcf: Output VCF file
        ploidy: Ploidy level
        min_qual: Minimum base quality
        min_depth: Minimum coverage
        use_population_model: Use population model
        
    Returns:
        Command string
    """
    cmd = f"freebayes -f {reference_fasta} -p {ploidy}"
    if use_population_model:
        cmd += " --use-mapping-quality"
    cmd += f" -q {min_qual} --min-coverage {min_depth}"
    cmd += f" {input_bam} > {output_vcf}"
    return cmd


def generate_bcftools_filter_command(
    input_vcf: str,
    output_vcf: str,
    min_qual: int = 30,
    min_depth: int = 10
) -> str:
    """
    Generate bcftools filter command.
    
    Args:
        input_vcf: Input VCF
        output_vcf: Output filtered VCF
        min_qual: Minimum QUAL
        min_depth: Minimum DP
        
    Returns:
        Command string
    """
    return (f"bcftools filter -i 'QUAL>{min_qual} && DP>{min_depth}' "
            f"{input_vcf} > {output_vcf}")


def generate_variant_calling_workflow(reference: str, bam: str, 
                                     output_prefix: str = "variants") -> Dict[str, str]:
    """
    Generate variant calling workflow commands.
    
    Args:
        reference: Reference FASTA
        bam: Sorted BAM file
        output_prefix: Prefix for outputs
        
    Returns:
        Dictionary of commands
    """
    workflow = {
        "1_call": generate_freebayes_command(reference, bam, f"{output_prefix}_raw.vcf"),
        "2_filter": generate_bcftools_filter_command(f"{output_prefix}_raw.vcf", 
                                                     f"{output_prefix}_filtered.vcf"),
        "3_stats": f"bcftools stats {output_prefix}_filtered.vcf > {output_prefix}_stats.txt"
    }
    return workflow


def get_variant_calling_recommendations() -> Dict[str, Any]:
    """
    Get recommendations for variant calling.
    
    Returns:
        Dictionary with recommendations
    """
    return {
        "caller": "FreeBayes (good for germline, haploid/diploid)",
        "alternatives": ["GATK HaplotypeCaller", "bcftools mpileup/call"],
        "tips": [
            "Use matching reference genome build",
            "Ensure proper read groups in BAM",
            "Consider ploidy for organism",
            "Filter based on quality metrics",
            "Validate with known sites if available"
        ],
        "notes": "For learning, FreeBayes is accessible via conda/bioconda"
    }
