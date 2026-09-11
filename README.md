Desafio MBA Engenharia de Software com IA - Full Cycle

## Pré-requisitos

- Python 3.10+
- Docker e Docker Compose
- Chave de API da OpenAI

## Configuração

1. Copie o arquivo de exemplo e preencha sua chave:
   ```bash
   cp .env.example .env  # Windows (PowerShell): Copy-Item .env.example .env
   ```
   Edite `.env` com os campos abaixo:
   ```env
   OPENAI_API_KEY=sk-...
   OPENAI_EMBEDDING_MODEL=text-embedding-3-small
   OPENAI_CHAT_MODEL=gpt-4o-mini
   DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/rag
   PG_VECTOR_COLLECTION_NAME=rag_documents
   PDF_PATH=document.pdf
   ```

2. Coloque o PDF a ser ingerido na raiz do projeto com o nome `document.pdf`.

3. Crie e ative o ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

## Ordem de execução

### 1. Subir o banco de dados
```bash
docker compose up -d
```

### 2. Ingerir o PDF
```bash
python src/ingest.py
```

### 3. Iniciar o chat
```bash
python src/chat.py
```
