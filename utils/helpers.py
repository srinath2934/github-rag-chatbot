"""
Helper utility functions for the RAG chatbot
"""
import os
import hashlib
from typing import List, Dict
import streamlit as st


def create_directory(path: str) -> None:
    """Create directory if it doesn't exist"""
    if not os.path.exists(path):
        os.makedirs(path)
        

def generate_repo_hash(repo_url: str) -> str:
    """Generate a unique hash for a repository URL"""
    return hashlib.md5(repo_url.encode()).hexdigest()[:8]


def format_source_reference(source: Dict) -> str:
    """Format source reference for display"""
    file_name = source.get('file', 'Unknown')
    line_num = source.get('line', 'N/A')
    return f"📄 `{file_name}` (Line {line_num})"


def count_tokens(text: str) -> int:
    """Rough token count estimation"""
    return len(text.split())


def truncate_text(text: str, max_length: int = 200) -> str:
    """Truncate text to max length with ellipsis"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."


@st.cache_data
def get_file_extension_filter() -> List[str]:
    """Get list of supported file extensions for code files"""
    return [
        '.py', '.js', '.jsx', '.ts', '.tsx',
        '.java', '.cpp', '.c', '.h', '.hpp',
        '.go', '.rs', '.rb', '.php', '.cs',
        '.swift', '.kt', '.scala', '.r',
        '.md', '.txt', '.json', '.yaml', '.yml',
        '.html', '.css', '.scss', '.sql'
    ]


def is_valid_code_file(file_path: str) -> bool:
    """Check if file is a valid code file"""
    extensions = get_file_extension_filter()
    return any(file_path.endswith(ext) for ext in extensions)


def format_chat_history(messages: List[Dict]) -> str:
    """Format chat history for context"""
    formatted = []
    for msg in messages:
        role = msg.get('role', 'user')
        content = msg.get('content', '')
        formatted.append(f"{role.upper()}: {content}")
    return "\n".join(formatted)
