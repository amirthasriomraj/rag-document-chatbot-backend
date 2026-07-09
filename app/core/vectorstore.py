from langchain_community.vectorstores import Chroma

CHROMA_PERSIST_DIR = "chroma_db"


def get_vectorstore():
    return Chroma(
        persist_directory=CHROMA_PERSIST_DIR,
        collection_name="rag_documents"
    )