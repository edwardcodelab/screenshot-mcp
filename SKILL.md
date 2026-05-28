# Screenshot MCP Skill

## Overview
This skill allows Hermes Agent to capture screenshots of the user's desktop using a custom MCP server running on the host machine.

**MCP Server:** `localhost:8001`

## How to Use

### Basic Usage
Ask Hermes to take a screenshot using any of these prompts:

- "Take a screenshot"
- "Capture my screen"
- "Use the screenshot tool"
- "Show me what's on my desktop"

### Advanced Usage
- "Take a screenshot and describe what you see"
- "Capture the screen and tell me what apps are open"
- "Take a screenshot of the region 100,100,800,600"
- "Monitor my screen and alert me if something changes"

### With Specific Instructions
- "Take a screenshot and check if Chrome is open"
- "Capture my desktop and summarize what I'm working on"
- "Take a screenshot and save it with today's date"

## Configuration

Add this to your Hermes `config.yaml`:

```yaml
mcp_servers:
  screenshot:
    url: "http://localhost:8001"
    timeout: 30
```

Then restart Hermes:

```bash
docker restart <hermes-container>
```

## Available Tool

### `take_screenshot`
- **Description:** Captures a screenshot of the desktop
- **Parameters:**
  - `region` (optional): "full" or "x,y,width,height" (e.g., "100,100,800,600")
- **Returns:** Image (PNG format)

## Best Practices

1. **Always use clear instructions** — Hermes works best when you tell it what to do with the screenshot
2. **Combine with other tools** — Use together with memory, file operations, or web search
3. **Test first** — Run `uv run test_mcp_screenshot.py` on the host to verify the server is working
4. **Use specific regions** when you only need part of the screen (faster)

## Example Workflows

### Daily Check-in
```
Take a screenshot of my desktop and tell me what I'm working on today.
```

### Security Monitoring
```
Take a screenshot every 30 seconds. If you see anything suspicious, alert me.
```

### Documentation
```
Take a screenshot of my current work and save it with a timestamp.
```

## Troubleshooting

- **Black screenshot?** Make sure the MCP server is running with `uv run screenshot_mcp.py`
- **Connection error?** Check that `localhost:8001` is reachable from inside Docker
- **Timeout?** Increase `timeout` value in config.yaml

## Protocol & Method

**Protocol:** Model Context Protocol (MCP) over HTTP (Streamable HTTP transport)

**Screenshot Method:** `pyscreenshot` library (cross-platform, works on Wayland + X11)

The MCP server runs on the host machine and exposes the `take_screenshot` tool via HTTP. Hermes connects to it and receives the image back as PNG data.

## Python Example

```python
import asyncio
from mcp.client.session import ClientSession
from mcp.client.streamable_http import streamablehttp_client
import base64

async def get_screenshot():
    async with streamablehttp_client("http://localhost:8001/mcp") as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Call the tool
            result = await session.call_tool("take_screenshot", {"region": "full"})
            
            # Get the image
            if result.content and result.content[0].type == "image":
                image_data = base64.b64decode(result.content[0].data)
                
                with open("screenshot.png", "wb") as f:
                    f.write(image_data)
                print("Screenshot saved as screenshot.png")

asyncio.run(get_screenshot())
```

## Notes

- Works on Wayland (Ubuntu 22.04+)
- Uses pyscreenshot backend (reliable)
- Server must be running on host machine
- Image is returned in PNG format
- Supports full screen or custom regions

---
