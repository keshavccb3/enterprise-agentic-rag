from app.agents.graph import AgenticRAG
from app.core.memory import ConversationMemory
from app.rag.retriever import VectorRetriever

retriever = VectorRetriever()
memory = ConversationMemory()
agent = AgenticRAG(retriever, memory)

def initialize():
    return retriever.rebuild()

def chat(query, session_id):
    return agent.invoke(query, session_id)
