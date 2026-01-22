# 🤖 GitHub RAG Chatbot

A production-ready AI chatbot that lets you ask questions about any GitHub repository using Retrieval-Augmented Generation (RAG) and semantic search.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31+-red)
![License](https://img.shields.io/badge/License-MIT-green)

## 🌟 Features

### Core Capabilities
- 🔍 **Semantic Code Search** - Find relevant code using meaning, not just keywords
- 🤖 **AI-Powered Answers** - Get intelligent responses using Groq's LLaMA 3.1 70B
- 📚 **Citation Tracking** - See exactly which files and functions were used
- 💾 **Vector Database** - Fast, accurate retrieval with ChromaDB
- 🔄 **Retry Logic** - Robust error handling for GitHub API connections
- 📊 **Progress Tracking** - Real-time updates during repository ingestion

### Advanced Features
- **AST-Based Code Splitting** - Keeps functions and classes intact
- **Import Context Enrichment** - Preserves code dependencies
- **Language-Aware Processing** - Optimized for Python, JavaScript, and more
- **Commit History Integration** - Includes recent commits for temporal context
- **Smart Caching** - Faster subsequent queries with embeddings cache

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd GIT_rag_cahtbot

# Create virtual environment
python -m venv rag_env

# Activate virtual environment
# Windows:
.\rag_env\Scripts\activate
# Linux/Mac:
source rag_env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file in the project root:

```env
# Groq API Key (Get from: https://console.groq.com/keys)
GROQ_API_KEY=your_groq_api_key_here

# GitHub Token (Optional - for private repos and higher rate limits)
GITHUB_TOKEN=your_github_token_here
```

### 3. Run the App

```bash
# Make sure virtual environment is activated
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📖 How to Use

### Step 1: Load a Repository

1. Open the sidebar (click the arrow if collapsed)
2. Enter a GitHub repository in format: `owner/repo` (e.g., `facebook/react`)
3. Click "🚀 Load Repository"
4. Wait for the ingestion process to complete

### Step 2: Ask Questions

Once the repository is loaded, you can ask questions like:

- "How does authentication work?"
- "Show me the main entry point"
- "What API endpoints are available?"
- "How is data validated?"
- "What are the main components?"
- "How does error handling work?"

### Step 3: View Sources

Click "📚 View Sources" under any answer to see:
- Which files were referenced
- Line numbers
- Function/Class names
- Direct links to GitHub

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Streamlit Frontend                       │
│  (app.py - Beautiful UI with chat interface)                │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                    Backend Services                          │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  1. GitHubLoader (services/github_loader.py)                 │
│     - Fetch repository files and commits                     │
│     - Retry logic for connection errors                      │
│     - Rate limit handling                                    │
│                                                              │
│  2. Document Processor (services/document_processor.py)      │
│     - AST-based code splitting                               │
│     - Import context enrichment                              │
│     - Language-aware chunking                                │
│                                                              │
│  3. Embeddings (services/embeddings.py)                      │
│     - Convert text to vectors                                │
│     - Using sentence-transformers/all-MiniLM-L6-v2           │
│                                                              │
│  4. Retrieval (services/retrieval.py)                        │
│     - Semantic similarity search                             │
│     - Context formatting for LLM                             │
│     - Citation extraction                                    │
│                                                              │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                   External Services                          │
├──────────────────────────────────────────────────────────────┤
│  - GitHub API (repository data)                              │
│  - Groq API (LLaMA 3.1 70B for answers)                      │
│  - ChromaDB (vector storage)                                 │
│  - HuggingFace (embeddings model)                            │
└──────────────────────────────────────────────────────────────┘
```

## 🔧 Configuration Options

### Repository Loading

You can customize the loading behavior in `app.py`:

```python
loader = GitHubLoader(
    repo=repo_url,
    branch=branch,
    access_token=os.getenv("GITHUB_TOKEN"),
    file_extensions=(".py", ".js", ".md", ".yaml", ".yml", ".json"),
    max_file_size_bytes=1_048_576,  # 1 MB
    commit_history_limit=30  # Number of recent commits
)
```

### Document Processing

Adjust chunking strategy:

```python
chunks = process_documents(
    documents,
    chunk_size=1000,        # Characters per chunk
    chunk_overlap=200,      # Overlap between chunks
    strategy="hybrid"       # Options: "hybrid", "ast", "language"
)
```

### Retrieval Settings

Modify the number of context chunks:

```python
results = retrieve_context(
    query,
    vectorstore,
    k=5  # Number of relevant chunks to retrieve
)
```

## 📊 Features Deep Dive

### 1. Robust GitHub API Integration

- **Retry Logic**: Automatically retries failed requests 3 times with exponential backoff
- **Rate Limit Handling**: Detects and waits for rate limit resets
- **Connection Error Recovery**: Handles `RemoteDisconnected` and other network issues
- **Progress Tracking**: Real-time updates during file download

### 2. Intelligent Code Splitting

- **AST-Based**: Keeps Python functions and classes whole
- **Import Context**: Preserves dependencies for better understanding
- **Language-Aware**: Optimized splitting for multiple languages
- **Metadata Rich**: Includes file paths, line numbers, function names

### 3. Production-Ready UI

- **Modern Design**: Beautiful gradient backgrounds and smooth animations
- **Responsive**: Works on desktop and mobile
- **Real-time Feedback**: Progress bars and status updates
- **Citation Links**: Direct links to source code on GitHub

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'X'"

Make sure you've activated the virtual environment:

```bash
# Windows
.\rag_env\Scripts\activate

# Linux/Mac
source rag_env/bin/activate

# Then install requirements again
pip install -r requirements.txt
```

### "Connection Error" during repository loading

This is handled automatically with retry logic. If it persists:

1. Check your internet connection
2. Verify your GitHub token is valid
3. Try a smaller repository first
4. Check GitHub API status: https://www.githubstatus.com/

### "Rate Limit Exceeded"

**Without GitHub Token**: 60 requests/hour  
**With GitHub Token**: 5,000 requests/hour

Add your GitHub token to `.env`:
```env
GITHUB_TOKEN=your_token_here
```

### "GROQ_API_KEY not found"

1. Get a free API key from https://console.groq.com/keys
2. Add it to your `.env` file:
   ```env
   GROQ_API_KEY=gsk_your_key_here
   ```
3. Restart the Streamlit app

## 📝 Example Workflows

### Workflow 1: Analyze a New Project

1. Load repository: `facebook/react`
2. Ask: "What is the main entry point?"
3. Ask: "How does component rendering work?"
4. Ask: "Show me error handling patterns"

### Workflow 2: Debug Issues

1. Load your own repository
2. Ask: "Where is authentication implemented?"
3. Ask: "How are API errors handled?"
4. Ask: "Show me database connection logic"

### Workflow 3: Learning a Codebase

1. Load a well-known repository
2. Ask: "What are the main components?"
3. Ask: "How is the project structured?"
4. Ask: "What design patterns are used?"

## 🚧 Roadmap

- [ ] Support for private repositories
- [ ] Multi-repository comparison
- [ ] Code generation capabilities
- [ ] Diagram generation from code
- [ ] Integration with Jira/Linear
- [ ] IDE extensions (VSCode, PyCharm)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - feel free to use this project for your own purposes

## 🙏 Acknowledgments

- **Groq** - For fast LLM inference
- **LangChain** - For RAG pipeline components
- **Streamlit** - For the amazing web framework
- **HuggingFace** - For embeddings models
- **ChromaDB** - For vector storage

## 📧 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Review the [Architecture](#-architecture) to understand the system
3. Open an issue on GitHub

---

**Built with ❤️ using Streamlit, LangChain, and Groq**
