from llm.conversations.pdf_auto import get_pdf_auto_conversation

pdf_auto_conversation = get_pdf_auto_conversation()

LOAD_KNOWLEDGE_BASE = True
if LOAD_KNOWLEDGE_BASE and pdf_auto_conversation.knowledge_base:
    pdf_auto_conversation.knowledge_base.load(recreate=False)

pdf_auto_conversation.print_response("Tell me about food safety?")
pdf_auto_conversation.print_response("Share a good evening recipe?")
pdf_auto_conversation.print_response("How do I make chicken casserole?")
pdf_auto_conversation.print_response("Summarize our conversation")
