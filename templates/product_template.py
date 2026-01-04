from typing import Dict, Any, List


class ProductTemplate:
    """Template for generating detailed product pages."""
    
    @staticmethod
    def get_structure() -> Dict[str, Any]:
        """
        Get the template structure definition.
        
        Returns:
            Dictionary defining the product page structure
        """
        return {
            "page_type": "product",
            "product_info": {
                "name": "",
                "concentration": "",
                "skin_type": "",
                "key_ingredients": "",
                "price": ""
            },
            "benefits_section": {
                "summary": "",
                "benefits_list": [],
                "primary_benefit": ""
            },
            "usage_section": {
                "timing": "",
                "steps": [],
                "tips": []
            },
            "safety_section": {
                "side_effects": [],
                "severity": "",
                "precautions": [],
                "warnings": []
            },
            "metadata": {
                "generated_date": "",
                "version": "1.0",
                "template": "product_template"
            }
        }
    
    @staticmethod
    def get_required_fields() -> List[str]:
        """Get list of required fields that must be populated."""
        return ["product_info", "benefits_section", "usage_section", "safety_section"]
    
    @staticmethod
    def get_logic_block_dependencies() -> Dict[str, str]:
        """
        Define which logic blocks are used for which sections.
        
        Returns:
            Dictionary mapping section names to logic block names
        """
        return {
            "benefits_section": "benefits_block",
            "usage_section": "usage_block",
            "safety_section": "safety_block"
        }
    
    @staticmethod
    def fill_template(product_data: Dict[str, Any], 
                     benefits_data: Dict[str, Any],
                     usage_data: Dict[str, Any],
                     safety_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fill the product template with data from logic blocks.
        
        Args:
            product_data: Raw product information
            benefits_data: Processed benefits from benefits_block
            usage_data: Processed usage info from usage_block
            safety_data: Processed safety info from safety_block
            
        Returns:
            Populated product template
        """
        from datetime import datetime
        
        template = ProductTemplate.get_structure()
        
        # Fill product info
        template["product_info"]["name"] = product_data.get("name", "")
        template["product_info"]["concentration"] = product_data.get("concentration", "")
        template["product_info"]["skin_type"] = product_data.get("skin_type", "")
        template["product_info"]["key_ingredients"] = product_data.get("key_ingredients", "")
        template["product_info"]["price"] = product_data.get("price", "")
        
        # Fill benefits section (from benefits_block)
        template["benefits_section"]["summary"] = benefits_data.get("benefits_summary", "")
        template["benefits_section"]["benefits_list"] = benefits_data.get("benefits_list", [])
        template["benefits_section"]["primary_benefit"] = benefits_data.get("primary_benefit", "")
        
        # Fill usage section (from usage_block)
        template["usage_section"]["timing"] = usage_data.get("timing", "")
        template["usage_section"]["steps"] = usage_data.get("steps", [])
        template["usage_section"]["tips"] = usage_data.get("tips", [])
        
        # Fill safety section (from safety_block)
        template["safety_section"]["side_effects"] = safety_data.get("side_effects", [])
        template["safety_section"]["severity"] = safety_data.get("severity", "")
        template["safety_section"]["precautions"] = safety_data.get("precautions", [])
        template["safety_section"]["warnings"] = safety_data.get("warnings", [])
        
        # Update metadata
        template["metadata"]["generated_date"] = datetime.now().isoformat()
        
        return template
