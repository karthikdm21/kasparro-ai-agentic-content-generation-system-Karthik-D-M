import os
import time
from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


class AnswerGenerator:
    """Generates product Q&A answers via LLM."""
    
    def __init__(self, api_key: str = None):
        """
        Initialize the Answer Generator.
        """
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
        
        if not api_key:
            raise RuntimeError("AnswerGenerator: No valid API key provided. System must explicitly fail.")
            
        try:
            if self.provider == "google":
                from langchain_google_genai import ChatGoogleGenerativeAI
                self.llm = ChatGoogleGenerativeAI(
                    model="gemini-2.0-flash",
                    temperature=0.7,
                    google_api_key=api_key
                )
            else:
                self.llm = ChatOpenAI(
                    model="gpt-4o-mini",
                    temperature=0.7,
                    api_key=api_key
                )
        except Exception as e:
            raise RuntimeError(f"AnswerGenerator: Failed to initialize LLM ({self.provider}): {e}")

    def generate_answer(self, question: str, product_data: Dict[str, Any], 
                       processed_content: Dict[str, Any], max_retries: int = 3) -> str:
        """LLM-backed answer generation with retry logic."""
        template = """You are a skincare expert answering customer questions about a product.

Product Information:
- Name: {name}
- Concentration: {concentration}
- Skin Type: {skin_type}
- Key Ingredients: {key_ingredients}
- Benefits: {benefits}
- How to Use: {how_to_use}
- Side Effects: {side_effects}
- Price: {price}

Additional Context:
- Benefits Summary: {benefits_summary}
- Usage Instructions: {usage_instructions}
- Safety Information: {safety_info}

Question: {question}

Provide a helpful, accurate answer based ONLY on the product information provided above. 
Do not add any information that is not in the product data.
Keep the answer concise (2-3 sentences) and professional.

Answer:"""
        
        prompt = ChatPromptTemplate.from_template(template)
        
        # Extract processed content
        benefits_data = processed_content.get('benefits', {})
        usage_data = processed_content.get('usage', {})
        safety_data = processed_content.get('safety', {})
        
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
                    benefits_summary=benefits_data.get('benefits_summary', ''),
                    usage_instructions=usage_data.get('full_instructions', ''),
                    safety_info=', '.join(safety_data.get('precautions', [])),
                    question=question
                )
                
                # Generate answer
                response = self.llm.invoke(formatted_prompt)
                return response.content.strip()
            except Exception as e:
                print(f"  Attempt {attempt + 1} for answer failed: {e}")
                last_exception = e
                time.sleep(1)
        
        raise RuntimeError(f"AnswerGenerator: Failed to generate answer after {max_retries} attempts. Last error: {last_exception}")

    def generate_answers_batch(self, questions: List[Dict[str, Any]], 
                               product_data: Dict[str, Any],
                               processed_content: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate answers for multiple questions.
        """
        questions_with_answers = []
        
        for q in questions:
            question_text = q.get('question', '')
            answer = self.generate_answer(question_text, product_data, processed_content)
            
            questions_with_answers.append({
                "question": question_text,
                "answer": answer,
                "category": q.get('category', 'General')
            })
        
        return questions_with_answers
