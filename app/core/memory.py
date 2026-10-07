from collections import defaultdict

class ConversationMemory:
    def __init__(self, max_messages: int = 12):
        self._store = defaultdict(list)
        self.max_messages = max_messages

    def history(self, session_id: str):
        return list(self._store.get(session_id, []))

    def add(self, session_id: str, role: str, content: str):
        self._store[session_id].append({"role": role, "content": content})
        self._store[session_id] = self._store[session_id][-self.max_messages:]
