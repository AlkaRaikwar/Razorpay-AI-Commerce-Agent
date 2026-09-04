#  📝 Previous conversation/context

from typing import List, Dict

class ConversationMemory:
    def __init__(self):
        self.messages: List[Dict[str, str]] = []

    def add(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})

    def get_messages(self):
        return self.messages

    def clear(self):
        self.messages.clear()
