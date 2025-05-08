import operator
from typing import TypedDict, Annotated, List
from langchain_ollama import OllamaLLM
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.graph import StateGraph, END
import os


class AgentState(TypedDict):
    input: str      
    intermediate_steps: Annotated[List[str], operator.add]  
    response: str    
    search_query: str  
    search_results: str   


ollama_url = os.getenv("OLLAMA_BASE_URL", "http://host.docker.internal:11434")
llm = OllamaLLM(base_url=ollama_url, model="llama3.2:1b")
search_tool = DuckDuckGoSearchRun()


def log_step(state: AgentState, message: str) -> AgentState:
    steps = state.get("intermediate_steps", [])
    if message not in steps:  # Prevent any duplicate, not just consecutive ones
        print(f"[STEP] {message}")
        return {**state, "intermediate_steps": steps + [message]}
    return state



def plan_search(state: AgentState):
    if state.get("search_query"):
        return state

    state = log_step(state, "Planning search query")

    prompt = (
        f"You are a web based AI agent. Your job is to extract a clear, specific, and Google-searchable query "
        f"from the following question:\n\n"
        f"\"{state['input']}\"\n\n"
        "Generate ONE well-formed search query. Avoid explanations or punctuation. Include keywords of different types if u find relevant. "
        "Output only the search query, no quotes or extra text."
    )
    raw_query = llm.invoke(prompt).strip().split('\n')[0]
    query = raw_query.replace('"', '').strip()

   
    if len(query.split()) < 2 or not query[0].isalnum():
        state = log_step(state, f"Warning: Low-confidence search query generated: '{query}'")

    state = log_step(state, f"Generated search query: {query}")
    return {**state, "search_query": query}



def execute_search(state: AgentState):
    state = log_step(state, "Executing web search")
    query = state.get("search_query", "").strip()
    if not query:
        state = log_step(state, "No search query found. Skipping search.")
        return {**state, "search_results": ""}

    try:
        results = search_tool.run(query)
        state = log_step(state, f"Obtained search results (truncated): {results[:200]}...")
        return {**state, "search_results": results}
    except Exception as e:
        state = log_step(state, f"Search failed: {str(e)}")
        return {**state, "search_results": ""} 


def generate_answer(state: AgentState):
    state = log_step(state, "Synthesizing final answer")
    prompt = (
        f"Based on these search results, answer the question: {state['input']}\n\n"
        f"{state.get('search_results', '')}"
    )
    answer = llm.invoke(prompt).strip()
    state = log_step(state, "Final answer generated.")
    return {**state, "response": answer}



workflow = StateGraph(AgentState)
workflow.add_node("plan", plan_search)
workflow.add_node("search", execute_search)
workflow.add_node("answer", generate_answer)

workflow.set_entry_point("plan")
workflow.add_edge("plan", "search")
workflow.add_edge("search", "answer")
workflow.add_edge("answer", END)

agent = workflow.compile()



if __name__ == "__main__":
    user_question = "tell me advancement of AI in 2022?"
    initial_state = {
        "input": user_question,
        "intermediate_steps": [],
        "response": "",
        "search_query": "",
        "search_results": ""
    }    
    result = agent.invoke(initial_state)

    print("\n=== FINAL ANSWER ===\n", result["response"])
    print("\n=== SUMMARY OF STEPS ===")
    seen = set()
    deduped_steps = []
    for step in result["intermediate_steps"]:
        if step not in seen:
            deduped_steps.append(step)
            seen.add(step)

    for step in deduped_steps:
        print("-", step)


