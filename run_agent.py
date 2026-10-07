from src.agent import build_agent


# Build the LangGraph agent
agent = build_agent()


# Ask the user for a question
question = input(
    "Ask a market intelligence question: "
)


# Run the agent
result = agent.invoke(
    {
        "question": question,
        "route": "",
        "metrics": {},
        "sec_context": "",
        "answer": ""
    }
)


# Show which route LangGraph selected
print("\nROUTE")
print(result["route"])


# Show the final LLM-generated answer
print("\nFINAL ANSWER")
print(result["answer"])