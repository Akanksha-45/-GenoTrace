"""
Sequence I/O utilities for GenoTrace using Biopython.
Handles reading/writing FASTA/FASTQ files and basic validation.
"""
import os
from pathlib import Path
from typing import Dict, Any, List, Optional
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord


class SequenceIOError(Exception):
    """Custom exception for sequence I/O errors."""
    pass


def read_fasta(filepath: str) -> List[SeqRecord]:
    """
    Read sequences from a FASTA file.
    
    Args:
        filepath: Path to FASTA file
        
    Returns:
        List of SeqRecord objects
        
    Raises:
        SequenceIOError: If file doesn't exist or is invalid
    """
    if not os.path.exists(filepath):
        raise SequenceIOError(f"File not found: {filepath}")
    
    try:
        records = list(SeqIO.parse(filepath, "fasta"))
        if not records:
            raise SequenceIOError(f"No sequences found in {filepath}")
        return records
    except Exception as e:
        raise SequenceIOError(f"Error reading FASTA {filepath}: {e}")


def read_fastq(filepath: str) -> List[SeqRecord]:
    """
    Read sequences from a FASTQ file.
    
    Args:
        filepath: Path to FASTQ file
        
    Returns:
        List of SeqRecord objects
        
    Raises:
        SequenceIOError: If file doesn't exist or is invalid
    """
    if not os.path.exists(filepath):
        raise SequenceIOError(f"File not found: {filepath}")
    
    try:
        records = list(SeqIO.parse(filepath, "fastq"))
        if not records:
            raise SequenceIOError(f"No sequences found in {filepath}")
        return records
    except Exception as e:
        raise SequenceIOError(f"Error reading FASTQ {filepath}: {e}")


def get_sequence_stats(records: List[SeqRecord]) -> Dict[str, Any]:
    """
    Calculate basic statistics for sequence records.
    
    Args:
        records: List of SeqRecord objects
        
    Returns:
        Dictionary with statistics
    """
    if not records:
        return {}
    
    lengths = [len(rec.seq) for rec in records]
    total_bases = sum(lengths)
    
    return {
        "num_sequences": len(records),
        "total_bases": total_bases,
        "min_length": min(lengths),
        "max_length": max(lengths),
        "mean_length": total_bases / len(lengths),
        "sequence_ids": [rec.id for rec in records]
    }


def validate_reference_fasta(filepath: str) -> Dict[str, Any]:
    """
    Validate a reference FASTA file for alignment.
    
    Args:
        filepath: Path to reference FASTA
        
    Returns:
        Validation report dictionary
    """
    report = {
        "valid": False,
        "filepath": filepath,
        "errors": [],
        "warnings": [],
        "stats": {}
    }
    
    try:
        records = read_fasta(filepath)
        stats = get_sequence_stats(records)
        report["stats"] = stats
        report["valid"] = True
        
        # Basic validation checks
        if stats["num_sequences"] == 0:
            report["errors"].append("No sequences found")
            report["valid"] = False
        
        # Check for unusual characters
        for rec in records:
            seq_str = str(rec.seq).upper()
            valid_bases = set("ATGCN")
            invalid = set(seq_str) - valid_bases
            if invalid:
                report["warnings"].append(f"Non-standard bases in {rec.id}: {invalid}")
        
    except SequenceIOError as e:
        report["errors"].append(str(e))
    
    return report


def write_fasta(records: List[SeqRecord], filepath: str) -> None:
    """
    Write sequences to a FASTA file.
    
    Args:
        records: List of SeqRecord objects
        filepath: Output path
    """
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    try:
        SeqIO.write(records, filepath, "fasta")
    except Exception as e:
        raise SequenceIOError(f"Error writing FASTA {filepath}: {e}")
