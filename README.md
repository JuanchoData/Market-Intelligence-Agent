# Market Intelligence Agent

An end-to-end Agentic GenAI application that combines market analytics, SEC 10-K retrieval, LangGraph orchestration, FastAPI, Docker, and Llama 3.2 via Ollama.

## Overview

The Market Intelligence Agent is a portfolio project designed to demonstrate how structured financial analytics and unstructured company filings can be combined in a grounded GenAI workflow.

The system accepts natural-language questions about NVIDIA and routes them to the appropriate tools.

It can:

- Analyze recent market behavior
- Calculate return, volatility, moving averages, and drawdown
- Retrieve relevant business risks from NVIDIA's SEC 10-K
- Combine structured analytics with unstructured SEC evidence
- Generate grounded natural-language responses using Llama 3.2
- Expose the workflow through a FastAPI REST API
- Run in Docker
- Validate application behavior with automated tests and GitHub Actions CI

---

## Architecture

```text
                    User Question
                         |
                         v
                      FastAPI
                         |
                         v
                 LangGraph Router
                  /      |       \
                 /       |        \
                v        v         v
            Market      SEC      Combined
            Route       RAG       Route
              |          |          |
              v          v          |
         Yahoo Finance   SEC 10-K   |
              |          |          |
              v          v          |
          Python      Chunking      |
          Metrics     + Embeddings  |
              |          |          |
              |      Semantic       |
              |      Retrieval      |
              \          |         /
               \         |        /
                \        v       /
                  Grounded Context
                         |
                         v
                    Llama 3.2
                    via Ollama
                         |
                         v
                   Final Response


How It Works
1. User Question
A user sends a question such as:
What is NVIDIA's recent volatility and 30-day return?

or:
What are NVIDIA's main supply-chain risks?

or:
How is NVIDIA's stock behaving and what business risks does the company report?

2. FastAPI Receives the Request
FastAPI exposes the application through a REST API.
The main endpoint is:
POST /query

Example request:
{
  "question": "What is NVIDIA's recent volatility and 30-day return?"
}

3. LangGraph Routes the Request
LangGraph acts as the orchestration layer.
A deterministic router identifies whether the question requires:
- Market analytics
- SEC risk retrieval
- Both
The router does not use the LLM for classification. This keeps the routing logic simple, predictable, and inexpensive.
Example:
Question:
"What is NVIDIA's recent volatility and 30-day return?"

Route:
market

Market Analytics
For market-related questions, the application retrieves NVIDIA market data using yfinance.
Python then calculates metrics such as:
- Latest closing price
- 30-day return
- Annualized volatility
- 20-day moving average
- 50-day moving average
- Maximum drawdown
- Whether price is above or below moving averages
An important design choice is that the LLM does not calculate these values.
Python performs the numerical calculations first, and the verified values are then provided to the LLM.
This reduces arithmetic hallucinations and makes the analytical workflow deterministic.
SEC 10-K RAG Pipeline
For company-risk questions, the system uses NVIDIA's SEC 10-K filing as the grounding source.
The workflow is:
SEC 10-K
   |
   v
Item 1A Risk Factors
   |
   v
Text Chunking
   |
   v
Sentence Transformer Embeddings
   |
   v
Semantic Similarity Search
   |
   v
Relevant SEC Passages
   |
   v
Llama 3.2

Risk-Factor Extraction
The retrieval pipeline focuses on:
Item 1A. Risk Factors

This reduces noise from unrelated sections of the filing.
Chunking
The Risk Factors section is split into smaller overlapping text chunks.
This allows the system to retrieve specific passages instead of sending the entire filing to the LLM.
Embeddings
The project uses:
all-MiniLM-L6-v2

from Sentence Transformers.
The model converts text chunks into numerical embeddings.
These embeddings allow the application to compare the semantic meaning of the user's question with the SEC text.
Retrieval
The most relevant chunks are selected using similarity scores.
For example, a question about:
export controls

retrieves passages related to semiconductor regulation, AI GPU restrictions, and international trade controls.
LLM Generation
The final response is generated using:
Llama 3.2

The model runs locally through:
Ollama

Llama is the language model.
Ollama is the runtime used to serve the model locally through an API.
The application sends the verified market metrics and/or retrieved SEC passages to Llama.
The prompt restricts the model to the supplied evidence and explicitly discourages unsupported claims.
For example, the model is instructed not to:
- Invent news
- Infer investor sentiment
- Claim that SEC risks caused recent stock movements
- Use prior knowledge outside the supplied evidence
- Treat volatility as a guaranteed price range
Why Separate Python Analytics from the LLM?
A central design decision in this project is to separate deterministic calculations from generative reasoning.
Python handles:
- Returns
- Volatility
- Moving averages
- Drawdown
- Price comparisons
The LLM handles:
- Natural-language explanation
- Summarization
- Interpretation of retrieved SEC evidence
This creates a more reliable architecture than asking the LLM to calculate financial metrics directly.
Technology Stack
GenAI and Orchestration
- Llama 3.2
- Ollama
- LangGraph
Retrieval
- Sentence Transformers
- all-MiniLM-L6-v2
- Semantic similarity search
Data and Analytics
- Python
- pandas
- NumPy
- yfinance
API
- FastAPI
- Pydantic
- Uvicorn
Testing
- pytest
- FastAPI TestClient
- unittest.mock
Deployment and Engineering
- Docker
- Git
- GitHub
- GitHub Actions
Project Structure
Market-Intelligence-Agent/
|
├── .github/
│   └── workflows/
│       └── ci.yml
|
├── data/
│   └── sec/
│       └── nvda_10k.txt
|
├── src/
│   ├── __init__.py
│   ├── agent.py
│   ├── llm.py
│   |
│   ├── api/
│   │   ├── __init__.py
│   │   └── app.py
│   |
│   └── tools/
│       ├── __init__.py
│       ├── analytics.py
│       ├── market_data.py
│       ├── retrieval.py
│       └── sec_ingestion.py
|
├── tests/
│   └── test_api.py
|
├── .dockerignore
├── .gitignore
├── Dockerfile
├── requirements.txt
├── run_agent.py
└── README.md

Example API Response
Request:
{
  "question": "What is NVIDIA's recent volatility and 30-day return?"
}

Example response:
{
  "route": "market",
  "answer": "Here are NVIDIA's recent volatility and 30-day return based on the verified market metrics:\n\n- Annualized volatility: 38.79%\n- 30-day return: 6.29%"
}

The values can change because the system retrieves current market data.
Running the Project Locally
1. Clone the Repository
git clone https://github.com/JuanchoData/Market-Intelligence-Agent.git
cd Market-Intelligence-Agent

2. Create a Virtual Environment
Windows PowerShell:
python -m venv marketenv
.\marketenv\Scripts\Activate.ps1

3. Install Dependencies
pip install -r requirements.txt

4. Install Ollama
Install Ollama on the host machine.
Then pull Llama 3.2:
ollama pull llama3.2

Verify that the model is available:
ollama list

5. Run the FastAPI Application
uvicorn src.api.app:app --reload

Open:
http://127.0.0.1:8000/docs

Running with Docker
The application can also run inside Docker.
The LLM itself is not packaged inside the application container.
Instead:
Dockerized Application
        |
        v
Ollama on Host Machine
        |
        v
Llama 3.2

Build the Docker Image
docker build -t market-intelligence-agent .

Run the Container
On Docker Desktop:
docker run --rm -p 8000:8000 \
  -e OLLAMA_URL=http://host.docker.internal:11434/api/generate \
  market-intelligence-agent

This command:
- Starts the application container
- Maps port 8000 from the container to the host
- Passes the Ollama API address as an environment variable
- Allows the Dockerized FastAPI application to communicate with Llama 3.2 running on the host
Then open:
http://127.0.0.1:8000/docs

Testing
Run the test suite with:
pytest -v

The tests verify:
- Root API endpoint
- Health endpoint
- Market-query routing
- Valid API responses
External dependencies are mocked during automated testing.
For example:
- Live Yahoo Finance calls are replaced with test values
- Ollama/Llama calls are replaced with deterministic mock responses
This makes the tests faster and reproducible.
Continuous Integration
The repository uses GitHub Actions for continuous integration.
On every push or pull request to main, GitHub automatically:
Checks out the repository
        |
        v
Installs Python 3.11
        |
        v
Installs dependencies
        |
        v
Runs pytest
        |
        v
Pass / Fail

This validates the application automatically without requiring access to the developer's local Ollama instance.
Key Design Decisions
Deterministic Routing
The router uses explicit keyword rules instead of asking an LLM to decide which tool to use.
This makes the routing behavior transparent and predictable.
Deterministic Numerical Analytics
Financial metrics are calculated in Python rather than generated by the LLM.
Grounded RAG
Business-risk answers are grounded in retrieved SEC 10-K passages.
Separation of Application and Model Runtime
The FastAPI/LangGraph application runs separately from the LLM runtime.
The model endpoint is configured through:
OLLAMA_URL

This makes the model backend replaceable without tightly coupling it to the application.
Mocked External Dependencies in CI
Automated tests do not require live market services or a local LLM.
This improves reproducibility and reliability.
Current Scope
This project is a portfolio demonstration of Agentic GenAI architecture.
The current implementation:
- Focuses on NVIDIA
- Uses one SEC 10-K filing
- Uses Llama 3.2 locally
- Uses an in-memory embedding workflow
- Uses deterministic keyword routing
- Does not provide financial advice
- Is not presented as a production trading system
Future Improvements
Potential extensions include:
- Support for multiple companies and tickers
- Dynamic ticker extraction
- Automatic SEC filing ingestion
- Persistent vector database
- Embedding caching
- Conversation memory
- LLM-based or hybrid routing
- Authentication and authorization
- Logging and observability
- Model monitoring
- Cloud deployment
- Dedicated LLM inference service
- More extensive unit and integration tests
- Evaluation metrics for retrieval quality and grounded generation
What This Project Demonstrates
This project demonstrates experience with:
- GenAI application design
- Large language models
- Retrieval-Augmented Generation
- Embeddings and semantic search
- Agent orchestration
- Financial data analytics
- REST API development
- Automated testing
- Dependency mocking
- Docker containerization
- GitHub Actions CI
- Reproducible ML/AI software engineering
Interview Summary
A concise explanation of the project:
I built an end-to-end Agentic GenAI market-intelligence application. LangGraph routes user questions to market analytics, SEC 10-K retrieval, or both. Python performs deterministic financial calculations, Sentence Transformers provides semantic retrieval over SEC Risk Factors, and Llama 3.2 generates grounded natural-language responses through Ollama. I exposed the workflow using FastAPI, containerized the application with Docker, added automated tests with mocked external dependencies, and implemented GitHub Actions CI.

Disclaimer
This project is intended for educational and portfolio purposes only.
It is not financial advice and should not be used as the sole basis for investment decisions.

Then save the file and push it:

```powershell
git add README.md
git commit -m "Improve project documentation"
git push




