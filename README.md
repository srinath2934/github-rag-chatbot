# 🤖 GitHub RAG Chatbot

An intelligent chatbot that lets you chat with any GitHub repository using Retrieval Augmented Generation (RAG).

## 🌟 Features

- 📦 Connect to any GitHub repository
- 🧠 Smart code parsing and chunking
- 🔍 Semantic search across codebase
- 💬 Chat with your code in natural language
- 📚 Get answers with source references (files, functions, commits)

## 🏗️ Architecture

Based on a 4-phase pipeline:
1. **Repository Ingestion** - Clone and load GitHub repos
2. **Semantic Indexing** - Parse, chunk, embed, and store code
3. **Context Retrieval** - Find relevant code snippets
4. **Grounded Generation** - Generate answers with LLM + references

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Vector DB**: ChromaDB
- **Embeddings**: Sentence Transformers
- **LLM**: Groq (Llama 3.1)
- **Framework**: LangChain

## 🚀 Setup

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Set up environment variables**:
```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

3. **Get Groq API Key**:
   - Visit: https://console.groq.com/keys
   - Create a free account
   - Generate API key
   - Add to `.env` file

4. **Run the app**:
```bash
streamlit run app.py
```

## 📖 Usage

1. Enter a GitHub repository URL
2. Click "Index Repository" to process the code
3. Ask questions about the codebase
4. Get intelligent answers with source references!

## 📁 Project Structure

```
GIT_rag_chatbot/
├── app.py                      # Main Streamlit UI
├── services/                   # Core functionality
│   ├── github_loader.py        # GitHub repo loading
│   ├── document_processor.py   # Code parsing & chunking
│   ├── embeddings.py           # Vector embeddings
│   ├── vector_store.py         # ChromaDB management
│   ├── retrieval.py            # Context retrieval
│   └── llm.py                  # LLM integration
├── utils/                      # Helper functions
├── requirements.txt            # Dependencies
└── .env                        # API keys (not in git)
```

## 📝 License

MIT License
