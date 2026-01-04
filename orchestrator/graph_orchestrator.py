import os
import sys
from typing import Dict, Any, List, TypedDict, Annotated
from langgraph.graph import StateGraph, END

# Add parent directory for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from processors.product_parser import ProductParser
from agents.question_generator_agent import QuestionGeneratorAgent
from processors.content_processor import ContentProcessor
from processors.template_processor import TemplateProcessor
from processors.page_builder import PageBuilder
from orchestrator.answer_generator import AnswerGenerator
from orchestrator.execution_context import ExecutionContext

class PipelineState(TypedDict):
    raw_data: Dict[str, Any]
    structured_data: Dict[str, Any]
    questions: List[Dict[str, Any]]
    processed_content: Dict[str, Any]
    faq_questions: List[Dict[str, Any]]
    templates: Dict[str, Any]
    output_paths: Dict[str, str]
    execution_context: ExecutionContext
    api_key: str
    error: str

class GraphOrchestrator:
    def __init__(self, api_key: str = None, output_dir: str = "outputs"):
        self.api_key = api_key
        self.output_dir = output_dir
        
        # Initialize components
        self.parser = ProductParser()
        self.question_gen = QuestionGeneratorAgent(api_key=api_key)
        self.logic_processor = ContentProcessor()
        self.answer_gen = AnswerGenerator(api_key=api_key)
        self.template_processor = TemplateProcessor()
        self.builder = PageBuilder(output_dir=output_dir)
        
        # Build the graph
        self.workflow = self._create_workflow()
        self.app = self.workflow.compile()

    def _create_workflow(self):
        workflow = StateGraph(PipelineState)
        
        # Add nodes
        workflow.add_node("parse_product", self._node_parse_product)
        workflow.add_node("generate_questions", self._node_generate_questions)
        workflow.add_node("process_content", self._node_process_content)
        workflow.add_node("generate_answers", self._node_generate_answers)
        workflow.add_node("fill_templates", self._node_fill_templates)
        workflow.add_node("build_pages", self._node_build_pages)
        
        # Set edges
        workflow.set_entry_point("parse_product")
        workflow.add_edge("parse_product", "generate_questions")
        
        # Branching/Validation logic: Ensure 15+ questions
        workflow.add_conditional_edges(
            "generate_questions",
            self._decide_after_questions,
            {
                "continue": "process_content",
                "retry": "generate_questions"
            }
        )
        
        workflow.add_edge("process_content", "generate_answers")
        workflow.add_edge("generate_answers", "fill_templates")
        workflow.add_edge("fill_templates", "build_pages")
        workflow.add_edge("build_pages", END)
        
        return workflow

    # Node functions
    def _node_parse_product(self, state: PipelineState) -> Dict[str, Any]:
        print("\n[Node: parse_product] Parsing raw product data...")
        structured_data = self.parser.parse(state["raw_data"])
        state["execution_context"].record_agent("ProductParser")
        return {"structured_data": structured_data}

    def _node_generate_questions(self, state: PipelineState) -> Dict[str, Any]:
        print("\n[Node: generate_questions] Generating FAQ questions (LLM)...")
        questions = self.question_gen.generate_questions(state["structured_data"])
        state["execution_context"].record_agent("QuestionGeneratorAgent")
        return {"questions": questions}

    def _decide_after_questions(self, state: PipelineState) -> str:
        if len(state.get("questions", [])) < 15:
            print(f"  Warning: Only {len(state['questions'])} questions generated. Retrying node...")
            return "retry"
        return "continue"

    def _node_process_content(self, state: PipelineState) -> Dict[str, Any]:
        print("\n[Node: process_content] Applying business logic transformations...")
        processed_content = self.logic_processor.process_all_blocks(state["structured_data"])
        state["execution_context"].record_agent("ContentProcessor")
        return {"processed_content": processed_content}

    def _node_generate_answers(self, state: PipelineState) -> Dict[str, Any]:
        print("\n[Node: generate_answers] Generating contextual answers (LLM)...")
        # For FAQ, we take all 15+ questions generated
        faq_questions = self.answer_gen.generate_answers_batch(
            state["questions"],
            state["structured_data"],
            state["processed_content"]
        )
        state["execution_context"].record_agent("AnswerGenerator")
        return {"faq_questions": faq_questions}

    def _node_fill_templates(self, state: PipelineState) -> Dict[str, Any]:
        print("\n[Node: fill_templates] Populating page templates...")
        structured_data = state["structured_data"]
        faq_questions = state["faq_questions"]
        processed_content = state["processed_content"]
        
        templates = {}
        templates['faq'] = self.template_processor.fill_template(
            'faq', product_data=structured_data, questions=faq_questions
        )
        templates['product'] = self.template_processor.fill_template(
            'product', product_data=structured_data, 
            benefits_data=processed_content['benefits'],
            usage_data=processed_content['usage'],
            safety_data=processed_content['safety']
        )
        
        comparison_data = self.logic_processor.generate_comparison_data(structured_data)
        templates['comparison'] = self.template_processor.fill_template(
            'comparison',
            product_a_data=comparison_data['product_a'],
            product_b_data=comparison_data['product_b'],
            comparison_data=comparison_data['comparison']
        )
        
        state["execution_context"].record_agent("TemplateProcessor")
        return {"templates": templates}

    def _node_build_pages(self, state: PipelineState) -> Dict[str, Any]:
        print("\n[Node: build_pages] Saving final JSON artifacts...")
        output_paths = self.builder.build_all_pages(state["templates"], state["execution_context"])
        state["execution_context"].record_agent("PageBuilder")
        return {"output_paths": output_paths}

    def run(self, raw_product_data: Dict[str, Any]) -> Dict[str, str]:
        print("=" * 60)
        print("Starting LangGraph Content Generation Pipeline")
        print("=" * 60)
        
        initial_state = {
            "raw_data": raw_product_data,
            "structured_data": {},
            "questions": [],
            "processed_content": {},
            "faq_questions": [],
            "templates": {},
            "output_paths": {},
            "execution_context": ExecutionContext(),
            "api_key": self.api_key,
            "error": ""
        }
        
        try:
            final_state = self.app.invoke(initial_state)
            
            print("\n" + "=" * 60)
            print("PIPELINE COMPLETED SUCCESSFULLY")
            print("=" * 60)
            
            return final_state["output_paths"]
        except Exception as e:
            print(f"\nCritical Pipeline Failure: {e}")
            raise
