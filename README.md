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
