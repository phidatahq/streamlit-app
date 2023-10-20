from phi.knowledge.pdf import PDFUrlKnowledgeBase, PDFKnowledgeBase, PDFReader  # noqa
from phi.knowledge.website import WebsiteKnowledgeBase
from phi.vectordb.pgvector import PgVector

from db.session import db_url

pdf_knowledge_base = PDFUrlKnowledgeBase(
    urls=[
        "https://www.family-action.org.uk/content/uploads/2019/07/meals-more-recipes.pdf"
    ],
    # Table name: llm.pdf_documents
    vector_db=PgVector(
        collection="pdf_documents",
        db_url=db_url,
        schema="llm",
    ),
    num_documents=2,
)

# -*- To use local PDFs instead of URLs, uncomment the following lines -*-
# pdf_knowledge_base = PDFKnowledgeBase(
#     path="data/pdfs",
#     # Table name: llm.pdf_documents
#     vector_db=PgVector(
#         collection="pdf_documents",
#         db_url=db_url,
#         schema="llm",
#     ),
# )

website_knowledge_base = WebsiteKnowledgeBase(
    urls=["https://www.phidata.com"],
    # Number of links to follow from the seed URLs
    max_links=10,
    # Table name: llm.website_documents
    vector_db=PgVector(
        collection="website_documents",
        db_url=db_url,
        schema="llm",
    ),
    num_documents=3,
)
