from langchain_core.tools import tool


def create_search_tool(retriever):
    @tool
    def search_knowledge_base(query: str) -> str:
        """Search the enterprise knowledge base for factual information."""
        hits = retriever.search(query, 4)

        if not hits:
            return "No relevant documents were found."

        return "\n\n".join(
            f'[{h["source"]}#{h["chunk"]}] {h["text"]}'
            for h in hits
        )

    return search_knowledge_base
