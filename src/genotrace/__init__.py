"""
GenoTrace: Clinical Decision Support (CDS) prototype for NGS variant analysis & prioritization.

Research/educational use only. Not a clinical diagnostic tool.
"""
__version__ = "0.2.0"
__author__ = "GenoTrace Project"
__license__ = "MIT"

# Optional convenience imports
try:
    from . import acmg_classifier  # noqa: F401
    from . import clinical_report  # noqa: F401
    from . import vcf_parser  # noqa: F401
    from . import prioritization  # noqa: F401
    from . import sequence_io  # noqa: F401
except Exception:
    pass

