from typing import Dict, Any, List


class ComparisonTemplate:
    """Template for generating product comparison pages."""
    
    @staticmethod
    def get_structure() -> Dict[str, Any]:
        """
        Get the template structure definition.
        
        Returns:
            Dictionary defining the comparison page structure
        """
        return {
            "page_type": "comparison",
            "product_a": {
                "name": "",
                "concentration": "",
                "skin_type": "",
                "key_ingredients": "",
                "benefits": "",
                "price": ""
            },
            "product_b": {
                "name": "",
                "concentration": "",
                "skin_type": "",
                "key_ingredients": "",
                "benefits": "",
                "price": ""
            },
            "comparison": {
                "feature_comparison": [],
                "winner_features": {
                    "product_a": [],
                    "product_b": []
                },
                "similarities": [],
                "differences": []
            },
            "recommendation": "",
            "metadata": {
                "generated_date": "",
                "version": "1.0",
                "template": "comparison_template"
            }
        }
    
    @staticmethod
    def get_required_fields() -> List[str]:
        """Get list of required fields that must be populated."""
        return ["product_a", "product_b", "comparison", "recommendation"]
    
    @staticmethod
    def get_logic_block_dependencies() -> Dict[str, str]:
        """
        Define which logic blocks are used for which sections.
        
        Returns:
            Dictionary mapping section names to logic block names
        """
        return {
            "comparison": "comparison_block"
        }
    
    @staticmethod
    def fill_template(product_a_data: Dict[str, Any],
                     product_b_data: Dict[str, Any],
                     comparison_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fill the comparison template with product data and comparison results.
        
        Args:
            product_a_data: First product information
            product_b_data: Second product information
            comparison_data: Comparison results from comparison_block
            
        Returns:
            Populated comparison template
        """
        from datetime import datetime
        
        template = ComparisonTemplate.get_structure()
        
        # Fill product A info
        template["product_a"]["name"] = product_a_data.get("name", "")
        template["product_a"]["concentration"] = product_a_data.get("concentration", "")
        template["product_a"]["skin_type"] = product_a_data.get("skin_type", "")
        template["product_a"]["key_ingredients"] = product_a_data.get("key_ingredients", "")
        template["product_a"]["benefits"] = product_a_data.get("benefits", "")
        template["product_a"]["price"] = product_a_data.get("price", "")
        
        # Fill product B info
        template["product_b"]["name"] = product_b_data.get("name", "")
        template["product_b"]["concentration"] = product_b_data.get("concentration", "")
        template["product_b"]["skin_type"] = product_b_data.get("skin_type", "")
        template["product_b"]["key_ingredients"] = product_b_data.get("key_ingredients", "")
        template["product_b"]["benefits"] = product_b_data.get("benefits", "")
        template["product_b"]["price"] = product_b_data.get("price", "")
        
        # Fill comparison data (from comparison_block)
        template["comparison"]["feature_comparison"] = comparison_data.get("feature_comparison", [])
        template["comparison"]["winner_features"] = comparison_data.get("winner_features", {"product_a": [], "product_b": []})
        template["comparison"]["similarities"] = comparison_data.get("similarities", [])
        template["comparison"]["differences"] = comparison_data.get("differences", [])
        
        # Fill recommendation
        template["recommendation"] = comparison_data.get("recommendation", "")
        
        # Update metadata
        template["metadata"]["generated_date"] = datetime.now().isoformat()
        
        return template
