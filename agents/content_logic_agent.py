from typing import Dict, Any
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic_blocks.benefits_block import format_benefits, get_benefit_details
from logic_blocks.usage_block import format_usage_instructions, get_usage_tips
from logic_blocks.safety_block import format_safety_info, get_contraindications
from logic_blocks.comparison_block import compare_products, generate_fictional_competitor


class ContentLogicAgent:
    
    def __init__(self):
        self.agent_name = "ContentLogicAgent"
        
        self.logic_blocks = {
            "benefits": format_benefits,
            "usage": format_usage_instructions,
            "safety": format_safety_info,
            "comparison": compare_products,
            "fictional_competitor": generate_fictional_competitor
        }
    
    def process(self, block_name: str, product_data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        if block_name not in self.logic_blocks:
            raise ValueError(f"Unknown logic block: {block_name}")
        
        logic_function = self.logic_blocks[block_name]
        
        if block_name == "comparison":
            product_b = kwargs.get('product_b')
            if not product_b:
                raise ValueError("Comparison block requires 'product_b' argument")
            result = logic_function(product_data, product_b)
        else:
            result = logic_function(product_data)
        
        return result
    
    def process_all_blocks(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        results = {
            "benefits": self.process("benefits", product_data),
            "usage": self.process("usage", product_data),
            "safety": self.process("safety", product_data)
        }
        
        results["usage"]["tips"] = get_usage_tips(product_data)
        results["safety"]["contraindications"] = get_contraindications(product_data)
        
        return results
    
    def generate_comparison_data(self, product_a: Dict[str, Any]) -> Dict[str, Any]:
        product_b = self.process("fictional_competitor", product_a)
        comparison = self.process("comparison", product_a, product_b=product_b)
        
        return {
            "product_a": product_a,
            "product_b": product_b,
            "comparison": comparison
        }
