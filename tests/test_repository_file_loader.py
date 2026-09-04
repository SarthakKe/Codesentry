from pathlib import Path

import pytest

from scanner.repository_file_loader import RepositoryFileLoader


def write_file(path: Path, content: str = "content") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_discover_recursively_returns_file_metadata(tmp_path: Path) -> None:
    write_file(tmp_path / "app.py", "print('hello')")
    write_file(tmp_path / "src" / "client.ts", "export {}")

    files = RepositoryFileLoader().discover(tmp_path)

    assert [file.relative_path.as_posix() for file in files] == ["app.py", "src/client.ts"]
    assert files[0].absolute_path == tmp_path / "app.py"
    assert files[0].extension == ".py"
    assert files[0].size_bytes == len("print('hello')".encode("utf-8"))


def test_discover_only_returns_supported_extensions(tmp_path: Path) -> None:
    supported_names = [
        "a.py", "b.js", "c.ts", "d.java", "e.php", "f.json", "g.yml", "h.yaml", ".env"
    ]
    for name in supported_names:
        write_file(tmp_path / name)
    write_file(tmp_path / "notes.txt")
    write_file(tmp_path / ".env.local")

    files = RepositoryFileLoader().discover(tmp_path)

    assert {file.relative_path.name for file in files} == set(supported_names)
    assert next(file.extension for file in files if file.relative_path.name == ".env") == ".env"


def test_discover_ignores_configured_directories(tmp_path: Path) -> None:
    ignored_directories = [".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build"]
    for directory in ignored_directories:
        write_file(tmp_path / directory / "ignored.py")
    write_file(tmp_path / "nested" / "node_modules" / "ignored.ts")
    write_file(tmp_path / "src" / "included.py")

    files = RepositoryFileLoader().discover(tmp_path)

    assert [file.relative_path.as_posix() for file in files] == ["src/included.py"]


def test_discover_rejects_nonexistent_repository_path(tmp_path: Path) -> None:
    missing_path = tmp_path / "missing-repository"

    with pytest.raises(FileNotFoundError, match="does not exist"):
        RepositoryFileLoader().discover(missing_path)
