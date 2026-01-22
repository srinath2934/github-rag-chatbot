# 🚀 Quick Start Guide - GitHub RAG Chatbot

## ⚡ 3-Minute Setup

### Step 1: Start the App (30 seconds)

**Option A: Using the Startup Script (Easiest)**
```bash
# Just double-click this file:
start_app.bat
```

**Option B: Manual Start**
```bash
# Activate virtual environment
.\rag_env\Scripts\activate

# Run the app
streamlit run app.py
```

The app will automatically open in your browser at `http://localhost:8501`

### Step 2: Load a Repository (1-2 minutes)

1. **In the sidebar**, enter a repository:
   ```
   Example: srinath2934/execflow-ai
   Or: facebook/react
   Or: pytorch/pytorch
   ```

2. **Click "🚀 Load Repository"**

3. **Wait for the progress bar** - You'll see:
   - 📦 Connecting to GitHub...
   - 📥 Downloading files...
   - ✅ Loaded X documents
   - 🔪 Splitting documents into chunks...
   - 🧠 Generating embeddings...
   - 💾 Building vector database...
   - ✅ Repository loaded successfully!

### Step 3: Start Asking Questions! (Instant)

Try these example questions:

**General Understanding:**
```
- What does this repository do?
- How is the project structured?
- What are the main features?
```

**Technical Deep-Dive:**
```
- How does authentication work?
- Show me the API endpoints
- How is error handling implemented?
- Where is the database connection configured?
```

**Code-Specific:**
```
- What is the main entry point?
- How does the user login function work?
- Show me how data validation is done
- Where is the configuration file?
```

## 💡 Pro Tips

### 1. Better Questions = Better Answers

❌ **Bad**: "show code"  
✅ **Good**: "Show me how user authentication is implemented"

❌ **Bad**: "how work?"  
✅ **Good**: "How does the payment processing workflow work?"

### 2. Use the Citations

Every answer includes **source citations**:
- Click "📚 View Sources" to see which files were used
- Click the GitHub links to view the actual code
- Check line numbers for exact locations

### 3. Follow-up Questions

You can ask follow-up questions:
```
You: "How does authentication work?"
Bot: [Explains authentication...]

You: "Can you show me the login function in detail?"
Bot: [Shows detailed code...]

You: "What happens if the password is wrong?"
Bot: [Explains error handling...]
```

### 4. Repository Best Practices

**Start Small:**
- Test with small repos first (< 100 files)
- Example: `srinath2934/execflow-ai` (good for testing)

**Then Scale Up:**
- Once comfortable, try larger repos
- Example: `facebook/react`, `tensorflow/tensorflow`

**Use GitHub Token:**
- Without token: 60 API calls/hour
- With token: 5,000 API calls/hour
- Add to `.env`: `GITHUB_TOKEN=your_token_here`

## 🎯 Common Use Cases

### Use Case 1: Learning a New Codebase

```
1. Load the repository
2. Ask: "What are the main components?"
3. Ask: "How is the project organized?"
4. Ask: "What design patterns are used?"
5. Browse the citations to understand the structure
```

### Use Case 2: Debugging

```
1. Load your project repository
2. Ask: "Where is [feature X] implemented?"
3. Ask: "How does [component Y] handle errors?"
4. Ask: "Show me the configuration for [service Z]"
```

### Use Case 3: Code Review

```
1. Load the repository
2. Ask: "What security measures are in place?"
3. Ask: "How is input validation done?"
4. Ask: "Are there any potential issues with [specific module]?"
```

### Use Case 4: Onboarding New Team Members

```
1. Load your team's repository
2. Guide them to ask:
   - "What is the development setup process?"
   - "How do I run tests?"
   - "What are the coding conventions?"
   - "Where is the API documentation?"
```

## 🔥 Advanced Features

### Custom Repository Settings

Edit `app.py` to customize loading:

```python
loader = GitHubLoader(
    repo=repo_url,
    branch=branch,
    access_token=os.getenv("GITHUB_TOKEN"),
    file_extensions=(".py", ".js", ".md"),  # Only these files
    max_file_size_bytes=500000,  # 500KB max
    commit_history_limit=20  # Fewer commits = faster
)
```

### Adjusting Answer Quality

More context = Better answers (but slower):

```python
results = retrieve_context(
    query,
    vectorstore,
    k=10  # Retrieve 10 chunks instead of 5
)
```

### Changing the LLM Model

Edit `app.py`:

```python
llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="mixtral-8x7b-32768",  # Faster, less accurate
    # OR
    model_name="llama-3.1-70b-versatile",  # Slower, more accurate
    temperature=0.1,  # Lower = more focused
    max_tokens=4096  # Longer answers
)
```

## 🐛 Troubleshooting

### App Won't Start

```bash
# Make sure you're in the right directory
cd "c:\Users\SRINATH\Desktop\data science\GIT_rag_cahtbot"

# Activate environment
.\rag_env\Scripts\activate

# Check if streamlit is installed
pip list | findstr streamlit

# If not, install it
pip install streamlit

# Run the app
streamlit run app.py
```

### "Repository Loading Failed"

1. **Check your internet connection**
2. **Verify the repository name** (must be `owner/repo`)
3. **Check if the repo is public** (or add your GitHub token for private repos)
4. **Try a different branch** (sometimes `main` doesn't exist, try `master`)

### "GROQ_API_KEY not found"

1. Create a `.env` file in the project root
2. Add: `GROQ_API_KEY=your_key_here`
3. Get a free key from: https://console.groq.com/keys
4. Restart the app

### "Slow Response Times"

**Solutions:**
- Use a smaller repository
- Reduce `k` value in retrieval (fewer chunks)
- Use a faster model (`mixtral-8x7b-32768`)
- Add GitHub token to increase rate limits

## 📊 Performance Metrics

| Repository Size | Load Time | Memory Usage |
|----------------|-----------|--------------|
| Small (<50 files) | 30-60s | ~500MB |
| Medium (50-200 files) | 1-3 min | ~1GB |
| Large (200+ files) | 3-10 min | ~2GB |

| Query Type | Response Time |
|-----------|---------------|
| Simple question | 2-5s |
| Complex question | 5-10s |
| With 10 context chunks | 10-15s |

## 🎓 Example Session

```
👤 You: Load repository "srinath2934/execflow-ai"
🤖 Bot: ✅ Loaded 37 document chunks!

👤 You: What does this repository do?
🤖 Bot: This repository implements ExecFlow AI, an intelligent task 
        execution and workflow automation system. The main components 
        include:
        - Task planning and decomposition (task_planner.py)
        - AI-powered execution (executor.py)
        - Workflow management (workflow_manager.py)
        
        📚 Sources: main.py, README.md, task_planner.py

👤 You: How does the task planner work?
🤖 Bot: The task planner uses a multi-step approach:
        1. Receives high-level task description
        2. Breaks it down into subtasks using LLM
        3. Creates execution plan with dependencies
        4. Assigns priorities and estimates
        
        Key function: `plan_task()` in task_planner.py (lines 45-89)
        
        📚 Sources: task_planner.py, config.yaml

👤 You: Show me the plan_task function
🤖 Bot: [Shows detailed code with explanation...]
```

## ✅ Next Steps

1. **Test with your own repository**
2. **Experiment with different questions**
3. **Customize the settings** for your needs
4. **Share with your team**
5. **Provide feedback** for improvements

---

🎉 **You're all set! Start exploring codebases with AI!** 🚀
