"""
ACMG/AMP 2015 simplified classifier for Clinical Decision Support (CDS).
Educational use only. Not for standalone clinical diagnosis.
"""
from typing import Dict, Any, List
import pandas as pd


class ACMGClassifier:
    def __init__(self):
        self.classifications = [
            "Pathogenic",
            "Likely Pathogenic", 
            "Uncertain Significance",
            "Likely Benign",
            "Benign"
        ]
    
    def classify(self, variant: Dict[str, Any]) -> Dict[str, Any]:
        evidence_codes = []
        rationale_parts = []
        
        ref = str(variant.get('REF', ''))
        alt = str(variant.get('ALT', ''))
        qual = variant.get('QUAL', 0)
        
        try:
            qual_float = float(qual) if qual not in [None, '.'] else 0
        except:
            qual_float = 0
        
        # PVS1 - Loss of function
        if len(ref) > len(alt) and len(alt) == 1:
            evidence_codes.append("PVS1")
            rationale_parts.append("Potential frameshift/deletion effect")
        elif len(alt) > len(ref):
            evidence_codes.append("PVS1")
            rationale_parts.append("Potential insertion effect")
        
        # PM2 - Low frequency
        af = variant.get('AF')
        if af:
            try:
                af_float = float(af)
                if af_float < 0.001:
                    evidence_codes.append("PM2")
                    rationale_parts.append("Rare allele frequency")
                elif af_float >= 0.05:
                    evidence_codes.append("BA1")
                    rationale_parts.append("Common allele frequency")
            except:
                evidence_codes.append("PM2")
                rationale_parts.append("Unknown frequency - treated as rare for CDS")
        else:
            evidence_codes.append("PM2")
            rationale_parts.append("No population frequency data available")
        
        # PP3 - Supporting evidence
        if qual_float > 80 and "PVS1" in evidence_codes:
            evidence_codes.append("PP3")
            rationale_parts.append("High quality supporting evidence")
        
        # Classification
        pathogenic_codes = [c for c in evidence_codes if c in ['PVS1', 'PS1', 'PS2']]
        benign_codes = [c for c in evidence_codes if c in ['BA1', 'BS1']]
        
        if len(pathogenic_codes) >= 2 or ('PVS1' in evidence_codes and len(pathogenic_codes) >= 1):
            classification = "Likely Pathogenic"
        elif len(pathogenic_codes) >= 1:
            classification = "Uncertain Significance"
        elif len(benign_codes) >= 1:
            classification = "Likely Benign"
        else:
            classification = "Uncertain Significance"
        
        return {
            "classification": classification,
            "evidence_codes": evidence_codes,
            "rationale": "; ".join(rationale_parts) if rationale_parts else "Insufficient evidence for classification",
            "method": "Simplified ACMG/AMP 2015 (CDS prototype)"
        }
    
    def classify_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        results = []
        for _, row in df.iterrows():
            variant_dict = row.to_dict()
            # Extract AF from INFO if present
            if 'INFO' in variant_dict and pd.notna(variant_dict['INFO']):
                info = str(variant_dict['INFO'])
                for item in info.split(';'):
                    if item.startswith('AF='):
                        variant_dict['AF'] = item.split('=')[1]
            res = self.classify(variant_dict)
            results.append({
                'CHROM': variant_dict.get('#CHROM') or variant_dict.get('CHROM'),
                'POS': variant_dict.get('POS'),
                'REF': variant_dict.get('REF'),
                'ALT': variant_dict.get('ALT'),
                'QUAL': variant_dict.get('QUAL'),
                **res
            })
        return pd.DataFrame(results)
