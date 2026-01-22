# GitHub RAG Loader - 404 Error Fix

## 🐛 The Problem

You're experiencing a **404 Not Found** error when using LangChain's `GithubFileLoader`:

```
HTTPError: 404 Client Error: Not Found for url: 
https://api.github.com/api/v3/repos/srinath2934/execflow-ai/git/trees/main?recursive=1
```

### Root Cause

The `GithubFileLoader` from `langchain_community` has a bug where it constructs incorrect GitHub API URLs by adding `/api/v3/` twice in the path:

- **Incorrect URL**: `https://api.github.com/api/v3/repos/.../git/trees/main`
- **Correct URL**: `https://api.github.com/repos/.../git/trees/main`

The library appends `/api/v3/` to the `github_api_url` parameter, but `https://api.github.com` should not have this suffix added.

## ✅ The Solution

I've created a custom `GitHubRepoLoader` class that correctly uses the GitHub API. This class:

1. ✅ Properly constructs GitHub API URLs
2. ✅ Handles authentication with GitHub tokens
3. ✅ Filters files by extension
4. ✅ Returns LangChain `Document` objects
5. ✅ Provides detailed progress tracking
6. ✅ Includes error handling

## 📁 Files Created

1. **`custom_github_loader.py`** - Standalone Python module with the custom loader
2. **`test_github_loader.ipynb`** - Complete Jupyter notebook with:
   - The custom loader implementation
   - Example usage
   - Full RAG pipeline setup
   - Test queries

## 🚀 How to Use

### Option 1: Use the Jupyter Notebook

Open `test_github_loader.ipynb` and run all cells. It includes:
- Custom GitHub loader
- Vector store creation with FAISS
- RAG chain setup
- Example queries

### Option 2: Import the Custom Loader

```python
from custom_github_loader import GitHubRepoLoader
import os
from dotenv import load_dotenv

load_dotenv()

# Create loader
loader = GitHubRepoLoader(
    repo="srinath2934/execflow-ai",  # ✅ Format: owner/repo
    branch="main",
    access_token=os.getenv("GITHUB_TOKEN"),  # Optional for public repos
    file_extensions=(".py", ".md", ".js")
)

# Load documents
docs = loader.load()
print(f"Loaded {len(docs)} documents")
```

## 🔑 Key Differences from LangChain's Loader

| Feature | LangChain GithubFileLoader | Custom GitHubRepoLoader |
|---------|---------------------------|------------------------|
| URL Construction | ❌ Buggy (adds /api/v3/ twice) | ✅ Correct |
| Error Messages | ❌ Unclear | ✅ Detailed |
| Progress Tracking | ❌ None | ✅ Yes |
| Repo Format | `owner/repo` or full URL | `owner/repo` only |
| Timeout Handling | ❌ No | ✅ Yes (30s default) |

## 📝 Configuration

### Required Environment Variables

Create a `.env` file with:

```env
GITHUB_TOKEN=your_github_personal_access_token  # Optional for public repos
GROQ_API_KEY=your_groq_api_key  # For the LLM
```

### GitHub Token Permissions

For public repositories, no token is needed. For private repositories or to avoid rate limits:

1. Go to GitHub Settings → Developer Settings → Personal Access Tokens
2. Generate a new token with `repo` scope
3. Add it to your `.env` file

## 🛠️ Technical Details

The custom loader works by:

1. **Fetching the repository tree** via GitHub's Git Trees API
   ```
   GET /repos/{owner}/{repo}/git/trees/{branch}?recursive=1
   ```

2. **Filtering files** by extension from the tree

3. **Fetching file contents** via GitHub's Contents API
   ```
   GET /repos/{owner}/{repo}/contents/{path}?ref={branch}
   ```

4. **Decoding Base64** content returned by the API

5. **Creating LangChain Documents** with proper metadata

## 🎯 Next Steps

After loading documents, you can:

1. **Create embeddings** using HuggingFace or OpenAI
2. **Store in vector database** (FAISS, Pinecone, ChromaDB, etc.)
3. **Build RAG pipeline** for Q&A
4. **Integrate with your chatbot** application

The `test_github_loader.ipynb` notebook includes a complete example of all these steps.

## 🐞 Troubleshooting

### Still getting 404?
- ✅ Verify the repository exists: `https://github.com/srinath2934/execflow-ai`
- ✅ Check the branch name (usually `main` or `master`)
- ✅ Ensure repo format is `owner/repo`, not the full URL

### Rate limiting?
- Add a GitHub token to your `.env` file
- Authenticated requests have a much higher rate limit (5000/hour vs 60/hour)

### Connection errors?
- Check your internet connection
- Try adding a longer timeout: `requests.get(..., timeout=60)`
- GitHub might be experiencing issues

## 📚 Resources

- [GitHub REST API Documentation](https://docs.github.com/en/rest)
- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)
- [FAISS Documentation](https://github.com/facebookresearch/faiss)
