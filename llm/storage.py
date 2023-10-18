from phi.conversation.storage.postgres import PgConversationStorage

from db.session import db_url

pdf_conversation_storage = PgConversationStorage(
    table_name="pdf_conversations",
    db_url=db_url,
    schema="llm",
)

website_conversation_storage = PgConversationStorage(
    table_name="website_conversations",
    db_url=db_url,
    schema="llm",
)
