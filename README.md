# screenshot-mcp
A lightweight MCP (Model Context Protocol) server that allows AI agents like **Hermes** to capture screenshots of your desktop.

## Features

- ✅ Works on **Wayland** (Ubuntu 22.04+, Fedora, etc.)
- ✅ Uses `pyscreenshot` backend (reliable cross-platform)
- ✅ Supports full screen or custom regions
- ✅ Returns images in PNG format
- ✅ Easy integration with Hermes Agent
- ✅ Includes GUI control panel (optional)

## Quick Start

### 1. Install Dependencies

```bash
pip install fastmcp pyscreenshot Pillow mcp
```

Or using `uv`:

```bash
uv pip install fastmcp pyscreenshot Pillow mcp
```

### 2. Start the MCP Server

```bash
python screenshot_mcp.py
```

The server will run on `http://0.0.0.0:8001`

### 3. Connect to Hermes Agent

Add this to your Hermes `config.yaml`:

```yaml
mcp_servers:
  screenshot:
    url: "http://YOUR_HOST_IP:8001"
    timeout: 30
```

Then restart Hermes:

```bash
docker restart <hermes-container>
```

### 4. Use It

Talk to Hermes:

- "Take a screenshot"
- "Capture my screen and describe what you see"
- "Take a screenshot of the region 100,100,800,600"

## Project Structure

```
screenshot_mcp/
├── screenshot_mcp.py      # Main MCP server
├── screenshot_mcp_gui.py  # GUI control panel (optional)
├── test_mcp_screenshot.py # Test script
├── SKILL.md               # Hermes skill documentation
└── README.md              # This file
```

## How It Works

1. The MCP server runs on your host machine
2. Hermes (running in Docker) connects via HTTP
3. When you ask Hermes to take a screenshot, it calls the `take_screenshot` tool
4. The server captures the screen using `pyscreenshot`
5. The image is sent back to Hermes as PNG data

## Available Tool

### `take_screenshot`

**Parameters:**
- `region` (optional): `"full"` or `"x,y,width,height"` (e.g. `"100,100,800,600"`)

**Returns:** PNG image

## GUI Version (Optional)

If you prefer a graphical interface:

```bash
python screenshot_mcp_gui.py
```

This provides:
- Start/Stop server buttons
- Manual screenshot button
- Live screenshot counter

## Troubleshooting

### Black Screenshot
- Make sure the server is running
- Try the GUI version instead
- On some systems, you may need to log in using "Ubuntu on Xorg"

### Connection Error
- Check that port 8001 is not blocked by firewall
- Use `localhost` or your actual host IP in Hermes config
- Make sure Hermes container can reach the host

### Timeout
- Increase the `timeout` value in Hermes config
- The first screenshot may take longer

## Requirements

- Python 3.10+
- `fastmcp`
- `pyscreenshot`
- `Pillow`

## License

MIT License

---
