# 🏗️ GitHub RAG Chatbot - Architecture Diagram

## 📊 Complete System Architecture

```mermaid
flowchart TB
    subgraph UI["🎨 STREAMLIT UI - app.py"]
        A[User Interface]
    end

    subgraph PHASE1["🟣 PHASE 1: REPOSITORY INGESTION"]
        B[GitHub API]
        C[GithubFileLoader<br/>github_loader.py]
        D[Access Token Auth]
        E[Source Code Files]
        F[Documentation]
        G[Git Commits]
    end

    subgraph PHASE2["🔵 PHASE 2: SEMANTIC INDEXING"]
        H[Document Processor<br/>document_processor.py]
        I[AST Parser]
        J[Chunker]
        K[Sentence Transformers<br/>embeddings.py]
        L[Embeddings 384D]
        M[ChromaDB<br/>vector_store.py]
    end

    subgraph PHASE3["🟢 PHASE 3: CONTEXT RETRIEVAL"]
        N[User Query]
        O[Query Embedder<br/>retrieval.py]
        P[Vector Similarity Search]
        Q[Context Retriever]
        R[Retrieved Context]
    end

    subgraph PHASE4["🟠 PHASE 4: GROUNDED GENERATION"]
        S[LLM Groq<br/>llm.py]
        T[Answer Generator]
        U[References Provider]
        V[Final Answer]
    end

    A --> B
    A --> N
    B --> C
    C --> D
    D --> E
    D --> F
    D --> G
    E --> H
    F --> H
    G --> H
    H --> I --> J
    J --> K --> L
    L --> M
    N --> O
    O --> P
    M --> P
    P --> Q --> R
    R --> S
    S --> T --> U --> V
    V --> A

    style PHASE1 fill:#e6d5f5
    style PHASE2 fill:#d5e5f5
    style PHASE3 fill:#d5f5e5
    style PHASE4 fill:#f5e5d5
```

---

## 🔄 Detailed Data Flow

```mermaid
graph LR
    A[GitHub Repository] -->|GithubFileLoader| B[Code Files]
    B -->|Parse & Chunk| C[Text Chunks]
    C -->|Sentence Transformers| D[Embeddings]
    D -->|Store| E[ChromaDB]
    
    F[User Question] -->|Embed| G[Query Vector]
    G -->|Search| E
    E -->|Retrieve| H[Relevant Context]
    
    H -->|Input| I[Groq LLM]
    I -->|Generate| J[Answer + References]
```

---

## 📁 File Structure to Architecture Mapping

```mermaid
graph TD
    ROOT[GIT_rag_chatbot/]
    
    ROOT --> APP[app.py<br/>📱 Streamlit UI]
    ROOT --> SERVICES[services/]
    ROOT --> UTILS[utils/]
    ROOT --> ENV[.env<br/>🔑 API Keys]
    
    SERVICES --> S1[github_loader.py<br/>🟣 Phase 1]
    SERVICES --> S2[document_processor.py<br/>🔵 Phase 2 - Step 2]
    SERVICES --> S3[embeddings.py<br/>🔵 Phase 2 - Step 3]
    SERVICES --> S4[vector_store.py<br/>🔵 Phase 2 - Step 4]
    SERVICES --> S5[retrieval.py<br/>🟢 Phase 3]
    SERVICES --> S6[llm.py<br/>🟠 Phase 4]
    
    UTILS --> U1[helpers.py<br/>🛠️ Utilities]
    
    style S1 fill:#e6d5f5
    style S2 fill:#d5e5f5
    style S3 fill:#d5e5f5
    style S4 fill:#d5e5f5
    style S5 fill:#d5f5e5
    style S6 fill:#f5e5d5
```

---

## 🎯 Phase-by-Phase Component Diagram

### Phase 1: Repository Ingestion

```mermaid
flowchart LR
    A[User Input:<br/>GitHub URL] --> B[GitHub API<br/>Authentication]
    B --> C{Token Valid?}
    C -->|Yes| D[GithubFileLoader]
    C -->|No| E[Error: Invalid Token]
    D --> F[Load Files]
    F --> G[.py files]
    F --> H[.js files]
    F --> I[.md files]
    F --> J[Other code files]
    G & H & I & J --> K[Output: Documents]
    
    style A fill:#fff3cd
    style D fill:#e6d5f5
    style K fill:#d4edda
```

### Phase 2: Semantic Indexing

```mermaid
flowchart TD
    A[Input: Code Files] --> B[Document Processor]
    B --> C{File Type?}
    C -->|Python| D[AST Parser<br/>Python]
    C -->|JavaScript| E[AST Parser<br/>JS]
    C -->|Other| F[Text Parser]
    
    D & E & F --> G[Chunking<br/>Max 1000 tokens<br/>Overlap 200]
    G --> H[Text Chunks]
    
    H --> I[Sentence Transformers<br/>all-MiniLM-L6-v2]
    I --> J[384D Embeddings]
    
    J --> K[ChromaDB]
    K --> L[Vector Store<br/>+ Metadata]
    
    style B fill:#d5e5f5
    style I fill:#d5e5f5
    style L fill:#d5e5f5
```

### Phase 3: Context Retrieval

```mermaid
flowchart LR
    A[User Question:<br/>'How does auth work?'] --> B[Query Embedder]
    B --> C[384D Query Vector]
    
    D[ChromaDB<br/>Vector Store] --> E[Similarity Search]
    C --> E
    
    E --> F{Top-K Results<br/>K=5}
    F --> G[Result 1<br/>Score: 0.92]
    F --> H[Result 2<br/>Score: 0.88]
    F --> I[Result 3<br/>Score: 0.81]
    F --> J[Result 4<br/>Score: 0.76]
    F --> K[Result 5<br/>Score: 0.74]
    
    G & H & I & J & K --> L[Retrieved Context<br/>+ Metadata]
    
    style A fill:#fff3cd
    style E fill:#d5f5e5
    style L fill:#d4edda
```

### Phase 4: Grounded Generation

```mermaid
flowchart TD
    A[Retrieved Context] --> B[Prepare Prompt]
    C[User Question] --> B
    
    B --> D[System Prompt:<br/>You are a code expert...]
    D --> E[Context:<br/>Code snippets + metadata]
    E --> F[Question:<br/>User query]
    
    F --> G[Groq LLM<br/>llama-3.1-70b]
    G --> H[Generate Answer]
    
    H --> I[Extract References]
    I --> J{Has Sources?}
    J -->|Yes| K[Add File Names<br/>Line Numbers<br/>Commit IDs]
    J -->|No| L[Generic Answer]
    
    K --> M[Final Answer<br/>+ References]
    L --> M
    
    style G fill:#f5e5d5
    style M fill:#d4edda
```

---

## 🔐 Authentication & Configuration

```mermaid
flowchart LR
    A[.env File] --> B[GITHUB_PERSONAL_ACCESS_TOKEN]
    A --> C[GROQ_API_KEY]
    
    B --> D[GitHub API<br/>Authentication]
    C --> E[Groq LLM<br/>Authentication]
    
    D --> F[Access Repositories]
    E --> G[Generate Answers]
    
    style A fill:#fff3cd
    style B fill:#f8d7da
    style C fill:#f8d7da
```

---

## 📊 Data Storage Schema

```mermaid
erDiagram
    CHROMADB ||--o{ EMBEDDINGS : contains
    EMBEDDINGS ||--|| METADATA : has
    METADATA ||--|| DOCUMENT : references
    
    EMBEDDINGS {
        string id
        float[] vector_384d
        string collection_name
    }
    
    METADATA {
        string file_path
        string function_name
        int line_start
        int line_end
        string language
        string commit_sha
        string url
    }
    
    DOCUMENT {
        string content
        int chunk_id
        string source
    }
```

---

## 🚀 Tech Stack Overview

```mermaid
graph TB
    subgraph Frontend
        A[Streamlit]
    end
    
    subgraph DataLoading
        B[PyGithub]
        C[LangChain GithubFileLoader]
    end
    
    subgraph Processing
        D[LangChain TextSplitters]
        E[AST Parsing]
    end
    
    subgraph Embeddings
        F[Sentence Transformers]
        G[all-MiniLM-L6-v2]
    end
    
    subgraph VectorDB
        H[ChromaDB]
        I[HNSW Index]
    end
    
    subgraph LLM
        J[Groq API]
        K[Llama 3.1 70B]
    end
    
    A --> B & C
    B & C --> D & E
    D & E --> F & G
    F & G --> H & I
    H & I --> J & K
    J & K --> A
```

---

## ⚙️ Environment Setup Flow

```mermaid
flowchart TD
    A[Start Setup] --> B{Virtual Env Exists?}
    B -->|No| C[Create: python -m venv rag_env]
    B -->|Yes| D[Activate Env]
    C --> D
    
    D --> E[Install: pip install -r requirements.txt]
    E --> F{Installation Success?}
    
    F -->|No| G[Error: Check ChromaDB]
    F -->|Yes| H[Create .env file]
    
    H --> I[Add GITHUB_TOKEN]
    I --> J[Add GROQ_API_KEY]
    
    J --> K[Run: streamlit run app.py]
    K --> L[🎉 App Ready!]
    
    G --> E
    
    style C fill:#d5e5f5
    style H fill:#fff3cd
    style L fill:#d4edda
```

---

## 📝 File Responsibilities

| File | Phase | Responsibility |
|------|-------|----------------|
| `app.py` | All | Streamlit UI, orchestrates all phases |
| `services/github_loader.py` | 1 | GitHub API access, load repository files |
| `services/document_processor.py` | 2 | Parse and chunk code with AST awareness |
| `services/embeddings.py` | 2 | Generate 384D embeddings using Sentence Transformers |
| `services/vector_store.py` | 2 | ChromaDB initialization and storage |
| `services/retrieval.py` | 3 | Query embedding and similarity search |
| `services/llm.py` | 4 | Groq LLM integration and answer generation |
| `utils/helpers.py` | - | Utility functions across all modules |

---

## 🔄 Request-Response Flow

```mermaid
sequenceDiagram
    actor User
    participant UI as Streamlit UI
    participant Loader as GitHub Loader
    participant Processor as Doc Processor
    participant Embedder as Embeddings
    participant VectorDB as ChromaDB
    participant Retriever as Retrieval
    participant LLM as Groq LLM

    User->>UI: Enter GitHub URL
    UI->>Loader: Load repository
    Loader->>Processor: Send code files
    Processor->>Embedder: Send chunks
    Embedder->>VectorDB: Store embeddings
    VectorDB-->>UI: ✅ Repository indexed

    User->>UI: Ask question
    UI->>Retriever: Process query
    Retriever->>VectorDB: Search similar chunks
    VectorDB-->>Retriever: Return context
    Retriever->>LLM: Send context + query
    LLM-->>UI: Return answer + references
    UI-->>User: Display answer
```

---

## 🎯 Key Features

```mermaid
mindmap
  root((GitHub RAG Chatbot))
    Data Ingestion
      GitHub API
      File Filtering
      Commit History
    Processing
      AST Parsing
      Smart Chunking
      Multi-Language
    Embeddings
      Sentence Transformers
      Vector Storage
      Semantic Search
    Generation
      Groq LLM
      Context Grounding
      Source Citations
```

---

## 📚 API Keys Required

```mermaid
flowchart LR
    A[Get API Keys] --> B[GitHub Token<br/>github.com/settings/tokens]
    A --> C[Groq API Key<br/>console.groq.com/keys]
    
    B --> D[Permissions:<br/>✓ repo<br/>✓ public_repo]
    C --> E[Free Tier:<br/>✓ 30 requests/min<br/>✓ 14,400/day]
    
    D --> F[.env File]
    E --> F
    
    style B fill:#e6d5f5
    style C fill:#f5e5d5
    style F fill:#fff3cd
```

---

*Architecture Version: 1.0*  
*Created: 2026-01-16*  
*All diagrams render in GitHub, VS Code, and Markdown viewers*
