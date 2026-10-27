"""
Read alignment utilities for GenoTrace.
Provides documentation and helper functions for BWA/SAMtools workflows.
"""
import os
from pathlib import Path
from typing import Dict, Any, Optional


class AlignmentError(Exception):
    """Custom exception for alignment errors."""
    pass


def generate_bwa_index_command(reference_fasta: str, threads: int = 4) -> str:
    """
    Generate BWA index command.
    
    Args:
        reference_fasta: Path to reference FASTA
        threads: Number of threads
        
    Returns:
        Command string
    """
    return f"bwa index {reference_fasta}"


def generate_bwa_mem_command(
    reference_fasta: str,
    read1: str,
    read2: Optional[str] = None,
    output_sam: str = "aligned.sam",
    threads: int = 4,
    read_group: Optional[str] = None
) -> str:
    """
    Generate BWA MEM alignment command.
    
    Args:
        reference_fasta: Path to reference FASTA
        read1: Path to R1 FASTQ
        read2: Path to R2 FASTQ (for paired-end)
        output_sam: Output SAM file
        threads: Number of threads
        read_group: Read group string
        
    Returns:
        Command string
    """
    cmd = f"bwa mem -t {threads}"
    if read_group:
        cmd += f" -R '{read_group}'"
    cmd += f" {reference_fasta} {read1}"
    if read2:
        cmd += f" {read2}"
    cmd += f" > {output_sam}"
    return cmd


def generate_samtools_sort_command(input_sam: str, output_bam: str, threads: int = 4) -> str:
    """
    Generate SAMtools sort command.
    
    Args:
        input_sam: Input SAM/BAM
        output_bam: Output sorted BAM
        threads: Number of threads
        
    Returns:
        Command string
    """
    return f"samtools sort -@ {threads} -o {output_bam} {input_sam}"


def generate_samtools_index_command(input_bam: str) -> str:
    """
    Generate SAMtools index command.
    
    Args:
        input_bam: Input BAM file
        
    Returns:
        Command string
    """
    return f"samtools index {input_bam}"


def generate_alignment_stats_command(input_bam: str) -> str:
    """
    Generate SAMtools flagstat command for alignment statistics.
    
    Args:
        input_bam: Input BAM file
        
    Returns:
        Command string
    """
    return f"samtools flagstat {input_bam} > {Path(input_bam).stem}_flagstat.txt"


def get_alignment_workflow(reference: str, r1: str, r2: Optional[str] = None, 
                          output_prefix: str = "aligned") -> Dict[str, str]:
    """
    Generate complete alignment workflow commands.
    
    Args:
        reference: Reference FASTA path
        r1: Read 1 FASTQ path
        r2: Read 2 FASTQ path (optional)
        output_prefix: Prefix for outputs
        
    Returns:
        Dictionary of step names and commands
    """
    workflow = {
        "1_index": generate_bwa_index_command(reference),
        "2_align": generate_bwa_mem_command(reference, r1, r2, f"{output_prefix}.sam"),
        "3_sort": generate_samtools_sort_command(f"{output_prefix}.sam", f"{output_prefix}.sorted.bam"),
        "4_index_bam": generate_samtools_index_command(f"{output_prefix}.sorted.bam"),
        "5_stats": generate_alignment_stats_command(f"{output_prefix}.sorted.bam")
    }
    return workflow
