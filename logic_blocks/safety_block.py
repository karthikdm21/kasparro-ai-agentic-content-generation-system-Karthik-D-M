from typing import List, Dict, Any


def format_safety_info(product_data: Dict[str, Any]) -> Dict[str, Any]:
    side_effects_raw = product_data.get('side_effects', '')
    skin_type = product_data.get('skin_type', '')
    
    side_effects = []
    severity = "mild"
    
    if side_effects_raw:
        if ',' in side_effects_raw:
            side_effects = [se.strip() for se in side_effects_raw.split(',')]
        else:
            side_effects = [side_effects_raw.strip()]
        
        if any(word in side_effects_raw.lower() for word in ['severe', 'burning', 'rash']):
            severity = "moderate"
        elif any(word in side_effects_raw.lower() for word in ['mild', 'slight', 'tingling']):
            severity = "mild"
    
    precautions = [
        "Perform a patch test on your inner arm before first use",
        "Discontinue use if irritation occurs",
        "Avoid contact with eyes; rinse thoroughly if contact occurs"
    ]
    
    if 'sensitive' in side_effects_raw.lower():
        precautions.append("Those with sensitive skin should start with alternate-day application")
    
    warnings = []
    if 'vitamin c' in product_data.get('concentration', '').lower():
        warnings.append("May increase sun sensitivity - always use sunscreen during the day")
    
    warnings.append("For external use only")
    warnings.append("Keep out of reach of children")
    
    safe_for_list = []
    if skin_type:
        skin_types = [st.strip() for st in skin_type.split(',')]
        safe_for_list.extend(skin_types)
    
    safe_for = f"Suitable for {', '.join(safe_for_list)} skin types" if safe_for_list else "Suitable for most skin types"
    
    return {
        "side_effects": side_effects,
        "severity": severity,
        "precautions": precautions,
        "warnings": warnings,
        "safe_for": safe_for,
        "is_safe": severity in ["mild", "none"]
    }


def get_contraindications(product_data: Dict[str, Any]) -> List[str]:
    contraindications = []
    
    ingredients = product_data.get('key_ingredients', '').lower()
    
    if 'vitamin c' in ingredients:
        contraindications.append("Do not use with retinol or benzoyl peroxide in the same routine")
        contraindications.append("Avoid if you have active skin wounds or sunburn")
    
    if 'hyaluronic acid' in ingredients:
        contraindications.append("Apply to damp skin for best absorption")
    
    contraindications.append("Not recommended during active skin infections")
    contraindications.append("Consult a dermatologist if pregnant or nursing")
    
    return contraindications
