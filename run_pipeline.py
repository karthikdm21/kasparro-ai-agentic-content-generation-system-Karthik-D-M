"""
Main entry point for the multi-agent content generation pipeline.

Run this script to execute the complete pipeline end-to-end.
"""

import os
import sys
from dotenv import load_dotenv

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from orchestrator.pipeline import ContentGenerationPipeline


def main():
    """Execute the content generation pipeline."""
    
    # Load environment variables
    load_dotenv()
    
    # Get API key from environment (OpenAI or Google)
    api_key = os.getenv('OPENAI_API_KEY')
    
    # Check if the key is just a placeholder
    if api_key and "your_openai_api_key_here" in api_key:
        api_key = None
        
    if not api_key:
        api_key = os.getenv('GOOGLE_API_KEY')
        # Check if Google key is placeholder
        if api_key and "your_google" in api_key:
            api_key = None
            
        if api_key:
            print("Using Google Gemini API")
        else:
            print("WARNING: No valid API key found. Using fallback methods.")
    else:
        print("Using OpenAI API")
    
    # Define input product data (ONLY source of truth - no external research)
    raw_product_data = {
        "name": "GlowBoost Vitamin C Serum",
        "concentration": "10% Vitamin C",
        "skin_type": "Oily, Combination",
        "key_ingredients": "Vitamin C, Hyaluronic Acid",
        "benefits": "Brightening, Fades dark spots",
        "how_to_use": "Apply 2–3 drops in the morning before sunscreen",
        "side_effects": "Mild tingling for sensitive skin",
        "price": "₹699"
    }
    
    # Initialize pipeline
    output_dir = os.path.join(os.path.dirname(__file__), "outputs")
    pipeline = ContentGenerationPipeline(output_dir=output_dir, api_key=api_key)
    
    # Run pipeline
    try:
        output_paths = pipeline.run(raw_product_data)
        
        print("\n" + "=" * 60)
        print("SUCCESS: All pages generated successfully!")
        print("=" * 60)
        
        return 0
        
    except Exception as e:
        print("\n" + "=" * 60)
        print(f"ERROR: Pipeline failed with error: {e}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
