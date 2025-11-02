# 🔍 MCP Keyword Search Server (Python)

This project implements a Model Context Protocol (MCP) server in Python using FastMCP. It exposes a tool called `search_in_file` that lets you search for a keyword or regular expression inside text files.

You can run this server locally and connect it to the MCP Inspector for testing and visualization.

## 🚀 Features

- 🔎 Search within text files stored in the `my_files/` directory.
- 🧩 Supports:
    - Case-insensitive search
    - Regex-based matching
    - Optional surrounding context lines
- 🔒 Safe — file access is restricted to the `my_files` directory only.
- 🌐 Runs as an HTTP MCP server for easy integration with the MCP Inspector.

## 🧱 Project Structure

```
mcp-keyword-search/
├── server.py
├── my_files/
│   └── stock.txt
└── README.md
```

## ⚙️ Prerequisites

- Python 3.9+
- `pip` installed
- Node.js (for MCP Inspector testing)

## 🧩 Setup & Run Instructions

1.  **Clone the repository**
    ```bash
    git clone https://github.com/niteshjangid29/ressl-ai-mcp-server.git
    cd ressl-ai-mcp-server
    ```

2.  **Create and activate a virtual environment**
    ```bash
    python -m venv .venv
    source .venv/bin/activate   
    ```

3.  **Install dependencies**
    ```bash
    uv add "mcp[cli]"
    ```

4.  **Run the MCP Server**

    To run the server with MCP Inspector, use the following command:
    
    ```bash
    mcp dev server.py
    ```

    The server will start, and you can access the MCP Inspector in your browser to interact with the `search_in_file` tool.


## Example Input/Output
### Example Request

```json
{
  "filename": "stock.txt",
  "keyword": "stock",
  "case_insensitive": false,
  "context_lines": 0,
  "use_regex": false
}
```

### Example Response

```json
{
  "result": {
    "ok": true,
    "filename": "stock.txt",
    "keyword": "stock",
    "count": 3,
    "matches": [
      {
        "line_number": 1,
        "line": "The stock market opened higher today as tech shares gained momentum.",
        "context": [
          {
            "line_number": 1,
            "line": "The stock market opened higher today as tech shares gained momentum."
          }
        ]
      },
      {
        "line_number": 5,
        "line": "The Nifty index showed a bullish trend driven by IT and energy stocks.",
        "context": [
          {
            "line_number": 5,
            "line": "The Nifty index showed a bullish trend driven by IT and energy stocks."
          }
        ]
      },
      {
        "line_number": 8,
        "line": "Analysts recommend buying dips in quality large-cap stocks.",
        "context": [
          {
            "line_number": 8,
            "line": "Analysts recommend buying dips in quality large-cap stocks."
          }
        ]
      }
    ]
  }
}
```
