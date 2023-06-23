from typing import List

import openai
from fastapi import APIRouter
from pydantic import BaseModel
from phidata.utils.log import logger

from api.routes.endpoints import endpoints
from llm.schemas import Message
from llm.settings import llm_settings

# -*- Create a FastAPI router for llm endpoints
llm_router = APIRouter(prefix=endpoints.LLM, tags=["LLM"])


class PromptRequest(BaseModel):
    query: str = "Write a story about an AI named Phi."
    max_tokens: int = llm_settings.default_max_tokens
    temperature: float = llm_settings.default_temperature


class PromptResponse(BaseModel):
    output: str


@llm_router.post("/prompt", response_model=PromptResponse)
def llm_prompt_request(prompt_request: PromptRequest):
    """Send a prompt to the LLM and return the response."""

    # -*- Create a System Prompt
    system_prompt = "You are a helpful assistant that helps customers answer questions."

    # -*- Add the System Prompt to the conversation
    messages: List = []
    system_message = Message(role="system", content=system_prompt)
    messages.append(system_message.message())

    # -*- Add the user query to the conversation
    user_message = Message(role="user", content=prompt_request.query)
    messages.append(user_message.message())
    logger.info(f"LLM request: {messages}")

    # -*- Generate completion
    completion_result = openai.ChatCompletion.create(
        model=llm_settings.chat_gpt,
        messages=messages,
        max_tokens=prompt_request.max_tokens,
        temperature=prompt_request.temperature,
    )
    result = completion_result["choices"][0]["message"]["content"]
    logger.info(f"LLM response: {result}")

    # -*- Return result
    return PromptResponse(output=result)
