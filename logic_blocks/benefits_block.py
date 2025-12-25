from typing import List, Dict, Any


def format_benefits(product_data: Dict[str, Any]) -> Dict[str, Any]:
    benefits_raw = product_data.get('benefits', '')
    
    benefits_list = [b.strip() for b in benefits_raw.split(',') if b.strip()]
    
    primary_benefit = benefits_list[0] if benefits_list else "General skincare improvement"
    
    if len(benefits_list) > 1:
        benefits_summary = f"This product offers {', '.join(benefits_list[:-1])}, and {benefits_list[-1]}."
    elif len(benefits_list) == 1:
        benefits_summary = f"This product offers {benefits_list[0]}."
    else:
        benefits_summary = "This product offers skincare benefits."
    
    return {
        "benefits_list": benefits_list,
        "benefits_summary": benefits_summary,
        "primary_benefit": primary_benefit,
        "benefits_count": len(benefits_list)
    }


def get_benefit_details(benefit_name: str, product_data: Dict[str, Any]) -> str:
    ingredients = product_data.get('key_ingredients', '')
    
    benefit_explanations = {
        "brightening": f"The brightening effect comes from the active ingredients ({ingredients}), which work together to even out skin tone and enhance radiance.",
        "fades dark spots": f"Dark spot reduction is achieved through the combination of {ingredients}, which help reduce hyperpigmentation over time with consistent use.",
        "hydration": f"Hydration is provided by {ingredients}, which help retain moisture in the skin.",
        "anti-aging": f"Anti-aging benefits are delivered through {ingredients}, which support skin renewal and firmness."
    }
    
    benefit_lower = benefit_name.lower()
    for key, explanation in benefit_explanations.items():
        if key in benefit_lower:
            return explanation
    
    return f"This benefit is supported by the product's formulation with {ingredients}."
