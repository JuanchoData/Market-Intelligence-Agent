# Market Intelligence Agent

An end-to-end Agentic GenAI application that combines financial analytics, SEC 10-K retrieval, LangGraph orchestration, FastAPI, Docker, and Llama 3.2 via Ollama.

## Overview

The Market Intelligence Agent is a portfolio project designed to demonstrate how structured financial analytics and unstructured company filings can be combined in a grounded GenAI workflow.

The system accepts natural-language questions about NVIDIA and routes each request to the appropriate tools.

It can:

- Analyze recent NVIDIA market behavior
- Calculate return, volatility, moving averages, and drawdown
- Retrieve relevant business risks from NVIDIA's SEC 10-K
- Combine structured financial analytics with unstructured SEC evidence
- Generate grounded natural-language responses using Llama 3.2
- Expose the workflow through a FastAPI REST API
- Run inside Docker
- Validate application behavior with automated tests
- Run continuous integration with GitHub Actions

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
```

---

## How It Works

### 1. User Question

A user sends a natural-language question such as:

```text
What is NVIDIA's recent volatility and 30-day return?
```

or:

```text
What are NVIDIA's main supply-chain risks?
```

or:

```text
How is NVIDIA's stock behaving and what business risks does the company report?
```

---

### 2. FastAPI Receives the Request

FastAPI exposes the application through a REST API.

The main endpoint is:

```text
POST /query
```

Example request:

```json
{
  "question": "What is NVIDIA's recent volatility and 30-day return?"
}
```

---

### 3. LangGraph Routes the Request

LangGraph acts as the orchestration layer.

A deterministic router identifies whether the question requires:

- Market analytics
- SEC risk retrieval
- Both

The router does not use the LLM for classification.

This keeps the routing logic simple, transparent, predictable, and inexpensive.

Example:

```text
Question:
"What is NVIDIA's recent volatility and 30-day return?"

Route:
market
```

---

## Market Analytics

For market-related questions, the application retrieves NVIDIA market data using `yfinance`.

Python then calculates metrics such as:

- Latest closing price
- 30-day return
- Annualized volatility
- 20-day moving average
- 50-day moving average
- Maximum drawdown
- Whether price is above or below its moving averages

An important design decision is that the LLM does not calculate these values.

Python performs the numerical calculations first, and the verified values are then passed to the LLM.

This reduces arithmetic hallucinations and makes the analytical workflow deterministic.

---

## SEC 10-K RAG Pipeline

For company-risk questions, the system uses NVIDIA's SEC 10-K filing as the grounding source.

The retrieval workflow is:

```text
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
```

### Risk-Factor Extraction

The retrieval pipeline focuses on:

```text
Item 1A. Risk Factors
```

This reduces noise from unrelated parts of the filing.

### Chunking

The Risk Factors section is split into smaller overlapping text chunks.

This allows the system to retrieve specific passages instead of sending the entire SEC filing to the LLM.

### Embeddings

The project uses:

```text
all-MiniLM-L6-v2
```

from Sentence Transformers.

The model converts text chunks into numerical embeddings.

These embeddings allow the system to compare the semantic meaning of a user's question with the SEC filing text.

### Retrieval

The most relevant chunks are selected using semantic similarity.

For example, a question about:

```text
export controls
```

can retrieve SEC passages discussing semiconductor regulation, AI GPU restrictions, international trade controls, and related risks.

---

## LLM Generation

The final natural-language response is generated using:

```text
Llama 3.2
```

The model runs locally through:

```text
Ollama
```

Llama is the large language model.

Ollama is the runtime used to serve Llama locally through an API.

The application sends the verified market metrics and/or retrieved SEC passages to Llama.

The prompt restricts the model to the supplied evidence and discourages unsupported claims.

The model is instructed not to:

- Invent news
- Infer investor sentiment
- Use unsupported prior knowledge
- Claim that SEC risks caused recent stock movements
- Treat volatility as a guaranteed future price range
- Invent facts that are not present in the provided context

---

## Why Separate Python Analytics from the LLM?

A central design choice in this project is to separate deterministic calculations from generative reasoning.

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

This is more reliable than asking the LLM to calculate financial metrics directly.

---

## Technology Stack

### GenAI and Orchestration

- Llama 3.2
- Ollama
- LangGraph

### Retrieval

- Sentence Transformers
- `all-MiniLM-L6-v2`
- Semantic similarity search

### Data and Analytics

- Python
- pandas
- NumPy
- yfinance

### API

- FastAPI
- Pydantic
- Uvicorn

### Testing

- pytest
- FastAPI TestClient
- unittest.mock

### Engineering and Deployment

- Docker
- Git
- GitHub
- GitHub Actions

---

## Project Structure

```text
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
```

---

## Example API Request

```json
{
  "question": "What is NVIDIA's recent volatility and 30-day return?"
}
```

Example response:

```json
{
  "route": "market",
  "answer": "Here are NVIDIA's recent volatility and 30-day return based on the verified market metrics:\n\n- Annualized volatility: 38.79%\n- 30-day return: 6.29%"
}
```

The exact values may change because the application retrieves current market data.

---

## Run the Project Locally

### 1. Clone the Repository

```bash
git clone https://github.com/JuanchoData/Market-Intelligence-Agent.git
cd Market-Intelligence-Agent
```

### 2. Create a Virtual Environment

On Windows PowerShell:

```powershell
python -m venv marketenv
.\marketenv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Ollama and Llama 3.2

Install Ollama on the host machine.

Then pull the model:

```bash
ollama pull llama3.2
```

Verify that it is available:

```bash
ollama list
```

You should see:

```text
llama3.2
```

### 5. Run the FastAPI Application

```bash
uvicorn src.api.app:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

---

## Run with Docker

The application can also run inside Docker.

The LLM itself is not packaged inside the application container.

The architecture is:

```text
Dockerized FastAPI Application
            |
            v
       Ollama on Host
            |
            v
         Llama 3.2
```

### Build the Docker Image

```bash
docker build -t market-intelligence-agent .
```

### Run the Container

On Docker Desktop:

```bash
docker run --rm -p 8000:8000 -e OLLAMA_URL=http://host.docker.internal:11434/api/generate market-intelligence-agent
```

This command:

- Starts the application container
- Maps host port 8000 to container port 8000
- Passes the Ollama API location as an environment variable
- Allows the Dockerized application to communicate with Llama 3.2 running on the host machine

Then open:

```text
http://127.0.0.1:8000/docs
```

---

## Testing

Run the test suite with:

```bash
pytest -v
```

The tests verify:

- Root API endpoint
- Health endpoint
- Market-query routing
- Valid API responses

External dependencies are mocked during automated testing.

For example:

- Live market-data calls are replaced with fixed test values
- Ollama/Llama calls are replaced with deterministic mock responses

This makes the test suite faster and reproducible.

---

## Continuous Integration

The repository uses GitHub Actions for continuous integration.

On every push or pull request to the `main` branch, GitHub automatically:

```text
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
```

This validates the application automatically without requiring access to the developer's local Ollama instance.

---

## Key Design Decisions

### Deterministic Routing

The router uses explicit rules instead of asking the LLM to decide which tool should be used.

This makes the routing behavior transparent and predictable.

### Deterministic Financial Calculations

Financial metrics are calculated in Python rather than generated by the LLM.

### Grounded RAG

Business-risk answers are grounded in retrieved SEC 10-K passages.

### Separation of Application and Model Runtime

The FastAPI/LangGraph application runs separately from the LLM runtime.

The model endpoint is configured through:

```text
OLLAMA_URL
```

This allows the LLM backend to be changed without tightly coupling it to the application.

### Mocked External Dependencies in CI

Automated tests do not require live market services or a local LLM.

This improves reproducibility and reliability.

---

## Current Scope

This project is a portfolio demonstration of an Agentic GenAI architecture.

The current implementation:

- Focuses on NVIDIA
- Uses one SEC 10-K filing
- Uses Llama 3.2 locally
- Uses an in-memory embedding workflow
- Uses deterministic keyword routing
- Does not provide financial advice
- Is not presented as a production trading system

---

## Future Improvements

Potential extensions include:

- Support for multiple companies and tickers
- Dynamic ticker extraction
- Automatic SEC filing ingestion
- Persistent vector database
- Embedding caching
- Conversation memory
- Hybrid or LLM-based routing
- Authentication and authorization
- Logging and observability
- Model monitoring
- Cloud deployment
- Dedicated LLM inference service
- More extensive unit tests
- Integration tests
- Retrieval evaluation with Recall@K and Precision@K
- Grounded-response evaluation
- Source citations in generated answers

---

## What This Project Demonstrates

This project demonstrates experience with:

- Generative AI application design
- Large language models
- Retrieval-Augmented Generation
- Embeddings
- Semantic search
- Agent orchestration
- Structured financial analytics
- Unstructured document retrieval
- REST API development
- Automated testing
- Dependency mocking
- Docker containerization
- Git version control
- GitHub Actions CI
- Reproducible AI software engineering

---

## Interview Summary

A concise way to describe the project:

> I built an end-to-end Agentic GenAI market-intelligence application. LangGraph routes user questions to market analytics, SEC 10-K retrieval, or both. Python performs deterministic financial calculations, Sentence Transformers provides semantic retrieval over SEC Risk Factors, and Llama 3.2 generates grounded natural-language responses through Ollama. I exposed the workflow through FastAPI, containerized the application with Docker, added automated tests with mocked external dependencies, and implemented GitHub Actions CI.

---

## Disclaimer

This project is intended for educational and portfolio purposes only.

It is not financial advice and should not be used as the sole basis for investment decisions.
