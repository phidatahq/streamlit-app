from pydantic import BaseModel


class Message(BaseModel):
    """
    Message class for holding LLM messages.
    """

    role: str
    content: str

    def message(self):
        return {"role": self.role, "content": self.content}
