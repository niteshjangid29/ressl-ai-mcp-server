# server.py
from mcp.server.fastmcp import FastMCP
from pathlib import Path
import re
from typing import Any, Dict, List

# Create an MCP server
mcp = FastMCP("keyword-search-server")

# Restrict file access to this directory for safety
BASE_DIR = Path(__file__).parent.resolve() / "my_files"
BASE_DIR.mkdir(exist_ok=True)

def _resolve_and_check(filename: str) -> Path:
    target_file = (BASE_DIR / filename).resolve()
    try:
        # Ensure the target is inside BASE_DIR
        if BASE_DIR not in target_file.parents and target_file != BASE_DIR:
            raise ValueError("Access denied: file must be inside the server sample_files directory.")
    except Exception:
        raise
    return target_file

@mcp.tool()
def search_in_file(
    filename: str,
    keyword: str,
    case_insensitive: bool = False,
    context_lines: int = 0,
    use_regex: bool = False
) -> Dict[str, Any]:
    """
    Search for `keyword` inside a file located in ./sample_files.
    Returns JSON with matches including line numbers and optional surrounding context.

    Inputs:
      - filename: name of file inside sample_files (e.g., "example.txt")
      - keyword: substring to search for (or regex if use_regex=True)
      - case_insensitive: if True, do case-insensitive matching
      - context_lines: number of surrounding lines to include for each match
      - use_regex: treat `keyword` as a regular expression
    """
    try:
        target_file = _resolve_and_check(filename)
    except Exception as e:
        return {"ok": False, "error": str(e)}
    
    if not target_file.is_file():
        return {"ok": False, "error": f"File not found: {filename}"}
    
    flags = re.MULTILINE
    if case_insensitive:
        flags |= re.IGNORECASE

    pattern = keyword if use_regex else re.escape(keyword)
    compiled = re.compile(pattern, flags)

    lines = target_file.read_text(encoding="utf-8", errors="ignore").splitlines()

    matches: List[Dict[str, Any]] = []

    for line_num, line in enumerate(lines, start=1):
        if compiled.search(line):
            start = max(line_num - context_lines, 1)
            end = line_num + context_lines
            context = [
                {"line_number": i, "line": lines[i - 1].strip()}
                for i in range(start, end + 1) 
            ]
            matches.append({"line_number": line_num, "line": line.strip(), "context": context})

    return {
        "ok": True,
        "filename": filename,
        "keyword": keyword,
        "count": len(matches),
        "matches": matches,
    }

if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8000)