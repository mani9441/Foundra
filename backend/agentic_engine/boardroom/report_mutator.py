from typing import Dict, Any, List
import re

def mutate_report(original_report: Dict[str, Any], board_critiques: List[str]) -> Dict[str, Any]:
    new_report = dict(original_report)
    critiques_text = " ".join(board_critiques).lower()

    if "cut phases 4" in critiques_text or "cut phases 5" in critiques_text or "cut phase 4" in critiques_text:
        if "phases" in new_report:
            if isinstance(new_report["phases"], list):
                new_report["phases"] = [p for p in new_report["phases"] if not re.search(r"phase\s*[45]", str(p).lower())]
        if "product_strategy" in new_report and isinstance(new_report["product_strategy"], dict):
            new_report["product_strategy"]["mvp_scope"] = "Phases 1-3 only (Validation, Market Research, Business Model)"

    if "cut price" in critiques_text or "pricing too high" in critiques_text:
        if "pricing" in new_report and isinstance(new_report["pricing"], dict):
            old_price = new_report["pricing"].get("monthly", 49)
            new_price = int(old_price * 0.7) if isinstance(old_price, (int, float)) else 29
            new_report["pricing"]["monthly"] = new_price
            new_report["pricing"]["notes"] = "Reduced after board feedback"

    if "freemium" in critiques_text:
        new_report["pricing"] = new_report.get("pricing", {})
        new_report["pricing"]["freemium"] = True
        new_report["pricing"]["notes"] = "Freemium tier added per board request"

    if "execution risk" in critiques_text and "owner" in critiques_text:
        if "risks" in new_report and isinstance(new_report["risks"], list):
            new_report["risks"].append("Board-identified: execution risk of broad scope – assign owner")

    new_report["_board_mutations_applied"] = board_critiques[:3]
    return new_report