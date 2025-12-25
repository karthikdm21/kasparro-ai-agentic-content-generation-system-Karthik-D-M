from typing import List, Dict, Any


def format_usage_instructions(product_data: Dict[str, Any]) -> Dict[str, Any]:
    usage_raw = product_data.get('how_to_use', '')
    
    timing = "morning" if "morning" in usage_raw.lower() else "evening"
    if "morning" in usage_raw.lower():
        timing = "morning"
    elif "evening" in usage_raw.lower() or "night" in usage_raw.lower():
        timing = "evening"
    else:
        timing = "morning or evening"
    
    application_amount = "2-3 drops"
    if "drop" in usage_raw.lower():
        words = usage_raw.split()
        for i, word in enumerate(words):
            if "drop" in word.lower() and i > 0:
                application_amount = f"{words[i-1]} {word}"
                break
    
    steps = [
        "Cleanse your face thoroughly and pat dry",
        f"Apply {application_amount} to your fingertips",
        "Gently massage the serum onto your face and neck",
        "Wait for the serum to fully absorb (1-2 minutes)"
    ]
    
    if "sunscreen" in usage_raw.lower():
        steps.append("Follow with sunscreen (essential when using Vitamin C)")
    elif timing == "evening":
        steps.append("Follow with your regular moisturizer")
    else:
        steps.append("Continue with your regular skincare routine")
    
    full_instructions = f"For best results, use this product in the {timing}. " + " ".join([f"Step {i+1}: {step}." for i, step in enumerate(steps)])
    
    return {
        "steps": steps,
        "timing": timing,
        "application_amount": application_amount,
        "full_instructions": full_instructions,
        "step_count": len(steps)
    }


def get_usage_tips(product_data: Dict[str, Any]) -> List[str]:
    tips = []
    
    concentration = product_data.get('concentration', '')
    skin_type = product_data.get('skin_type', '')
    
    if 'vitamin c' in concentration.lower():
        tips.append("Store in a cool, dark place to maintain Vitamin C potency")
        tips.append("Use within 3-6 months of opening for maximum effectiveness")
    
    if 'oily' in skin_type.lower():
        tips.append("This lightweight formula is ideal for oily skin and won't clog pores")
    if 'combination' in skin_type.lower():
        tips.append("Focus application on areas that need brightening, avoiding overly dry patches")
    
    tips.append("Perform a patch test before first use")
    tips.append("Start with once daily application and increase as tolerated")
    
    return tips
