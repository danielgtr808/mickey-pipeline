from pathlib import Path
from .find_repo_root import find_repo_root

from typing import Optional

def find_relative_file(relative_path: Path, base_directory: Optional[Path] = None, if_file_doesnt_exist_throws: bool = True) -> Path:
    file_path: Path
    if (base_directory is None):
        file_path = find_repo_root()
    else:
        file_path = base_directory

    file_path = file_path / relative_path
    
    if if_file_doesnt_exist_throws and not file_path.exists():
        raise FileNotFoundError(f"{file_path} does not exist.")
    return file_path