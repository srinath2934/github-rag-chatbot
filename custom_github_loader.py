"""
GitHub RAG Loader - Clean implementation that works around LangChain bugs
"""

import os
import requests
import base64
from typing import List, Tuple
from langchain.schema import Document
from dotenv import load_dotenv


class GitHubRepoLoader:
    """
    A custom GitHub repository loader that works correctly with the GitHub API.
    This replaces the buggy langchain_community.document_loaders.GithubFileLoader.
    """
    
    def __init__(
        self,
        repo: str,  # Format: "owner/repo"
        branch: str = "main",
        access_token: str = None,
        file_extensions: Tuple[str, ...] = (".py", ".md", ".js", ".txt")
    ):
        """
        Initialize the GitHub loader.
        
        Args:
            repo: Repository in format "owner/repo" (e.g., "srinath2934/execflow-ai")
            branch: Branch name (default: "main")
            access_token: GitHub personal access token (optional for public repos)
            file_extensions: Tuple of file extensions to include
        """
        self.repo = repo
        self.branch = branch
        self.access_token = access_token
        self.file_extensions = file_extensions
        self.headers = {}
        
        if access_token:
            self.headers["Authorization"] = f"token {access_token}"
    
    def load(self) -> List[Document]:
        """
        Load all files from the repository that match the file extensions.
        
        Returns:
            List of LangChain Document objects
        """
        # Step 1: Get the repository tree
        tree_url = f"https://api.github.com/repos/{self.repo}/git/trees/{self.branch}?recursive=1"
        print(f"🔍 Fetching repository tree from GitHub...")
        
        try:
            response = requests.get(tree_url, headers=self.headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f"❌ Error: {e}")
            print(f"📍 URL: {tree_url}")
            print(f"💡 Tip: Check if the repository exists and the branch name is correct")
            raise
        
        tree_data = response.json()
        all_files = tree_data.get("tree", [])
        
        # Step 2: Filter files by extension
        filtered_files = [
            f for f in all_files 
            if f["type"] == "blob" and any(f["path"].endswith(ext) for ext in self.file_extensions)
        ]
        
        print(f"📁 Found {len(filtered_files)} files matching extensions: {self.file_extensions}")
        
        # Step 3: Load each file's content
        documents = []
        
        for i, file_info in enumerate(filtered_files, 1):
            file_path = file_info["path"]
            print(f"  [{i}/{len(filtered_files)}] Loading: {file_path}")
            
            try:
                # Get file content via GitHub API
                content_url = f"https://api.github.com/repos/{self.repo}/contents/{file_path}?ref={self.branch}"
                content_response = requests.get(content_url, headers=self.headers)
                content_response.raise_for_status()
                
                content_data = content_response.json()
                
                # Decode base64 content
                content = base64.b64decode(content_data["content"]).decode("utf-8")
                
                # Create LangChain Document
                doc = Document(
                    page_content=content,
                    metadata={
                        "source": file_path,
                        "repo": self.repo,
                        "branch": self.branch,
                        "sha": file_info["sha"],
                        "url": content_data.get("html_url", ""),
                        "size": file_info.get("size", 0)
                    }
                )
                documents.append(doc)
                
            except Exception as e:
                print(f"    ⚠️  Failed to load {file_path}: {e}")
                continue
        
        print(f"\n✅ Successfully loaded {len(documents)} documents from {self.repo}")
        return documents


# Example usage
if __name__ == "__main__":
    load_dotenv()
    
    # Load your GitHub repo
    loader = GitHubRepoLoader(
        repo="srinath2934/execflow-ai",
        branch="main",
        access_token=os.getenv("GITHUB_TOKEN"),  # Optional for public repos
        file_extensions=(".py", ".md", ".js")
    )
    
    docs = loader.load()
    
    # Show results
    if docs:
        print(f"\n{'='*60}")
        print(f"📄 Sample Document:")
        print(f"{'='*60}")
        print(f"Source: {docs[0].metadata['source']}")
        print(f"URL: {docs[0].metadata['url']}")
        print(f"Size: {docs[0].metadata['size']} bytes")
        print(f"\nContent (first 300 chars):")
        print(docs[0].page_content[:300] + "...")
