"""
Pipeline Orchestrator - Coordinates multi-agent workflow for content generation.

This module implements a DAG-like pipeline that orchestrates the flow of data
through multiple specialized agents to generate structured content pages.
"""

import sys
import os
from typing import Dict, Any, List

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.product_parser_agent import ProductParserAgent
from agents.question_generator_agent import QuestionGeneratorAgent
from agents.content_logic_agent import ContentLogicAgent
from agents.template_agent import TemplateAgent
from agents.page_builder_agent import PageBuilderAgent
from orchestrator.answer_generator import AnswerGenerator
from orchestrator.execution_context import ExecutionContext


class ContentGenerationPipeline:
    """
    Orchestrates the multi-agent content generation pipeline.
    
    Pipeline Stages (DAG-like flow):
    1. Parse Stage: ProductParserAgent → structured data
    2. Generate Stage: QuestionGeneratorAgent → categorized questions
    3. Process Stage: ContentLogicAgent → transformed content blocks
    4. Answer Stage: AnswerGenerator → FAQ answers
    5. Template Stage: TemplateAgent → populated templates (parallel for 3 pages)
    6. Build Stage: PageBuilderAgent → final JSON outputs
    
    LangChain is used only for agent coordination and message passing.
    Business logic remains in pure Python.
    """
    
    def __init__(self, output_dir: str = "outputs", api_key: str = None):
        """
        Initialize the pipeline with all agents.
        
        Args:
            output_dir: Directory for output files
            api_key: OpenAI API key for LLM-based agents
        """
        # Initialize all agents
        self.parser_agent = ProductParserAgent()
        self.question_agent = QuestionGeneratorAgent(api_key=api_key)
        self.logic_agent = ContentLogicAgent()
        self.template_agent = TemplateAgent()
        self.builder_agent = PageBuilderAgent(output_dir=output_dir)
        self.answer_generator = AnswerGenerator(api_key=api_key)
        
        # Pipeline state
        self.state = {}
        
        # Execution context for metadata tracking
        self.execution_context = None
    
    def run(self, raw_product_data: Dict[str, Any]) -> Dict[str, str]:
        """
        Execute the complete pipeline end-to-end.
        
        Args:
            raw_product_data: Raw product input data
            
        Returns:
            Dictionary mapping page names to output file paths
        """
        print("=" * 60)
        print("CONTENT GENERATION PIPELINE - STARTING")
        print("=" * 60)
        
        # Initialize execution context for this run
        self.execution_context = ExecutionContext()
        
        # Stage 1: Parse product data
        print("\n[Stage 1/6] Parsing product data...")
        structured_data = self._stage_parse(raw_product_data)
        print(f"✓ Parsed product: {structured_data.get('name')}")
        
        # Stage 2: Generate questions
        print("\n[Stage 2/6] Generating user questions...")
        questions = self._stage_generate_questions(structured_data)
        print(f"✓ Generated {len(questions)} questions across {len(set(q['category'] for q in questions))} categories")
        
        # Stage 3: Process content through logic blocks
        print("\n[Stage 3/6] Processing content through logic blocks...")
        processed_content = self._stage_process_content(structured_data)
        print(f"✓ Processed content: benefits, usage, safety")
        
        # Stage 4: Generate answers for FAQ
        print("\n[Stage 4/6] Generating FAQ answers...")
        faq_questions = self._stage_generate_answers(questions, structured_data, processed_content)
        print(f"✓ Generated answers for {len(faq_questions)} questions")
        
        # Stage 5: Fill templates (parallel)
        print("\n[Stage 5/6] Filling templates...")
        templates = self._stage_fill_templates(
            structured_data,
            faq_questions,
            processed_content
        )
        print(f"✓ Filled {len(templates)} templates: FAQ, Product, Comparison")
        
        # Stage 6: Build final JSON pages
        print("\n[Stage 6/6] Building JSON output files...")
        output_paths = self._stage_build_pages(templates)
        print(f"✓ Generated {len(output_paths)} JSON files")
        print(f"✓ Tracked {len(self.execution_context.agents_involved)} agents in execution metadata")
        
        print("\n" + "=" * 60)
        print("PIPELINE COMPLETED SUCCESSFULLY")
        print("=" * 60)
        print("\nGenerated files:")
        for filename, path in output_paths.items():
            print(f"  - {filename}: {path}")
        
        return output_paths
    
    def _stage_parse(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Stage 1: Parse and structure product data."""
        result = self.parser_agent.parse(raw_data)
        self.execution_context.record_agent("ProductParserAgent")
        return result
    
    def _stage_generate_questions(self, product_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Stage 2: Generate categorized questions."""
        result = self.question_agent.generate_questions(product_data)
        self.execution_context.record_agent("QuestionGeneratorAgent")
        return result
    
    def _stage_process_content(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Stage 3: Process content through all logic blocks."""
        result = self.logic_agent.process_all_blocks(product_data)
        self.execution_context.record_agent("ContentLogicAgent")
        return result
    
    def _stage_generate_answers(self, questions: List[Dict[str, Any]],
                                product_data: Dict[str, Any],
                                processed_content: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Stage 4: Generate answers for FAQ questions."""
        # Select top questions for FAQ (at least 5, distributed across categories)
        selected_questions = self._select_faq_questions(questions, min_count=5)
        
        # Generate answers
        result = self.answer_generator.generate_answers_batch(
            selected_questions,
            product_data,
            processed_content
        )
        self.execution_context.record_agent("AnswerGenerator")
        return result
    
    def _stage_fill_templates(self, product_data: Dict[str, Any],
                             faq_questions: List[Dict[str, Any]],
                             processed_content: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """Stage 5: Fill all templates (parallel operation)."""
        templates = {}
        
        # Fill FAQ template
        templates['faq'] = self.template_agent.fill_template(
            'faq',
            product_data=product_data,
            questions=faq_questions
        )
        
        # Fill Product template
        templates['product'] = self.template_agent.fill_template(
            'product',
            product_data=product_data,
            benefits_data=processed_content['benefits'],
            usage_data=processed_content['usage'],
            safety_data=processed_content['safety']
        )
        
        # Generate comparison data and fill Comparison template
        comparison_data = self.logic_agent.generate_comparison_data(product_data)
        templates['comparison'] = self.template_agent.fill_template(
            'comparison',
            product_a_data=comparison_data['product_a'],
            product_b_data=comparison_data['product_b'],
            comparison_data=comparison_data['comparison']
        )
        
        self.execution_context.record_agent("TemplateAgent")
        return templates
    
    def _stage_build_pages(self, templates: Dict[str, Dict[str, Any]]) -> Dict[str, str]:
        """Stage 6: Build final JSON pages."""
        pages = {
            'faq.json': templates['faq'],
            'product_page.json': templates['product'],
            'comparison_page.json': templates['comparison']
        }
        
        self.execution_context.record_agent("PageBuilderAgent")
        return self.builder_agent.build_all_pages(pages, self.execution_context)
    
    def _select_faq_questions(self, questions: List[Dict[str, Any]], 
                             min_count: int = 5) -> List[Dict[str, Any]]:
        """
        Select questions for FAQ, ensuring good distribution across categories.
        
        Args:
            questions: All generated questions
            min_count: Minimum number of questions to select
            
        Returns:
            Selected questions
        """
        # Group by category
        by_category = {}
        for q in questions:
            category = q.get('category', 'General')
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(q)
        
        # Select questions (at least 1 per category, then round-robin)
        selected = []
        
        # First, take 1 from each category
        for category, cat_questions in by_category.items():
            if cat_questions:
                selected.append(cat_questions[0])
        
        # If we need more, take additional questions round-robin
        if len(selected) < min_count:
            remaining_needed = min_count - len(selected)
            category_list = list(by_category.keys())
            cat_idx = 0
            question_idx = 1  # Start from second question in each category
            
            while remaining_needed > 0 and len(selected) < len(questions):
                category = category_list[cat_idx % len(category_list)]
                cat_questions = by_category[category]
                
                if question_idx < len(cat_questions):
                    selected.append(cat_questions[question_idx])
                    remaining_needed -= 1
                
                cat_idx += 1
                if cat_idx % len(category_list) == 0:
                    question_idx += 1
        
        return selected[:min_count] if len(selected) > min_count else selected
