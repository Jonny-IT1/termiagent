import pytest
from pathlib import Path
from termiagent.tools.filesystem import (
    view_file, write_file, edit_file, list_directory, search_codebase
)
from termiagent.tools.shell import run_shell_command

def test_write_and_view_file(tmp_path):
    f_path = tmp_path / "hello.py"
    write_res = write_file(str(f_path), "print('hello world')", overwrite=True)
    assert "Successfully wrote" in write_res

    view_res = view_file(str(f_path))
    assert "print('hello world')" in view_res
    assert "Lines 1-1" in view_res

def test_edit_file(tmp_path):
    f_path = tmp_path / "calc.py"
    write_file(str(f_path), "def add(a, b):\n    return a - b\n")

    edit_res = edit_file(str(f_path), "return a - b", "return a + b")
    assert "Successfully replaced" in edit_res

    content = f_path.read_text(encoding="utf-8")
    assert "return a + b" in content

def test_list_directory(tmp_path):
    (tmp_path / "main.py").write_text("x = 1")
    (tmp_path / "docs").mkdir()

    list_res = list_directory(str(tmp_path))
    assert "main.py" in list_res
    assert "docs" in list_res

def test_search_codebase(tmp_path):
    (tmp_path / "app.py").write_text("SECRET_KEY = '12345'\n")
    search_res = search_codebase("SECRET_KEY", str(tmp_path))
    assert "app.py:1: SECRET_KEY = '12345'" in search_res

def test_run_shell_command(tmp_path):
    cmd_res = run_shell_command("echo hello_termiagent", cwd=str(tmp_path))
    assert "hello_termiagent" in cmd_res
    assert "Exit Code: 0" in cmd_res
