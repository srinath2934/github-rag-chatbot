import os
import requests
from typing import List
from langchain.schema import Document
from dotenv import load_dotenv

load_dotenv()

def load_github_files(
    repo: str,  # Format: "owner/repo"
    branch: str = "main",
    access_token: str = None,
    file_extensions: tuple = (".py", ".md", ".js")
) -> List[Document]:
    """
    Load files from a GitHub repository.
    
    Args:
        repo: Repository in format "owner/repo"
        branch: Branch name (default: "main")
        access_token: GitHub personal access token (optional for public repos)
        file_extensions: Tuple of file extensions to include
    
    Returns:
        List of Document objects
    """
    headers = {}
    if access_token:
        headers["Authorization"] = f"token {access_token}"
    
    # Get the tree
    tree_url = f"https://api.github.com/repos/{repo}/git/trees/{branch}?recursive=1"
    print(f"📡 Fetching repository tree from: {tree_url}")
    
    response = requests.get(tree_url, headers=headers)
    response.raise_for_status()
    
    tree_data = response.json()
    files = tree_data.get("tree", [])
    
    # Filter files by extension
    filtered_files = [
        f for f in files 
        if f["type"] == "blob" and any(f["path"].endswith(ext) for ext in file_extensions)
    ]
    
    print(f"📁 Found {len(filtered_files)} files matching {file_extensions}")
    
    documents = []
    
    for file_info in filtered_files:
        file_path = file_info["path"]
        print(f"  ↳ Loading: {file_path}")
        
        # Get file content
        content_url = f"https://api.github.com/repos/{repo}/contents/{file_path}?ref={branch}"
        content_response = requests.get(content_url, headers=headers)
        content_response.raise_for_status()
        
        content_data = content_response.json()
        
        # Decode content (it's base64 encoded)
        import base64
        content = base64.b64decode(content_data["content"]).decode("utf-8")
        
        # Create document
        doc = Document(
            page_content=content,
            metadata={
                "source": file_path,
                "repo": repo,
                "branch": branch,
                "sha": file_info["sha"],
                "url": content_data.get("html_url", ""),
            }
        )
        documents.append(doc)
    
    return documents


if __name__ == "__main__":
    # Test the loader
    github_token = os.getenv("GITHUB_TOKEN")
    
    docs = load_github_files(
        repo="srinath2934/execflow-ai",
        branch="main",
        access_token=github_token,
        file_extensions=(".py", ".md", ".js")
    )
    
    print(f"\n✅ Successfully loaded {len(docs)} documents")
    
    if docs:
        print(f"\n📄 First document:")
        print(f"  - Source: {docs[0].metadata['source']}")
        print(f"  - URL: {docs[0].metadata['url']}")
        print(f"  - Content preview: {docs[0].page_content[:200]}...")
