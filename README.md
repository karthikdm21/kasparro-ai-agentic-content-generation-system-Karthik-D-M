# Multi-Agent Content Generation System

A production-grade agentic automation system that generates structured, machine-readable content pages from product data using modular agents orchestrated by LangChain.

## Overview

This system demonstrates a **multi-agent architecture** where specialized agents work together to automatically generate FAQ, Product, and Comparison pages in JSON format. LangChain is used **only as a lightweight orchestrator** for agent coordination, while all business logic remains in pure Python.

## Features

- **5 Specialized Agents**: Each with single responsibility and stateless design
- **4 Reusable Logic Blocks**: Pure Python transformation functions
- **3 Structured Templates**: FAQ, Product, and Comparison page definitions
- **DAG-like Pipeline**: Orchestrated workflow with clear stage boundaries
- **Automated End-to-End**: Single command execution from input to JSON output
- **Execution Metadata**: Transparent tracking of agent execution order and timestamps

## System Architecture

```
Input Data → Parser → Question Generator → Content Logic → Template Agent → Page Builder → JSON Outputs
                ↓                              ↓
                └──────────── Answer Generator ─┘
```

### Agents

1. **ProductParserAgent**: Validates and structures raw product data
2. **QuestionGeneratorAgent**: Generates ≥15 categorized user questions using LLM
3. **ContentLogicAgent**: Routes to logic blocks and applies transformations
4. **TemplateAgent**: Fills structured templates with processed content
5. **PageBuilderAgent**: Assembles and writes final JSON files

### Logic Blocks

- `benefits_block.py`: Transforms benefits into structured descriptions
- `usage_block.py`: Formats usage instructions with steps and tips
- `safety_block.py`: Structures safety information and contraindications
- `comparison_block.py`: Implements feature-by-feature product comparison

## Installation

### Prerequisites

- Python 3.8+
- OpenAI API key OR Google API key (for LLM-based question and answer generation)

### Setup

1. **Clone or download this repository**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API key**:
   
   Create a `.env` file in the project root:
   ```env
   # Option 1: OpenAI (Default)
   OPENAI_API_KEY=your_openai_api_key_here
   
   # Option 2: Google Gemini (Recommended for free tier)
   GOOGLE_API_KEY=your_google_ai_studio_key_here
   ```
   *Note: If `GOOGLE_API_KEY` is present, the system will prioritize it and use the `gemini-2.5-flash` model.*

## Usage

### Run the Pipeline

Execute the complete pipeline with a single command:

```bash
python run_pipeline.py
```

### Expected Output

The pipeline will generate 3 JSON files in the `outputs/` directory:

- **faq.json**: FAQ page with ≥5 Q&A pairs across multiple categories
- **product_page.json**: Structured product information with benefits, usage, and safety
- **comparison_page.json**: Side-by-side comparison with a fictional competitor

### Pipeline Stages

The pipeline executes in 6 stages:

1. **Parse**: Structure and validate product data
2. **Generate**: Create categorized user questions
3. **Process**: Transform content through logic blocks
4. **Answer**: Generate FAQ answers using LLM
5. **Template**: Fill all templates (parallel)
6. **Build**: Write final JSON files

## Project Structure

```
kasparro-ai-agentic-content-generation-system-karthik/
│
├── agents/                      # Specialized agent modules
│   ├── product_parser_agent.py
│   ├── question_generator_agent.py
│   ├── content_logic_agent.py
│   ├── template_agent.py
│   └── page_builder_agent.py
│
├── logic_blocks/                # Reusable transformation logic
│   ├── benefits_block.py
│   ├── usage_block.py
│   ├── safety_block.py
│   └── comparison_block.py
│
├── templates/                   # Template definitions
│   ├── faq_template.py
│   ├── product_template.py
│   └── comparison_template.py
│
├── orchestrator/                # Pipeline coordination
│   ├── pipeline.py
│   └── answer_generator.py
│
├── outputs/                     # Generated JSON files
│   ├── faq.json
│   ├── product_page.json
│   └── comparison_page.json
│
├── docs/                        # Documentation
│   └── projectdocumentation.md
│
├── run_pipeline.py              # Main entry point
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variable template
└── README.md                    # This file
```

## Design Principles

### Multi-Agent Architecture

- **Single Responsibility**: Each agent has one clear purpose
- **Stateless Design**: Agents don't maintain state between calls
- **Explicit I/O**: Clear input/output contracts for each agent

### LangChain Usage

✅ **Used for**:
- Agent wrappers and coordination
- LLM interaction for question/answer generation
- Message passing between stages

❌ **NOT used for**:
- Business logic (in pure Python)
- Template definitions (in pure Python)
- Content transformation rules (in pure Python)

### Modularity

- **Logic blocks** are reusable across multiple templates
- **Templates** define structure with dependencies on logic blocks
- **Agents** can be tested and modified independently

## Input Data

The system uses **only** the following product data (no external research):

```python
{
    "name": "GlowBoost Vitamin C Serum",
    "concentration": "10% Vitamin C",
    "skin_type": "Oily, Combination",
    "key_ingredients": "Vitamin C, Hyaluronic Acid",
    "benefits": "Brightening, Fades dark spots",
    "how_to_use": "Apply 2–3 drops in the morning before sunscreen",
    "side_effects": "Mild tingling for sensitive skin",
    "price": "₹699"
}
```

## Output Format

All outputs are **valid JSON** files with structured data:

- **faq.json**: Questions categorized into Informational, Usage, Safety, Purchase, Comparison
- **product_page.json**: Sections for product info, benefits, usage, and safety
- **comparison_page.json**: Feature-by-feature comparison with fictional competitor

## Agent Execution Metadata

Each output file includes a `_meta` object that tracks the pipeline execution details:

```json
"_meta": {
  "generated_by": "PageBuilderAgent",
  "agents_involved": [
    "ProductParserAgent",
    "QuestionGeneratorAgent",
    "ContentLogicAgent",
    "AnswerGenerator",
    "TemplateAgent",
    "PageBuilderAgent"
  ],
  "execution_timestamp": "2025-12-25T11:49:29.212033",
  "pipeline_version": "1.0.0"
}
```

This feature provides transparency into the generation process without modifying the core business logic or template structures.

## Troubleshooting

### API Key Issues

If you don't have an OpenAI API key:
- The pipeline will use fallback methods for question generation
- Answers will still be generated but may be less contextual
- For best results, obtain an API key from OpenAI

### Import Errors

If you encounter import errors:
```bash
# Ensure you're running from the project root
cd kasparro-ai-agentic-content-generation-system-karthik
python run_pipeline.py
```

## Documentation

For detailed system design and architecture, see [docs/projectdocumentation.md](docs/projectdocumentation.md).

## License

This project is created as a demonstration of multi-agent system design.
