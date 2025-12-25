"""
FAQ Template - Structured template for FAQ page generation.

This template defines the structure for FAQ pages with dependencies on logic blocks.
"""

from typing import Dict, Any, List


class FAQTemplate:
    """
    Template for generating FAQ pages with structured Q&A pairs.
    
    Template Structure:
    - page_type: "faq"
    - product_name: Name of the product
    - questions: List of Q&A pairs with categories
    - metadata: Page metadata (generated_date, version, etc.)
    """
    
    @staticmethod
    def get_structure() -> Dict[str, Any]:
        """
        Get the template structure definition.
        
        Returns:
            Dictionary defining the FAQ page structure
        """
        return {
            "page_type": "faq",
            "product_name": "",
            "total_questions": 0,
            "categories": [],
            "questions": [],
            "metadata": {
                "generated_date": "",
                "version": "1.0",
                "template": "faq_template"
            }
        }
    
    @staticmethod
    def get_required_fields() -> List[str]:
        """Get list of required fields that must be populated."""
        return ["product_name", "questions"]
    
    @staticmethod
    def get_logic_block_dependencies() -> Dict[str, str]:
        """
        Define which logic blocks are used for which sections.
        
        Returns:
            Dictionary mapping section names to logic block names
        """
        return {
            "benefits_questions": "benefits_block",
            "usage_questions": "usage_block",
            "safety_questions": "safety_block"
        }
    
    @staticmethod
    def validate_question_structure(question: Dict[str, Any]) -> bool:
        """
        Validate that a question has the required structure.
        
        Args:
            question: Question dictionary to validate
            
        Returns:
            True if valid, False otherwise
        """
        required_keys = ["question", "answer", "category"]
        return all(key in question for key in required_keys)
    
    @staticmethod
    def categorize_questions(questions: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Group questions by category.
        
        Args:
            questions: List of question dictionaries
            
        Returns:
            Dictionary with categories as keys and lists of questions as values
        """
        categorized = {}
        for q in questions:
            category = q.get("category", "General")
            if category not in categorized:
                categorized[category] = []
            categorized[category].append(q)
        return categorized
    
    @staticmethod
    def fill_template(product_data: Dict[str, Any], questions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Fill the FAQ template with product data and questions.
        
        Args:
            product_data: Product information
            questions: List of Q&A pairs with categories
            
        Returns:
            Populated FAQ template
        """
        from datetime import datetime
        
        template = FAQTemplate.get_structure()
        
        # Fill basic info
        template["product_name"] = product_data.get("name", "Unknown Product")
        template["questions"] = questions
        template["total_questions"] = len(questions)
        
        # Extract unique categories
        categories = list(set(q.get("category", "General") for q in questions))
        template["categories"] = sorted(categories)
        
        # Update metadata
        template["metadata"]["generated_date"] = datetime.now().isoformat()
        
        return template
