import os

# Utility functions
def ensure_directory_exists(directory: str):
    """Ensure a directory exists, and create it if it doesn't."""
    os.makedirs(directory, exist_ok=True)
