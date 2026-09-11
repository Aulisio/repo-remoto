import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector

load_dotenv()

PDF_PATH = os.getenv("PDF_PATH", "document.pdf")
CONNECTION_STRING = os.getenv("DATABASE_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/rag")
COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME", "rag_documents")
EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def validate_environment() -> None:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY nao definida. Crie o arquivo .env com OPENAI_API_KEY=<sua_chave>."
        )

    if not os.path.exists(PDF_PATH):
        raise FileNotFoundError(
            f"Arquivo PDF nao encontrado em '{PDF_PATH}'. Ajuste PDF_PATH no .env ou adicione o arquivo na raiz."
        )


def ingest_pdf():
    validate_environment()
    print(f"Carregando PDF: {PDF_PATH}")
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()
    print(f"{len(documents)} página(s) carregada(s).")

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = splitter.split_documents(documents)
    print(f"{len(chunks)} chunks gerados.")

    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)

    print("Salvando vetores no banco de dados...")
    PGVector.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        connection=CONNECTION_STRING,
        pre_delete_collection=True,
    )
    print("Ingestão concluída com sucesso.")


if __name__ == "__main__":
    ingest_pdf()