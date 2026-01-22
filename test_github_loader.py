"""
Test Script for GitHub Loader Fixes
Tests the connection error fixes with retry logic
"""

import os
import sys
from dotenv import load_dotenv
import logging

# Setup logging to see all the details
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s %(name)s – %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Load environment variables
load_dotenv()

# Import the fixed GitHubLoader
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from services.github_loader import GitHubLoader

def test_github_loader():
    """Test the GitHub loader with the applied fixes"""
    
    print("=" * 80)
    print("TESTING GITHUB LOADER WITH CONNECTION ERROR FIXES")
    print("=" * 80)
    print()
    
    # Get GitHub token
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        print("⚠️ WARNING: GITHUB_TOKEN not found in environment")
        print("   Proceeding without authentication (60 requests/hour limit)")
        print()
    else:
        print("✅ GitHub token found")
        print()
    
    # Test repository
    repo = "srinath2934/execflow-ai"
    branch = "main"
    
    print(f"📦 Repository: {repo}")
    print(f"🌿 Branch: {branch}")
    print()
    
    # Initialize loader
    try:
        loader = GitHubLoader(
            repo=repo,
            branch=branch,
            access_token=github_token,
            commit_history_limit=20,  # Reduce for testing
        )
        print("✅ GitHubLoader initialized successfully")
        print()
    except Exception as e:
        print(f"❌ Failed to initialize GitHubLoader: {e}")
        return False
    
    # Load documents
    print("🚀 Starting document loading...")
    print("   (This may take a minute, watch for retry messages)")
    print()
    
    try:
        documents = loader.load()
        
        print()
        print("=" * 80)
        print("RESULTS")
        print("=" * 80)
        print(f"✅ Successfully loaded {len(documents)} documents")
        print()
        
        # Breakdown by type
        code_docs = [d for d in documents if d.metadata.get('type') == 'code']
        commit_docs = [d for d in documents if d.metadata.get('type') == 'commit']
        placeholder_docs = [d for d in documents if d.metadata.get('type') == 'placeholder']
        
        print("📊 Document Breakdown:")
        print(f"   - Code files: {len(code_docs)}")
        print(f"   - Commits: {len(commit_docs)}")
        print(f"   - Placeholders: {len(placeholder_docs)}")
        print()
        
        # Show sample documents
        if code_docs:
            print("📄 Sample Code Document:")
            sample = code_docs[0]
            print(f"   File: {sample.metadata.get('source')}")
            print(f"   Size: {sample.metadata.get('size')} bytes")
            print(f"   URL: {sample.metadata.get('url')}")
            content_preview = sample.page_content[:200].replace('\n', '\n   ')
            print(f"   Preview: {content_preview}...")
            print()
        
        if commit_docs:
            print("🕒 Sample Commit Document:")
            sample = commit_docs[0]
            print(f"   SHA: {sample.metadata.get('sha')[:8]}...")
            content_preview = sample.page_content[:200].replace('\n', '\n   ')
            print(f"   Preview: {content_preview}")
            print()
        
        print("=" * 80)
        print("TEST PASSED ✅")
        print("=" * 80)
        return True
        
    except Exception as e:
        print()
        print("=" * 80)
        print("TEST FAILED ❌")
        print("=" * 80)
        print(f"Error: {type(e).__name__}: {e}")
        print()
        
        import traceback
        print("Full traceback:")
        print(traceback.format_exc())
        
        return False

if __name__ == "__main__":
    success = test_github_loader()
    sys.exit(0 if success else 1)
