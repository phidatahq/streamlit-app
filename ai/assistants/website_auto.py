from typing import Optional

from phi.assistant import Assistant
from phi.llm.openai import OpenAIChat

from ai.settings import ai_settings
from ai.storage import website_assistant_storage
from ai.knowledge_base import website_knowledge_base


def get_autonomous_website_assistant(
    run_id: Optional[str] = None,
    user_id: Optional[str] = None,
    debug_mode: bool = False,
) -> Assistant:
    """Get an Autonomous Assistant with a Website knowledge base."""

    return Assistant(
        name="auto_website_assistant",
        run_id=run_id,
        user_id=user_id,
        llm=OpenAIChat(
            model=ai_settings.gpt_4,
            max_tokens=ai_settings.default_max_tokens,
            temperature=ai_settings.default_temperature,
        ),
        storage=website_assistant_storage,
        knowledge_base=website_knowledge_base,
        monitoring=True,
        use_tools=True,
        show_tool_calls=True,
        debug_mode=debug_mode,
        description="You are a helpful assistant named 'phi' designed to answer questions about website contents.",
        extra_instructions=[
            "Keep your answers under 5 sentences.",
        ],
        assistant_data={"assistant_type": "autonomous"},
    )
