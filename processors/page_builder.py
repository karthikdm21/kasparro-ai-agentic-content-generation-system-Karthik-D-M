import json
from typing import Dict, Any, Optional
import os


class PageBuilder:
    
    def __init__(self, output_dir: str = "outputs"):
        self.processor_name = "PageBuilder"
        self.output_dir = output_dir
        
        os.makedirs(output_dir, exist_ok=True)
    
    def build_page(self, page_data: Dict[str, Any], filename: str, 
                   execution_context: Optional[Any] = None) -> str:
        if not isinstance(page_data, dict):
            raise ValueError("page_data must be a dictionary")
        
        if not filename.endswith('.json'):
            filename += '.json'
        
        if execution_context is not None:
            page_type = self._extract_page_type(filename)
            page_data_with_meta = page_data.copy()
            page_data_with_meta['_meta'] = execution_context.generate_meta(page_type)
        else:
            page_data_with_meta = page_data
        
        output_path = os.path.join(self.output_dir, filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(page_data_with_meta, f, indent=2, ensure_ascii=False)
        
        return output_path
    
    def build_all_pages(self, pages: Dict[str, Dict[str, Any]], 
                       execution_context: Optional[Any] = None) -> Dict[str, str]:
        output_paths = {}
        
        for filename, page_data in pages.items():
            output_path = self.build_page(page_data, filename, execution_context)
            output_paths[filename] = output_path
        
        return output_paths
    
    def _extract_page_type(self, filename: str) -> str:
        if 'faq' in filename.lower():
            return 'faq'
        elif 'product' in filename.lower():
            return 'product'
        elif 'comparison' in filename.lower():
            return 'comparison'
        return 'unknown'
    
    def validate_json(self, filepath: str) -> bool:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                json.load(f)
            return True
        except (json.JSONDecodeError, FileNotFoundError):
            return False
