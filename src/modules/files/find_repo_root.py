from typing import Optional
import os

MARKER_FILENAME = "__REPO_ROOT__"

def find_repo_root(start_path: str = '.') -> str:
    curr_dir = os.path.abspath(start_path)
    while True:
        marker_path = os.path.join(curr_dir, MARKER_FILENAME)
        if os.path.isfile(marker_path):
            return curr_dir
        parent_dir = os.path.dirname(curr_dir)
        if curr_dir == parent_dir:
            raise FileNotFoundError(f"Repo root marker '{MARKER_FILENAME}' not found starting from '{start_path}'.")
        curr_dir = parent_dir