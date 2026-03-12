<p align="center">
  <img src="https://cdn.worldvectorlogo.com/logos/figma-icon.svg" alt="Figma" width="60" height="60" />
  &nbsp;&nbsp;&nbsp;
  <img src="https://mintlify.s3.us-west-1.amazonaws.com/mcp/logo/light.svg" alt="MCP" width="60" height="60" />
</p>

<h1 align="center">figma-mcp</h1>

<p align="center">
  <strong>An MCP server that lets AI agents interact with Figma designs</strong>
</p>

<p align="center">
  <a href="#installation">Installation</a> •
  <a href="#tools">Tools</a> •
  <a href="#use-cases">Use Cases</a> •
  <a href="#configuration">Configuration</a>
</p>

---

## What is this?

**figma-mcp** is a [Model Context Protocol](https://modelcontextprotocol.io/) server that gives LLM agents (Claude, GPT, etc.) the ability to read, inspect, and export from Figma files programmatically.

Built with the official [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) using the `FastMCP` API.

## Architecture

```
┌─────────────────────┐
│  Claude Desktop /   │
│  Any MCP Client     │
└────────┬────────────┘
         │ stdio
┌────────▼────────────┐
│  figma-mcp Server   │
│  (FastMCP)          │
└────────┬────────────┘
         │ HTTPS
┌────────▼────────────┐
│  Figma REST API     │
│  api.figma.com/v1   │
└─────────────────────┘
```

**Project structure:**

```
src/figma_mcp/
  __init__.py        # Entry point
  config.py          # Environment config (dotenv)
  utils.py           # Logger (stderr) + validation helpers
  figma_client.py    # Figma API client (requests)
  server.py          # FastMCP server + all tool definitions
```

## Installation

```bash
git clone https://github.com/Anakintano/figma-mcp.git
cd figma-mcp
pip install -e .
```

Or with **uv** (recommended):

```bash
uv pip install -e .
```

## Configuration

### 1. Get a Figma Token

1. Go to [Figma Settings → Account → Personal access tokens](https://www.figma.com/developers/api#access-tokens)
2. Click **Generate new token**
3. Copy the token

### 2. Set Environment Variable

Create a `.env` file in the project root:

```
FIGMA_ACCESS_TOKEN=figd_your_token_here
```

### 3. Claude Desktop Setup

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "figma": {
      "command": "python",
      "args": ["-m", "figma_mcp"],
      "cwd": "/path/to/figma-mcp",
      "env": {
        "FIGMA_ACCESS_TOKEN": "figd_your_token_here"
      }
    }
  }
}
```

## Tools

| Tool | Description | Key Params |
|------|-------------|------------|
| `get_figma_file` | Get a complete Figma file | `file_key` |
| `get_frame_nodes` | Get specific nodes/frames | `file_key`, `node_ids` |
| `list_components` | List all components | `file_key` |
| `list_styles` | List all styles | `file_key` |
| `export_assets` | Export as PNG/JPG/SVG/PDF | `file_key`, `node_ids`, `format`, `scale` |

> **Finding your file key:** In any Figma URL like `https://www.figma.com/file/ABC123xyz/My-Design`, the file key is `ABC123xyz`.

## Use Cases

### 1. Design System Audit

> **Prompt:** _"List all components in my Figma file `abc123` and tell me which ones don't follow our naming convention"_

The agent uses `list_components` to fetch every component, then analyzes naming patterns — great for enforcing consistency across large design systems.

### 2. Developer Handoff

> **Prompt:** _"Get the layout details of the login page frame `1:42` from file `xyz789`"_

Uses `get_frame_nodes` to extract exact positions, sizes, colors, fonts, and spacing — giving developers precise specs without leaving the chat.

### 3. Asset Export Pipeline

> **Prompt:** _"Export all icon frames `1:10`, `1:11`, `1:12` as SVGs from file `abc123`"_

The agent calls `export_assets` with `format=svg` and returns download URLs for each icon, ready for use in code.

### 4. Style Token Extraction

> **Prompt:** _"What are all the color and text styles in file `myDesign`? Format them as CSS variables"_

Uses `list_styles` to pull every defined style, then the LLM formats them into usable CSS custom properties:

```css
--color-primary: #3B82F6;
--color-secondary: #10B981;
--font-heading: Inter, 24px, 700;
```

### 5. Design Review / QA

> **Prompt:** _"Get the full structure of file `abc123` and check if all frames have consistent padding"_

Fetches the entire file with `get_figma_file`, then the LLM traverses the node tree to flag layout inconsistencies.

### 6. Multi-File Comparison

> **Prompt:** _"Compare the components in file `designV1` vs `designV2` and list what changed"_

Calls `list_components` on both files, and the LLM diffs the results to produce a changelog of design changes.

## Example Prompts

Here are ready-to-use prompts for Claude Desktop with this MCP server:

```
"Get the structure of my Figma file with key abc123XYZ"

"Show me all components in this design file"

"Export frame 1:42 as an SVG"

"What text styles are defined in this design?"

"Extract the layout specs for nodes 1:2 and 3:4"

"List all color styles and convert them to a Tailwind config"

"Get the login page frame and describe the UI elements"
```

## API Reference

### get_figma_file
| Param | Type | Description |
|-------|------|-------------|
| `file_key` | `str` | Figma file key |

### get_frame_nodes
| Param | Type | Description |
|-------|------|-------------|
| `file_key` | `str` | Figma file key |
| `node_ids` | `list[str]` | Node IDs (e.g., `["1:2", "3:4"]`) |

### list_components
| Param | Type | Description |
|-------|------|-------------|
| `file_key` | `str` | Figma file key |

### list_styles
| Param | Type | Description |
|-------|------|-------------|
| `file_key` | `str` | Figma file key |

### export_assets
| Param | Type | Description |
|-------|------|-------------|
| `file_key` | `str` | Figma file key |
| `node_ids` | `list[str]` | Node IDs to export |
| `format` | `str` | `png`, `jpg`, `svg`, `pdf` (default: `png`) |
| `scale` | `float` | Scale factor (default: `2.0`) |

## Running Tests

```bash
pytest tests/ -v
```

## License

MIT
