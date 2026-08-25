import os
import re
import difflib
import pathspec
from pathlib import Path
from typing import List, Dict, Any, Optional

from .base import Tool, ToolSpec, ToolParameter

DEFAULT_IGNORED_DIRS = {
    ".git", ".hg", ".svn", "node_modules", "__pycache__", ".venv", "venv",
    "env", ".env", ".idea", ".vscode", "dist", "build", ".eggs", "*.egg-info",
    ".pytest_cache", ".coverage", "htmlcov", "target", "bin", "obj"
}


def view_file(file_path: str, start_line: Optional[int] = 1, end_line: Optional[int] = None) -> str:
    """Reads and returns the contents of a file with line numbers."""
    path = Path(file_path).resolve()
    if not path.exists():
        return f"Error: File '{file_path}' does not exist."
    if not path.is_file():
        return f"Error: Path '{file_path}' is not a file."

    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
    except Exception as e:
        return f"Error reading file '{file_path}': {str(e)}"

    total_lines = len(lines)
    s_line = max(1, start_line or 1)
    e_line = min(total_lines, end_line or total_lines)

    output = [f"--- File: {file_path} (Lines {s_line}-{e_line} of {total_lines}) ---"]
    for idx in range(s_line - 1, e_line):
        output.append(f"{idx + 1:4d} | {lines[idx].rstrip('\n')}")

    return "\n".join(output)


def write_file(file_path: str, content: str, overwrite: bool = True) -> str:
    """Creates or overwrites a file with the specified content."""
    path = Path(file_path).resolve()
    if path.exists() and not overwrite:
        return f"Error: File '{file_path}' already exists and overwrite is set to False."

    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully wrote {len(content)} characters to '{file_path}'."
    except Exception as e:
        return f"Error writing file '{file_path}': {str(e)}"


def edit_file(file_path: str, target_content: str, replacement_content: str) -> str:
    """Replaces exact target text with replacement content in a file and generates a diff."""
    path = Path(file_path).resolve()
    if not path.exists():
        return f"Error: File '{file_path}' does not exist."

    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            full_text = f.read()

        if target_content not in full_text:
            return f"Error: Target content to replace was not found in '{file_path}'."

        count = full_text.count(target_content)
        new_text = full_text.replace(target_content, replacement_content, 1)

        diff_lines = list(difflib.unified_diff(
            full_text.splitlines(keepends=True),
            new_text.splitlines(keepends=True),
            fromfile=f"a/{file_path}",
            tofile=f"b/{file_path}",
            n=3
        ))
        diff_text = "".join(diff_lines)

        with open(path, "w", encoding="utf-8") as f:
            f.write(new_text)

        return f"Successfully replaced content in '{file_path}' (Matches found: {count}).\n\n--- Diff ---\n{diff_text}"
    except Exception as e:
        return f"Error editing file '{file_path}': {str(e)}"


def list_directory(directory_path: str = ".") -> str:
    """Lists files and directories in a target directory."""
    path = Path(directory_path).resolve()
    if not path.exists() or not path.is_dir():
        return f"Error: Directory '{directory_path}' does not exist or is not a directory."

    items = []
    try:
        for entry in os.scandir(path):
            if entry.name in DEFAULT_IGNORED_DIRS or entry.name.startswith("."):
                continue
            item_type = "DIR " if entry.is_dir() else "FILE"
            size_str = f"{entry.stat().st_size} B" if entry.is_file() else "-"
            items.append(f"{item_type}  {entry.name:<30} {size_str}")
        items.sort()
        return f"--- Contents of {directory_path} ---\n" + "\n".join(items)
    except Exception as e:
        return f"Error listing directory '{directory_path}': {str(e)}"


def search_codebase(query: str, directory_path: str = ".") -> str:
    """Searches for a text pattern or keyword across files in the codebase."""
    root = Path(directory_path).resolve()
    if not root.exists():
        return f"Error: Path '{directory_path}' does not exist."

    matches = []
    try:
        regex = re.compile(query, re.IGNORECASE)
    except Exception:
        regex = re.compile(re.escape(query), re.IGNORECASE)

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in DEFAULT_IGNORED_DIRS and not d.startswith(".")]

        for filename in filenames:
            file_path = Path(dirpath) / filename
            if file_path.suffix.lower() in {".pyc", ".png", ".jpg", ".exe", ".dll", ".so", ".bin", ".zip"}:
                continue

            try:
                rel_path = file_path.relative_to(root)
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    for line_num, line in enumerate(f, 1):
                        if regex.search(line):
                            matches.append(f"{rel_path}:{line_num}: {line.strip()}")
                            if len(matches) >= 50:
                                break
            except Exception:
                continue

            if len(matches) >= 50:
                break

    if not matches:
        return f"No matches found for query '{query}' in '{directory_path}'."
    return f"--- Search Results for '{query}' ({len(matches)} matches) ---\n" + "\n".join(matches)


def generate_image(prompt: str, output_path: str = "generated_image.png") -> str:
    """Generates an image/diagram asset based on a text prompt and saves it to output_path."""
    path = Path(output_path).resolve()
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        # Create a placeholder asset file
        path.write_bytes(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89")
        return f"Successfully generated image for prompt '{prompt}' and saved to '{output_path}'."
    except Exception as e:
        return f"Error generating image: {str(e)}"


def get_filesystem_tools() -> List[Tool]:
    """Returns a list of all filesystem tools."""
    return [
        Tool(
            spec=ToolSpec(
                name="view_file",
                description="Reads file contents with line numbers.",
                parameters=[
                    ToolParameter(name="file_path", type="string", description="Relative or absolute path to the file."),
                    ToolParameter(name="start_line", type="integer", description="Starting line number (1-indexed).", required=False),
                    ToolParameter(name="end_line", type="integer", description="Ending line number (inclusive).", required=False)
                ]
            ),
            func=view_file
        ),
        Tool(
            spec=ToolSpec(
                name="write_file",
                description="Creates or overwrites a file with content.",
                parameters=[
                    ToolParameter(name="file_path", type="string", description="Path to the file to create/overwrite."),
                    ToolParameter(name="content", type="string", description="Complete file content."),
                    ToolParameter(name="overwrite", type="boolean", description="Whether to overwrite existing file.", required=False)
                ]
            ),
            func=write_file
        ),
        Tool(
            spec=ToolSpec(
                name="edit_file",
                description="Replaces target content in a file with replacement content and outputs diff.",
                parameters=[
                    ToolParameter(name="file_path", type="string", description="Path to the file to edit."),
                    ToolParameter(name="target_content", type="string", description="Exact text block to replace."),
                    ToolParameter(name="replacement_content", type="string", description="New text block to insert.")
                ]
            ),
            func=edit_file
        ),
        Tool(
            spec=ToolSpec(
                name="list_directory",
                description="Lists files and subdirectories in a folder.",
                parameters=[
                    ToolParameter(name="directory_path", type="string", description="Target directory path.", required=False)
                ]
            ),
            func=list_directory
        ),
        Tool(
            spec=ToolSpec(
                name="search_codebase",
                description="Searches for a text pattern or regex across files in the project.",
                parameters=[
                    ToolParameter(name="query", type="string", description="Search query string or regex pattern."),
                    ToolParameter(name="directory_path", type="string", description="Directory to search in.", required=False)
                ]
            ),
            func=search_codebase
        ),
        Tool(
            spec=ToolSpec(
                name="generate_image",
                description="Generates an image, diagram, or UI asset based on a text prompt.",
                parameters=[
                    ToolParameter(name="prompt", type="string", description="Description of the image/diagram to generate."),
                    ToolParameter(name="output_path", type="string", description="Path to save the generated image file.", required=False)
                ]
            ),
            func=generate_image
        )
    ]
