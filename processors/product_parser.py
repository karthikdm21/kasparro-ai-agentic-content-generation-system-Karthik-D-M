from typing import Dict, Any


class ProductParser:
    
    def __init__(self):
        self.processor_name = "ProductParser"
    
    def parse(self, raw_product_data: Dict[str, Any]) -> Dict[str, Any]:
        

        expected_fields = [
            'name', 'concentration', 'skin_type', 'key_ingredients',
            'benefits', 'how_to_use', 'side_effects', 'price'
        ]
        
        structured_data = {}
        
        for field in expected_fields:
            value = raw_product_data.get(field, '')
            
            if isinstance(value, str):
                value = value.strip()
            
            structured_data[field] = value
        
        required_fields = ['name', 'price']
        for field in required_fields:
            if not structured_data.get(field):
                raise ValueError(f"Missing required field: {field}")
        
        structured_data['_metadata'] = {
            'processor': self.processor_name,
            'status': 'parsed',
            'field_count': len([v for v in structured_data.values() if v])
        }
        
        return structured_data
    
    def validate_structure(self, data: Dict[str, Any]) -> bool:
        required_keys = ['name', 'price']
        return all(key in data for key in required_keys)
