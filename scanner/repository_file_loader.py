"""Discovery of scanable files within a local source repository."""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path


SUPPORTED_EXTENSIONS = frozenset(
    {".py", ".js", ".ts", ".java", ".php", ".json", ".yml", ".yaml", ".env"}
)
IGNORED_DIRECTORY_NAMES = frozenset(
    {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build"}
)


@dataclass(frozen=True, slots=True)
class RepositoryFile:
    """Metadata about a file selected for a future security scan."""

    absolute_path: Path
    relative_path: Path
    extension: str
    size_bytes: int


class RepositoryFileLoader:
    """Find supported files in a local repository while pruning generated content."""

    def __init__(
        self,
        supported_extensions: frozenset[str] = SUPPORTED_EXTENSIONS,
        ignored_directory_names: frozenset[str] = IGNORED_DIRECTORY_NAMES,
    ) -> None:
        self._supported_extensions = supported_extensions
        self._ignored_directory_names = ignored_directory_names

    def discover(self, repository_path: str | Path) -> list[RepositoryFile]:
        """Return supported regular files below *repository_path*, ordered by path.

        Raises:
            FileNotFoundError: If the supplied path does not exist.
            NotADirectoryError: If the supplied path is not a directory.
        """
        root = Path(repository_path).expanduser().resolve()
        if not root.exists():
            raise FileNotFoundError(f"Repository path does not exist: {root}")
        if not root.is_dir():
            raise NotADirectoryError(f"Repository path is not a directory: {root}")

        discovered_files: list[RepositoryFile] = []
        for current_directory, directories, file_names in os.walk(root, topdown=True):
            directories[:] = sorted(
                directory
                for directory in directories
                if directory not in self._ignored_directory_names
            )
            current_path = Path(current_directory)

            for file_name in sorted(file_names):
                path = current_path / file_name
                if not self._is_supported(path):
                    continue

                discovered_files.append(
                    RepositoryFile(
                        absolute_path=path,
                        relative_path=path.relative_to(root),
                        extension=self._extension_for(path),
                        size_bytes=path.stat().st_size,
                    )
                )

        return sorted(discovered_files, key=lambda file: file.relative_path.as_posix())

    def _is_supported(self, path: Path) -> bool:
        return self._extension_for(path) in self._supported_extensions

    @staticmethod
    def _extension_for(path: Path) -> str:
        return ".env" if path.name == ".env" else path.suffix.lower()
