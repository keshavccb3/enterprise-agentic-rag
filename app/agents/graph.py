from langgraph.graph import StateGraph, END
from langchain_ollama import ChatOllama
from app.agents.state import AgentState
from app.core.config import settings

class AgenticRAG:
    def __init__(self, retriever, memory):
        self.retriever = retriever
        self.memory = memory
        self.llm = ChatOllama(model=settings.ollama_model, base_url=settings.ollama_base_url, temperature=0)
        self.graph = self._build()

    def _route(self, state):
        q = state["query"].lower()

        direct_terms = (
            "hello",
            "hi",
            "hey",
            "who are you",
            "what can you do",
            "thank you",
            "thanks",
        )

        return {
            "route": "direct"
            if any(term in q for term in direct_terms)
            else "retrieve"
        }

    def _retrieve(self, state):
        hits = self.retriever.search(state["query"], 4)
        return {"context": "\n\n".join(f'[{h["source"]}#{h["chunk"]}] {h["text"]}' for h in hits), "sources": hits}

    def _generate(self, state):
        history = "\n".join(f'{m["role"]}: {m["content"]}' for m in self.memory.history(state["session_id"])[-6:])
        context = state.get("context", "")
        prompt = ("You are an enterprise knowledge assistant. Answer using the supplied context. "
                  "If context is insufficient, say so. Cite source names in brackets.\n\n"
                  f"Conversation:\n{history}\n\nContext:\n{context}\n\nQuestion: {state['query']}")
        if not context:
            prompt = f"You are a helpful enterprise assistant. Answer concisely.\n\nConversation:\n{history}\n\nQuestion: {state['query']}"
        answer = self.llm.invoke(prompt).content
        self.memory.add(state["session_id"], "user", state["query"])
        self.memory.add(state["session_id"], "assistant", answer)
        return {"answer": answer}

    def _build(self):
        g = StateGraph(AgentState)
        g.add_node("route", self._route)
        g.add_node("retrieve", self._retrieve)
        g.add_node("generate", self._generate)
        g.set_entry_point("route")
        g.add_conditional_edges("route", lambda s: s["route"], {"retrieve": "retrieve", "direct": "generate"})
        g.add_edge("retrieve", "generate")
        g.add_edge("generate", END)
        return g.compile()

    def invoke(self, query, session_id):
        state = self.graph.invoke({"query": query, "session_id": session_id})
        return {"answer": state.get("answer", ""), "route": state.get("route", "direct"), "sources": state.get("sources", [])}
