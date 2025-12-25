from typing import Dict, Any, List


def compare_products(product_a: Dict[str, Any], product_b: Dict[str, Any]) -> Dict[str, Any]:
    comparison = {
        "product_a_name": product_a.get('name', 'Product A'),
        "product_b_name": product_b.get('name', 'Product B'),
        "feature_comparison": [],
        "winner_features": {"product_a": [], "product_b": []},
        "similarities": [],
        "differences": []
    }
    
    conc_a = product_a.get('concentration', '')
    conc_b = product_b.get('concentration', '')
    comparison["feature_comparison"].append({
        "feature": "Concentration",
        "product_a": conc_a,
        "product_b": conc_b,
        "winner": _determine_concentration_winner(conc_a, conc_b)
    })
    
    price_a = product_a.get('price', '')
    price_b = product_b.get('price', '')
    comparison["feature_comparison"].append({
        "feature": "Price",
        "product_a": price_a,
        "product_b": price_b,
        "winner": _determine_price_winner(price_a, price_b)
    })
    
    skin_a = set(s.strip() for s in product_a.get('skin_type', '').split(','))
    skin_b = set(s.strip() for s in product_b.get('skin_type', '').split(','))
    
    common_skin_types = skin_a.intersection(skin_b)
    if common_skin_types:
        comparison["similarities"].append(f"Both suitable for {', '.join(common_skin_types)} skin")
    
    comparison["feature_comparison"].append({
        "feature": "Skin Type",
        "product_a": product_a.get('skin_type', ''),
        "product_b": product_b.get('skin_type', ''),
        "winner": "tie" if skin_a == skin_b else "product_b" if len(skin_b) > len(skin_a) else "product_a"
    })
    
    ing_a = product_a.get('key_ingredients', '')
    ing_b = product_b.get('key_ingredients', '')
    comparison["feature_comparison"].append({
        "feature": "Key Ingredients",
        "product_a": ing_a,
        "product_b": ing_b,
        "winner": "tie"
    })
    
    ben_a = product_a.get('benefits', '')
    ben_b = product_b.get('benefits', '')
    comparison["feature_comparison"].append({
        "feature": "Benefits",
        "product_a": ben_a,
        "product_b": ben_b,
        "winner": "tie"
    })
    
    for feature in comparison["feature_comparison"]:
        if feature["winner"] == "product_a":
            comparison["winner_features"]["product_a"].append(feature["feature"])
        elif feature["winner"] == "product_b":
            comparison["winner_features"]["product_b"].append(feature["feature"])
    
    comparison["recommendation"] = _generate_recommendation(comparison, product_a, product_b)
    
    return comparison


def _determine_concentration_winner(conc_a: str, conc_b: str) -> str:
    try:
        pct_a = float(''.join(filter(str.isdigit, conc_a.split('%')[0])))
        pct_b = float(''.join(filter(str.isdigit, conc_b.split('%')[0])))
        
        if pct_a > pct_b:
            return "product_a"
        elif pct_b > pct_a:
            return "product_b"
        else:
            return "tie"
    except:
        return "tie"


def _determine_price_winner(price_a: str, price_b: str) -> str:
    try:
        num_a = float(''.join(filter(str.isdigit, price_a)))
        num_b = float(''.join(filter(str.isdigit, price_b)))
        
        if num_a < num_b:
            return "product_a"
        elif num_b < num_a:
            return "product_b"
        else:
            return "tie"
    except:
        return "tie"


def _generate_recommendation(comparison: Dict, product_a: Dict, product_b: Dict) -> str:
    a_wins = len(comparison["winner_features"]["product_a"])
    b_wins = len(comparison["winner_features"]["product_b"])
    
    if a_wins > b_wins:
        return f"Choose {product_a.get('name', 'Product A')} for better overall value and effectiveness"
    elif b_wins > a_wins:
        return f"Choose {product_b.get('name', 'Product B')} for better overall value and effectiveness"
    else:
        return f"Both products are comparable; choose based on your specific skin concerns and budget"


def generate_fictional_competitor(base_product: Dict[str, Any]) -> Dict[str, Any]:
    fictional_product = {
        "name": "RadiantGlow Vitamin C Serum",
        "concentration": "15% Vitamin C",
        "skin_type": "All skin types",
        "key_ingredients": "Vitamin C, Vitamin E, Ferulic Acid",
        "benefits": "Anti-aging, Brightening, Antioxidant protection",
        "how_to_use": "Apply 3-4 drops in the evening before moisturizer",
        "side_effects": "May cause slight redness initially",
        "price": "₹899"
    }
    
    return fictional_product
