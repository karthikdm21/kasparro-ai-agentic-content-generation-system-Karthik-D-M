# Kasparro AI Agentic Content Generation System

## 1. Project Objective
This system is a modular agentic automation platform designed to transform a small product dataset into structured, machine-readable content pages (FAQ, Product Page, Comparison Page). It demonstrates advanced engineering in multi-agent workflows, automation graphs, and reusable content logic.

## 2. System Architecture (Automation Graph)
The system uses **LangGraph** to coordinate a multi-stage automation workflow. Unlike a linear script, this architecture provides explicit state management, error handling, and conditional branching.

### 2.1 Orchestration Workflow (DAG)
The pipeline operates as a Directed Acyclic Graph (DAG) with the following states and nodes:

| Node | Responsibility | Type |
| :--- | :--- | :--- |
| `parse_product` | Validates and structures raw input data. | Processor |
| `generate_questions` | Generates 15+ categorized user questions via LLM. | Agent |
| `validate_questions` | (Conditional) Ensures ≥15 questions exist; retries if needed. | Flow Control |
| `process_content` | Transforms data using reusable logic blocks. | Processor |
| `generate_answers` | Synthesizes contextual answers for FAQs via LLM. | Agent |
| `fill_templates` | Populates structured templates with transformed data. | Processor |
| `build_pages` | Assembles final JSON artifacts with metadata tracking. | Processor |

## 3. Requirement Compliance Matrix

| Requirement | Implementation Component | Method |
| :--- | :--- | :--- |
| **Parsing & Understanding** | [ProductParser](file:///d:/Applied_ai_project/kasparro-ai-agentic-content-generation-system-karthik/processors/product_parser.py) | Pydantic-style validation and normalization. |
| **15+ Categorized Questions** | [QuestionGeneratorAgent](file:///d:/Applied_ai_project/kasparro-ai-agentic-content-generation-system-karthik/agents/question_generator_agent.py) | LLM-backed (Gemini/OpenAI) with explicit validation node. |
| **Custom Templates** | [templates/](file:///d:/Applied_ai_project/kasparro-ai-agentic-content-generation-system-karthik/templates/) | Structured definitions for FAQ, Product, and Comparison. |
| **Reusable Logic Blocks** | [logic_blocks/](file:///d:/Applied_ai_project/kasparro-ai-agentic-content-generation-system-karthik/logic_blocks/) | Modules for benefits, usage, safety, and comparison rules. |
| **Fictional Competitor** | `generate_fictional_competitor` | Deterministic logic in `comparison_block.py`. |
| **Machine-Readable JSON** | `PageBuilder` | Validates and saves clean JSON to `outputs/`. |
| **Automated Orchestration** | [GraphOrchestrator](file:///d:/Applied_ai_project/kasparro-ai-agentic-content-generation-system-karthik/orchestrator/graph_orchestrator.py) | LangGraph StateMachine. |

## 4. Agents vs. Processors
To maintain high engineering standards, the system distinguishes between:
- **Agents**: LLM-backed nodes (Question/Answer Generation) that require external connectivity and retry logic.
- **Processors**: Deterministic Python nodes (Parsing, Logic, Templates) that ensure structural consistency and security.

## 5. Elimination of Fallbacks
Per the Anti-AI Gatekeeper Audit, all hardcoded "fallback" questions or answers have been removed. The system operates strictly via live LLM calls:
- **Strict Failure**: If an API key is missing or the LLM fails 3 times, the system raises a `RuntimeError`.
- **Validation**: Outputs are validated against Pydantic models and logic-based requirements (e.g., question count).

## 6. Execution Metadata
Each JSON output includes a `_meta` object for traceability:
```json
{
  "_meta": {
    "generated_by": "PageBuilder",
    "agents_involved": ["ProductParser", "QuestionGeneratorAgent", "ContentProcessor", "AnswerGenerator", "TemplateProcessor", "PageBuilder"],
    "execution_timestamp": "2026-01-02T22:00:00...",
    "pipeline_version": "1.0.0"
  }
}
```

## 7. Running the Pipeline
Ensure API keys are set in `.env` (OPENAI_API_KEY or GOOGLE_API_KEY).
```bash
python run_pipeline.py
```
*Note: The system requires a live LLM connection for Question and Answer generation.*
