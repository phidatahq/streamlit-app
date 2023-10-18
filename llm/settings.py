from pydantic_settings import BaseSettings


class LLMSettings(BaseSettings):
    """LLM settings that can be set using environment variables.

    Reference: https://pydantic-docs.helpmanual.io/usage/settings/
    """

    gpt_4: str = "gpt-4"
    gpt_3_5: str = "gpt-3.5-turbo-16k"
    embedding_model: str = "text-embedding-ada-002"
    default_max_tokens: int = 1024
    default_temperature: float = 0


# Create LLMSettings object
llm_settings = LLMSettings()
