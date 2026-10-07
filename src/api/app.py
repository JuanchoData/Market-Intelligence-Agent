from fastapi import FastAPI
from pydantic import BaseModel

from src.agent import build_agent


# ============================================================
# BUILD FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="Market Intelligence Agent",
    description=(
        "Agentic GenAI application using LangGraph, "
        "market analytics, SEC retrieval, and Llama 3.2."
    ),
    version="1.0.0"
)


# ============================================================
# BUILD LANGGRAPH AGENT ONCE
# ============================================================

agent = build_agent()


# ============================================================
# REQUEST MODEL
# ============================================================

class QueryRequest(BaseModel):
    """
    JSON body expected by the /query endpoint.
    """

    question: str


# ============================================================
# RESPONSE MODEL
# ============================================================

class QueryResponse(BaseModel):
    """
    JSON returned by the API.
    """

    route: str
    answer: str


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def root():
    """
    Simple endpoint to confirm the API is running.
    """

    return {
        "status": "running",
        "service": "Market Intelligence Agent"
    }


# ============================================================
# HEALTH ENDPOINT
# ============================================================

@app.get("/health")
def health():
    """
    Health check endpoint.
    """

    return {
        "status": "healthy"
    }


# ============================================================
# AGENT QUERY ENDPOINT
# ============================================================

@app.post(
    "/query",
    response_model=QueryResponse
)
def query_agent(
    request: QueryRequest
):
    """
    Send a question through the LangGraph agent.

    The router decides whether to use:
    - market analytics
    - SEC retrieval
    - both
    """

    result = agent.invoke(
        {
            "question": request.question,
            "route": "",
            "metrics": {},
            "sec_context": "",
            "answer": ""
        }
    )

    return QueryResponse(
        route=result["route"],
        answer=result["answer"]
    )