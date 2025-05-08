# AskNet: AI-Powered Web Lookup Agent

AskNet is a containerized web-based AI agent that intelligently answers questions using live web searches and LLM reasoning. It uses LangGraph for workflow logic, DuckDuckGoSearchRun for search integration, and Ollama with LLaMA 3 for language generation. A Gradio interface allows easy interaction with the agent.

---

## 🧰 Step-by-Step Project Setup (Local)

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/asknet-agent.git
cd asknet-agent
```

### Step 2: Set Up a Python Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Ensure Ollama is Running with LLaMA 3 Model

Download and start the LLaMA model using Ollama:

```bash
ollama serve
ollama run llama3
```

If Ollama is running remotely or in Docker, configure the URL using:

```bash
export OLLAMA_BASE_URL=http://localhost:11434  # Adjust as needed
```

### Step 5: Run the Backend Agent

```bash
python main.py
```

### Step 6: Launch the Gradio Interface (Frontend)

```bash
python gradio_ui.py
```

Visit `http://localhost:7860` in your browser to start chatting with the AI agent.

---

## 🧠 Tools & LLMs Used

| Tool/Library              | Description |
|---------------------------|-------------|
| **LangGraph**             | Manages the structured agent workflow |
| **LangChain**             | Integration of LLM tools and state |
| **DuckDuckGoSearchRun**   | Web search integration |
| **Ollama + LLaMA 3.2:1b** | Local LLM for search query generation and synthesis |
| **Gradio**                | Web interface for user input/output |
| **Docker**                | Containerization for backend deployment |

---

## 🌐 How Internet Search Is Integrated

The agent logic follows these steps:

1. **Plan Search Query**  
   The agent receives a natural language question and uses an LLM to generate a well-formed, keyword-rich search query.

2. **Execute Search**  
   The query is passed to DuckDuckGoSearchRun, which fetches relevant online results.

3. **Generate Final Answer**  
   The LLM (LLaMA 3) processes the search results to synthesize a clear, accurate response to the user's original question.

4. **Logging Steps**  
   All intermediate steps—query formulation, search execution, and answer generation—are logged in a list called `intermediate_steps`.

This design ensures the agent is both **transparent** and **traceable** in its reasoning.

---

## 📁 Folder Structure

```
asknet-agent/
├── main.py               # LangGraph-based agent logic
├── gradio_ui.py          # Gradio chat interface
├── requirements.txt      # Python dependencies
├── Dockerfile            # Container definition for backend
├── README.md             # Project overview and instructions
└── docs/
    └── architecture.md   # High-level architecture and workflow description
```

---

## 🐳 Docker Support (Optional)

You can build and run the backend agent in a Docker container:

```bash
docker build -t asknet-agent .
docker run -p 8000:8000 asknet-agent
```

Make sure to expose the Ollama server or set the correct `OLLAMA_BASE_URL`.

---

## 📄 License

This project is licensed under the MIT License.
