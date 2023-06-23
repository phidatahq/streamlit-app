from dataclasses import dataclass


@dataclass
class ApiEndpoints:
    LLM: str = "/llm"
    PING: str = "/ping"
    HEALTH: str = "/health"


endpoints = ApiEndpoints()
