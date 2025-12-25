from typing import Dict, Any
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from templates.faq_template import FAQTemplate
from templates.product_template import ProductTemplate
from templates.comparison_template import ComparisonTemplate


class TemplateAgent:
    
    def __init__(self):
        self.agent_name = "TemplateAgent"
        
        self.templates = {
            "faq": FAQTemplate,
            "product": ProductTemplate,
            "comparison": ComparisonTemplate
        }
    
    def fill_template(self, template_name: str, **kwargs) -> Dict[str, Any]:
        if template_name not in self.templates:
            raise ValueError(f"Unknown template: {template_name}")
        
        template_class = self.templates[template_name]
        
        if template_name == "faq":
            return self._fill_faq_template(template_class, **kwargs)
        elif template_name == "product":
            return self._fill_product_template(template_class, **kwargs)
        elif template_name == "comparison":
            return self._fill_comparison_template(template_class, **kwargs)
        else:
            raise ValueError(f"No fill method for template: {template_name}")
    
    def _fill_faq_template(self, template_class, **kwargs) -> Dict[str, Any]:
        product_data = kwargs.get('product_data')
        questions = kwargs.get('questions')
        
        if not product_data or not questions:
            raise ValueError("FAQ template requires 'product_data' and 'questions'")
        
        return template_class.fill_template(product_data, questions)
    
    def _fill_product_template(self, template_class, **kwargs) -> Dict[str, Any]:
        product_data = kwargs.get('product_data')
        benefits_data = kwargs.get('benefits_data')
        usage_data = kwargs.get('usage_data')
        safety_data = kwargs.get('safety_data')
        
        if not all([product_data, benefits_data, usage_data, safety_data]):
            raise ValueError("Product template requires product_data, benefits_data, usage_data, and safety_data")
        
        return template_class.fill_template(
            product_data,
            benefits_data,
            usage_data,
            safety_data
        )
    
    def _fill_comparison_template(self, template_class, **kwargs) -> Dict[str, Any]:
        product_a_data = kwargs.get('product_a_data')
        product_b_data = kwargs.get('product_b_data')
        comparison_data = kwargs.get('comparison_data')
        
        if not all([product_a_data, product_b_data, comparison_data]):
            raise ValueError("Comparison template requires product_a_data, product_b_data, and comparison_data")
        
        return template_class.fill_template(
            product_a_data,
            product_b_data,
            comparison_data
        )
    
    def get_template_structure(self, template_name: str) -> Dict[str, Any]:
        if template_name not in self.templates:
            raise ValueError(f"Unknown template: {template_name}")
        
        return self.templates[template_name].get_structure()
