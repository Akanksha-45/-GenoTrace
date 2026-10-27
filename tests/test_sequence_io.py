"""Tests for sequence_io module."""
import os
import tempfile
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from genotrace import sequence_io


def test_get_sequence_stats():
    records = [
        SeqRecord(Seq("ATGC"), id="seq1"),
        SeqRecord(Seq("ATGCAA"), id="seq2"),
    ]
    stats = sequence_io.get_sequence_stats(records)
    assert stats["num_sequences"] == 2
    assert stats["total_bases"] == 10
    assert stats["min_length"] == 4
    assert stats["max_length"] == 6
    assert stats["mean_length"] == 5.0


def test_write_and_read_fasta():
    records = [
        SeqRecord(Seq("ATGC"), id="test1", description="test sequence"),
        SeqRecord(Seq("GGCC"), id="test2", description="another"),
    ]
    with tempfile.NamedTemporaryFile(mode='w', suffix='.fasta', delete=False) as f:
        tmpfile = f.name
    
    try:
        sequence_io.write_fasta(records, tmpfile)
        read_records = sequence_io.read_fasta(tmpfile)
        assert len(read_records) == 2
        assert read_records[0].id == "test1"
        assert str(read_records[0].seq) == "ATGC"
    finally:
        if os.path.exists(tmpfile):
            os.unlink(tmpfile)
