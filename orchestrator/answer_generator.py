"""
Answer Generator - Uses LangChain to generate answers to questions based on product data.

This module uses LangChain with an LLM to generate contextual answers to user questions.
"""

from typing import Dict, Any, List
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


class AnswerGenerator:
    """
    Generates answers to questions using LangChain and LLM.
    
    This is used by the orchestrator to generate FAQ answers.
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize the Answer Generator.
        
        Args:
            api_key: OpenAI API key (optional, can use env var)
        """
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
        
        # Only initialize LLM if API key is available
        if api_key:
            try:
                if self.provider == "google":
                    # Import here to avoid issues if package missing
                    from langchain_google_genai import ChatGoogleGenerativeAI
                    self.llm = ChatGoogleGenerativeAI(
                        model="gemini-2.5-flash",
                        temperature=0.7,
                        google_api_key=api_key
                    )
                else:
                    self.llm = ChatOpenAI(
                        model="gpt-3.5-turbo",
                        temperature=0.7,
                        api_key=api_key
                    )
                self.use_llm = True
            except Exception as e:
                print(f"Warning: Failed to initialize LLM for answers ({self.provider}): {e}")
                self.use_llm = False
        else:
            self.use_llm = False
    
    def generate_answer(self, question: str, product_data: Dict[str, Any], 
                       processed_content: Dict[str, Any]) -> str:
        """
        Generate an answer to a question based on product data.
        
        Args:
            question: The user question
            product_data: Raw product information
            processed_content: Processed content from logic blocks
            
        Returns:
            Generated answer string
        """
        # Use fallback if LLM not available
        if not self.use_llm:
            return self._generate_fallback_answer(question, product_data, processed_content)
        
        # Create prompt template
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
        
        # Format the prompt
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
    
    def generate_answers_batch(self, questions: List[Dict[str, Any]], 
                               product_data: Dict[str, Any],
                               processed_content: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate answers for multiple questions.
        
        Args:
            questions: List of question dictionaries
            product_data: Product information
            processed_content: Processed content from logic blocks
            
        Returns:
            List of questions with answers added
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
    
    def _generate_fallback_answer(self, question: str, product_data: Dict[str, Any],
                                  processed_content: Dict[str, Any]) -> str:
        """
        Generate a basic fallback answer when LLM is not available.
        
        Args:
            question: The question to answer
            product_data: Product information
            processed_content: Processed content from logic blocks
            
        Returns:
            Basic answer string
        """
        question_lower = question.lower()
        name = product_data.get('name', 'this product')
        
        # Simple keyword-based answer generation
        if 'what is' in question_lower or 'what are' in question_lower:
            if 'ingredient' in question_lower:
                return f"{name} contains {product_data.get('key_ingredients', 'active ingredients')}."
            else:
                return f"{name} is a {product_data.get('concentration', 'vitamin C')} serum designed for {product_data.get('skin_type', 'various skin types')}."
        
        elif 'how' in question_lower and 'use' in question_lower:
            return f"{product_data.get('how_to_use', 'Apply as directed on the product label')}."
        
        elif 'side effect' in question_lower or 'safe' in question_lower:
            return f"Possible side effects include: {product_data.get('side_effects', 'none reported')}. Always perform a patch test before use."
        
        elif 'price' in question_lower or 'cost' in question_lower:
            return f"{name} is priced at {product_data.get('price', 'competitive market rates')}."
        
        elif 'benefit' in question_lower:
            benefits_data = processed_content.get('benefits', {})
            return benefits_data.get('benefits_summary', f"{name} offers {product_data.get('benefits', 'skincare benefits')}.")
        
        elif 'compare' in question_lower or 'different' in question_lower:
            return f"{name} features {product_data.get('concentration', '')} with {product_data.get('key_ingredients', 'quality ingredients')}, making it suitable for {product_data.get('skin_type', 'various skin types')}."
        
        else:
            # Generic answer
            return f"For detailed information about {name}, please refer to the product specifications. It contains {product_data.get('key_ingredients', 'active ingredients')} and is priced at {product_data.get('price', 'competitive rates')}."
