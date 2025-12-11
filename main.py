
import os
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from typing import TypedDict, Literal
import sqlite3

# Remove existing checkpoints for a fresh start
if os.path.exists("checkpoints.db"):
    os.remove("checkpoints.db")

# State
class AgentState(TypedDict):
    topic: str
    research: str
    draft: str
    next_step: Literal["researcher", "writer", "FINISH"]

# LLM
llm = ChatOllama(model="llama2", temperature=0)

# Supervisor
def supervisor(state: AgentState):
    if state.get("draft"):
        return {"next_step": "FINISH"}
    if state.get("research"):
        return {"next_step": "writer"}
    return {"next_step": "researcher"}

# Researcher
def researcher(state: AgentState):
    prompt = f"Give exactly 5 short bullet points about: {state['topic']}"
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"research": response.content}

# Writer
def writer(state: AgentState):
    prompt = f"""Write a beautiful 150-200 word article about: {state['topic']}
Use only these facts:
{state['research']}"""
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"draft": response.content}

# Build graph
conn = sqlite3.connect("checkpoints.db", check_same_thread=False)
memory = SqliteSaver(conn)

builder = StateGraph(AgentState)
builder.add_node("supervisor", supervisor)
builder.add_node("researcher", researcher)
builder.add_node("writer", writer)

builder.set_entry_point("supervisor")
builder.add_conditional_edges(
    "supervisor",
    lambda s: s["next_step"],
    {"researcher": "researcher", "writer": "writer", "FINISH": END}
)
builder.add_edge("researcher", "supervisor")
builder.add_edge("writer", "supervisor")

graph = builder.compile(checkpointer=memory)


print("Multi-Agent Swarm with llama2 (temperature=0) - FIXED!")
topic = input("\nEnter topic: ") or "what is a rainbow"

print("\nAgents working...")
print("=" * 70)

config = {"configurable": {"thread_id": "1"}}

# Track what we already showed
showed_supervisor_researcher = False
showed_supervisor_writer = False
showed_supervisor_finish = False
showed_research = False
showed_draft = False

for step in graph.stream({"topic": topic}, config, stream_mode="values"):
    s = step
    
    
    if not s.get("research") and not showed_supervisor_researcher:
        print("SUPERVISOR: Decides RESEARCHER (no research yet).")
        print("-" * 70)
        showed_supervisor_researcher = True
    
    
    if s.get("research") and not showed_research:
        print("RESEARCHER: Gathered facts.")
        print(s["research"])
        print("-" * 70)
        showed_research = True
    
    
    if s.get("research") and not s.get("draft") and not showed_supervisor_writer and showed_research:
        print("SUPERVISOR: Decides WRITER (research done, no article yet).")
        print("-" * 70)
        showed_supervisor_writer = True
    
  
    if s.get("draft") and not showed_draft:
        print("WRITER: Article complete.")
        print(s["draft"])
        print("-" * 70)
        showed_draft = True
    
    
    if s.get("draft") and not showed_supervisor_finish and showed_draft:
        print("SUPERVISOR: Decides FINISH (article done).")
        print("-" * 70)
        showed_supervisor_finish = True

print("Done! Checkpoints saved in checkpoints.db (persistent memory).")