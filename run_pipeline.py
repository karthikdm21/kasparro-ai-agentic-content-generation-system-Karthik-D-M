import os
import sys
from dotenv import load_dotenv

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from orchestrator.graph_orchestrator import GraphOrchestrator


def main():
    """Execute the content generation pipeline."""
    
    # Load environment variables
    load_dotenv()
    
    # Get API key from environment (OpenAI or Google)
    api_key = os.getenv('OPENAI_API_KEY')
    
    if api_key and "your_openai_api_key_here" in api_key:
        api_key = None
        
    if not api_key:
        api_key = os.getenv('GOOGLE_API_KEY')
        if api_key and "your_google" in api_key:
            api_key = None
            
        if api_key:
            print("Using Google Gemini API")
    else:
        print("Using OpenAI API")
    
    if not api_key:
        print("ERROR: No valid API key found. The system requires a live LLM to function.")
        return 1
    
    # Product data source
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
    orchestrator = GraphOrchestrator(api_key=api_key, output_dir=output_dir)
    
    # Run pipeline
    try:
        output_paths = orchestrator.run(raw_product_data)
        
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
