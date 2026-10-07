from src.tools.retrieval import DocumentRetriever


retriever = DocumentRetriever()

retriever.index_document(
    "data/sec/nvda_10k.txt"
)


queries = {
    "competition": """
    What risks does NVIDIA describe
    regarding competition and competitors?
    """,

    "supply": """
    What risks does NVIDIA describe
    regarding suppliers, foundries,
    manufacturing, and supply constraints?
    """,

    "regulation": """
    What risks does NVIDIA describe
    regarding export controls,
    government regulation,
    China, and geopolitical restrictions?
    """
}


for topic, question in queries.items():

    print(
        f"\n\n===== {topic.upper()} ====="
    )

    results = retriever.retrieve(
        query=question,
        top_k=3
    )

    for i, result in enumerate(
        results,
        start=1
    ):

        print(
            f"\nRESULT {i}"
        )

        print(
            f"Similarity score: "
            f"{result['score']:.3f}"
        )

        print(
            result["text"][:1500]
        )