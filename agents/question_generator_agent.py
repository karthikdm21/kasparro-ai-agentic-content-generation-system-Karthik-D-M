from typing import Dict, Any, List
import os
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field


class Question(BaseModel):
    question: str = Field(description="The user question")
    category: str = Field(description="Category: Informational, Usage, Safety, Purchase, or Comparison")


class QuestionList(BaseModel):
    questions: List[Question] = Field(description="List of generated questions")


class QuestionGeneratorAgent:
    
    def __init__(self, api_key: str = None):
        self.agent_name = "QuestionGeneratorAgent"
        self.api_key = api_key
        
        # Determine provider based on available key or env vars
        self.provider = "openai"
        
        if api_key:
            # Auto-detect provider from key format
            if api_key.startswith("AIza"):
                self.provider = "google"
            elif api_key.startswith("sk-"):
                self.provider = "openai"
        else:
            # Fallback to env vars if no key provided
            if os.getenv("GOOGLE_API_KEY") and "your_google" not in os.getenv("GOOGLE_API_KEY"):
                self.provider = "google"
                api_key = os.getenv("GOOGLE_API_KEY")
            elif os.getenv("OPENAI_API_KEY") and "your_open" not in os.getenv("OPENAI_API_KEY"):
                self.provider = "openai"
                api_key = os.getenv("OPENAI_API_KEY")
        
        if api_key:
            try:
                if self.provider == "google":
                    self.llm = ChatGoogleGenerativeAI(
                        model="gemini-2.5-flash",
                        temperature=0.7,
                        google_api_key=api_key,
                        convert_system_message_to_human=True
                    )
                else:
                    self.llm = ChatOpenAI(
                        model="gpt-3.5-turbo",
                        temperature=0.7,
                        api_key=api_key
                    )
                self.parser = PydanticOutputParser(pydantic_object=QuestionList)
                self.use_llm = True
            except Exception as e:
                print(f"Warning: Failed to initialize LLM ({self.provider}): {e}")
                self.use_llm = False
        else:
            self.use_llm = False
    
    def generate_questions(self, product_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        if not self.use_llm:
            print("  Using fallback question generation (no API key)")
            return self._generate_fallback_questions(product_data)
        
        template = """You are a skincare expert helping to generate realistic user questions about a product.

Product Information:
- Name: {name}
- Concentration: {concentration}
- Skin Type: {skin_type}
- Key Ingredients: {key_ingredients}
- Benefits: {benefits}
- How to Use: {how_to_use}
- Side Effects: {side_effects}
- Price: {price}

Generate at least 15 realistic questions that users might ask about this product.
Categorize each question into one of these categories:
- Informational: Questions about what the product is, ingredients, formulation
- Usage: Questions about how to use the product
- Safety: Questions about side effects, contraindications, safety
- Purchase: Questions about price, value, where to buy
- Comparison: Questions comparing this to other products

Ensure a good distribution across all categories (at least 2 questions per category).

{format_instructions}
"""
        
        prompt = ChatPromptTemplate.from_template(template)
        
        formatted_prompt = prompt.format_messages(
            name=product_data.get('name', ''),
            concentration=product_data.get('concentration', ''),
            skin_type=product_data.get('skin_type', ''),
            key_ingredients=product_data.get('key_ingredients', ''),
            benefits=product_data.get('benefits', ''),
            how_to_use=product_data.get('how_to_use', ''),
            side_effects=product_data.get('side_effects', ''),
            price=product_data.get('price', ''),
            format_instructions=self.parser.get_format_instructions()
        )
        
        response = self.llm.invoke(formatted_prompt)
        
        try:
            parsed_output = self.parser.parse(response.content)
            questions = [
                {
                    "question": q.question,
                    "category": q.category
                }
                for q in parsed_output.questions
            ]
        except Exception as e:
            print(f"Warning: Failed to parse LLM output: {e}")
            questions = self._generate_fallback_questions(product_data)
        
        return questions
    
    def _generate_fallback_questions(self, product_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        name = product_data.get('name', 'this product')
        
        return [
            {"question": f"What is {name}?", "category": "Informational"},
            {"question": f"What are the key ingredients in {name}?", "category": "Informational"},
            {"question": f"What skin types is {name} suitable for?", "category": "Informational"},
            {"question": f"How do I use {name}?", "category": "Usage"},
            {"question": f"When should I apply {name}?", "category": "Usage"},
            {"question": f"Can I use {name} with other products?", "category": "Usage"},
            {"question": f"What are the side effects of {name}?", "category": "Safety"},
            {"question": f"Is {name} safe for sensitive skin?", "category": "Safety"},
            {"question": f"Are there any contraindications for {name}?", "category": "Safety"},
            {"question": f"How much does {name} cost?", "category": "Purchase"},
            {"question": f"Is {name} worth the price?", "category": "Purchase"},
            {"question": f"Where can I buy {name}?", "category": "Purchase"},
            {"question": f"How does {name} compare to other Vitamin C serums?", "category": "Comparison"},
            {"question": f"What makes {name} different from competitors?", "category": "Comparison"},
            {"question": f"Should I choose {name} or a higher concentration serum?", "category": "Comparison"}
        ]
