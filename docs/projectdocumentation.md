# Multi-Agent Content Generation System

## Problem Statement

Creating structured, consistent, and high-quality marketing content (FAQs, product pages, comparisons) for a large inventory of products is time-consuming and error-prone when done manually. Ensuring that all content is accurate, SEO-friendly, and follows a specific brand voice requires significant human effort. Moreover, maintaining consistency across different content types (safety warnings, usage instructions) is difficult at scale without automation.

## Solution Overview

The **Kasparro AI Agentic Content Generation System** serves as an intelligent automation pipeline that transforms raw product data into fully formatted, ready-to-publish content. By orchestrating specialized AI agents, the system automates the generation of:

- **Comprehensive FAQs** with context-aware answers.
- **Detailed Product Pages** including benefits, usage instructions, and safety warnings.
- **Competitive Comparison Pages** against fictional or real competitors.

The solution leverages Large Language Models (LLMs) via LangChain for creative tasks (question generation, answer synthesis) while using deterministic Python logic for structural consistency and safety compliance.

## Scopes & Assumptions

### Scope
- **Input**: Structured JSON product data.
- **Output**: Three distinct JSON files (FAQ, Product Page, Comparison Page) per product containing execution metadata.
- **Agents**: Parser, Question Generator, Content Logic, Answer Generator, Template Filler, Page Builder.
- **Integration**: Supports OpenAI (GPT-3.5/4) and Google Gemini (gemini-2.5-flash) models.

### Assumptions
- Input data is well-formed and contains essential fields (name, description, features).
- Valid API keys for OpenAI or Google Gemini are provided in the environment.
- The system runs in a Python 3.8+ environment.
- Generated content is strictly based on provided product data to minimize hallucinations.

## System Design

![System Architecture](system_architecture.png)

The system is designed as a **staged pipeline** where each agent performs a specific transformation on the data. This modular approach ensures that the system is easy to debug, test, and extend.

### Core Components

- **Orchestrator (`pipeline.py`)**: The central nervous system that manages the flow of data between agents. It ensures that each stage receives the necessary context and handles errors gracefully.
- **LLM-Powered Agents**:
  - `QuestionGeneratorAgent`: Crafting user-centric questions using few-shot prompting.
  - `AnswerGenerator`: Synthesizing product data into concise, accurate answers.
- **Deterministic Logic Agents**:
  - `ProductParserAgent`: Enforces data integrity at the entry point.
  - `ContentLogicAgent`: Executes complex business rules (e.g., safety checks, benefit extraction) without LLM overhead.
- **Page Assembly Agents**:
  - `TemplateAgent`: Maps processed data to visual/structural components.
  - `PageBuilderAgent`: Finalizes the output and attaches execution telemetry.

### Data Flow

1. **Ingestion**: Raw product JSON is validated and transformed into a standard `ProductData` object.
2. **Expansion**: The system generates a broad set of queries and scenarios based on the product attributes.
3. **Refinement**: Content blocks are processed through specialized logic gates (Safety, Benefits, Comparison).
4. **Synthesis**: LLMs generate natural language responses based on the refined data.
5. **Finalization**: Data is serialized into multiple JSON formats with attached execution metadata.

## Project Structure

```
├── agents/                    # Specialized agents (Parser, Question Gen, etc.)
├── logic_blocks/              # Reusable transformation functions (Safety, Benefits, etc.)
├── templates/                 # Page structure definitions (FAQ, Product, Comparison)
├── orchestrator/              # Pipeline coordination and LLM management
├── outputs/                   # Generated JSON production assets
└── run_pipeline.py            # Automated execution entry point
```

## Key Design Principles

1. **LangChain for Coordination Only**: LLMs are used strictly for creativity, not for data routing or business logic.
2. **Pure Python Logic**: All structural transformations and safety checks are implemented in standard Python for 100% predictability.
3. **Single Responsibility**: Each agent has one clear purpose, making the system highly maintainable.
4. **Stateless execution**: No internal state is preserved between runs, ensuring reliability across different product datasets.
