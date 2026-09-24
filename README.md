LangGraph Content Orchestrator (langgraph-content-orchestrator)
An autonomous multi-agent content generation system built with LangGraph, LangChain, and local AI (Ollama llama2). This project demonstrates an orchestrated workflow where a Supervisor AI coordinates a Researcher AI and a Writer AI to create factual articles with built-in SQLite memory persistence.

📌 How the Team Works (Workflow Diagram)
<img width="741" height="573" alt="image" src="https://github.com/user-attachments/assets/cb6adbd5-621b-4294-a3a2-a67de94a9b96" />

🤖 Meet the AI Agents
<img width="729" height="273" alt="image" src="https://github.com/user-attachments/assets/75df412b-bbc2-439a-8d95-9edd5372a1c3" />


📂 Repository File Breakdown
main.py: Primary Python script containing the LangGraph state graph, node definitions, and execution flow.
checkpoints.db: SQLite database file used by SqliteSaver to record state memory at every step.
run_log.txt: Live execution log showing a real test run on the topic "what is the css".
task7.png: Diagram image showing the state machine graph layout.
README.md: Technical project documentation.

🛠️ Simple Technology Summary
<img width="741" height="257" alt="image" src="https://github.com/user-attachments/assets/7d582b24-c860-4c83-a506-0b014894d125" />


