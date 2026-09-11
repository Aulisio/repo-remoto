import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_postgres import PGVector

load_dotenv()

CONNECTION_STRING = os.getenv("DATABASE_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/rag")
COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME", "rag_documents")
EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-5-mini")

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se não houver resultados relevantes no vetor, ou se o score estiver muito ruim ou
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.
- Sempre que o contexto for sobre faturamento compare todos os valores de faturamento explicitamente presentes no contexto. Não infira. Se houver vários valores, escolha o maior. Se o faturamento não estiver explícito para alguma empresa, não use essa empresa como referência.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""


def search_prompt():
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY nao definida. Crie o arquivo .env com OPENAI_API_KEY=<sua_chave>."
        )

    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    store = PGVector(
        embeddings=embeddings,
        collection_name=COLLECTION_NAME,
        connection=CONNECTION_STRING,
    )
    llm = ChatOpenAI(model=CHAT_MODEL, temperature=0)

    def chain(question: str) -> str:
        results = store.similarity_search_with_score(question, k=10)
        contexto = "\n\n".join(doc.page_content for doc, _ in results)
        prompt = PROMPT_TEMPLATE.format(contexto=contexto, pergunta=question)
        response = llm.invoke(prompt)
        return response.content

    return chain