# Architecture Overview – AskNet: Web Lookup Agent

This document provides a technical overview of the AskNet project, highlighting its architecture, workflow, and core design components.

---

## 🧠 Objective

To build a web-based AI agent that can answer user questions by retrieving live information from the internet using an LLM-backed multi-step reasoning process.

---

## 🧱 Key Components

### 1. **Frontend (Gradio Interface)**

- Provides a simple chat-style interface for:
  - Entering user questions
  - Displaying answers
  - Showing step-by-step reasoning

### 2. **Backend (Python + LangGraph)**

The backend orchestrates a 3-phase reasoning pipeline using LangGraph:
1. **Plan a Search Query**
2. **Execute Internet Search**
3. **Generate Final Answer**

It tracks all intermediate steps in a state object for transparency.

### 3. **LLM (Ollama + LLaMA 3.2:1b)**

- Generates search queries from natural language questions
- Synthesizes answers using internet search results

### 4. **Web Search Tool (DuckDuckGoSearchRun)**

- Performs live web searches
- Fetches result snippets relevant to the generated search query

---

## 🔄 Agent Workflow Diagram

```
User Input
   ↓
[plan_search]
   ↓
[execute_search]
   ↓
[generate_answer]
   ↓
 Final Answer + Reasoning Logs
```

- **plan_search**: Uses the LLM to convert a natural question into a search-ready query.
- **execute_search**: Runs the query using DuckDuckGo and retrieves web snippets.
- **generate_answer**: Uses the LLM to synthesize a final response from those snippets.

---

## 🧾 Agent State Structure

The agent state is passed through each node in the workflow and evolves as follows:

```python
AgentState = {
    "input": "What is AI alignment?",
    "search_query": "AI alignment explanation",
    "search_results": "AI alignment is the field of...",
    "response": "AI alignment is...",
    "intermediate_steps": [
        "Planning search query",
        "Generated search query: AI alignment explanation",
        "Executing web search",
        "Obtained search results (truncated): ...",
        "Synthesizing final answer",
        "Final answer generated."
    ]
}
```

---

## 🔍 Design Principles

- **Transparency**: Each step is logged to `intermediate_steps` for traceability.
- **Modularity**: Each logical task is a standalone function in the LangGraph.
- **Extensibility**: New tools (e.g., Wikipedia search, calculator) can be added as new nodes.

---

## 📦 Extending the Architecture

Future enhancements may include:
- Additional tools like news APIs, Wikipedia, or WolframAlpha
- Support for larger LLMs via Ollama (e.g., LLaMA 3 8b or 70b)
- Database integration for caching or offline search

---

## ✅ Summary

AskNet combines:
- LangGraph for clean reasoning workflows,
- LLaMA 3 via Ollama for strong LLM capabilities,
- DuckDuckGoSearchRun for real-time internet access,
- and Gradio for an interactive UI.

This modular, containerized design ensures both usability and extensibility in real-world web-augmented AI applications.
