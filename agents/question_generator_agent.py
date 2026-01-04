import os
import time
from typing import Dict, Any, List
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
    """Generates 15+ FAQ questions via LLM."""
    
    def __init__(self, api_key: str = None):
        self.agent_name = "QuestionGeneratorAgent"
        self.api_key = api_key
        
        if api_key:
            if api_key.startswith("AIza"):
                self.provider = "google"
            elif api_key.startswith("sk-"):
                self.provider = "openai"
        else:
            if os.getenv("GOOGLE_API_KEY") and "your_google" not in os.getenv("GOOGLE_API_KEY"):
                self.provider = "google"
                api_key = os.getenv("GOOGLE_API_KEY")
            elif os.getenv("OPENAI_API_KEY") and "your_open" not in os.getenv("OPENAI_API_KEY"):
                self.provider = "openai"
                api_key = os.getenv("OPENAI_API_KEY")
        
        self.api_key = api_key
        
        if not api_key:
            raise RuntimeError("QuestionGeneratorAgent: No valid API key provided. System must explicitly fail.")
            
        try:
            if self.provider == "google":
                self.llm = ChatGoogleGenerativeAI(
                    model="gemini-2.0-flash",
                    temperature=0.7,
                    google_api_key=api_key,
                    convert_system_message_to_human=True
                )
            else:
                self.llm = ChatOpenAI(
                    model="gpt-4o-mini",
                    temperature=0.7,
                    api_key=api_key
                )
            self.parser = PydanticOutputParser(pydantic_object=QuestionList)
        except Exception as e:
            raise RuntimeError(f"QuestionGeneratorAgent: Failed to initialize LLM ({self.provider}): {e}")

    def generate_questions(self, product_data: Dict[str, Any], max_retries: int = 3) -> List[Dict[str, Any]]:
        """LLM-backed question generation with 15+ requirement enforcement."""
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

Generate exactly 15 or more realistic questions that users might ask about this product.
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
        
        last_exception = None
        for attempt in range(max_retries):
            try:
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
                parsed_output = self.parser.parse(response.content)
                
                questions = [
                    {"question": q.question, "category": q.category}
                    for q in parsed_output.questions
                ]
                
                # Validation: Enforce 15+ questions
                if len(questions) < 15:
                    print(f"  Validation failed: Generated only {len(questions)} questions. Retrying...")
                    continue
                    
                return questions
                
            except Exception as e:
                print(f"  Attempt {attempt + 1} failed: {e}")
                last_exception = e
                time.sleep(1) # Simple backoff
        
        raise RuntimeError(f"QuestionGeneratorAgent: Failed to generate valid questions after {max_retries} attempts. Last error: {last_exception}")
