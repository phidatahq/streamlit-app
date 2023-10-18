from llm.conversations.website_rag import get_website_rag_conversation

website_rag_conversation = get_website_rag_conversation()

LOAD_KNOWLEDGE_BASE = True
if LOAD_KNOWLEDGE_BASE and website_rag_conversation.knowledge_base:
    website_rag_conversation.knowledge_base.load(recreate=False)

website_rag_conversation.print_response("What is phidata?")
website_rag_conversation.print_response("How do I create a LLM App using phidata?")
