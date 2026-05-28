#!/usr/bin/env python3
"""
Test script to verify the Screenshot MCP server is working.
This connects to the running MCP server and calls take_screenshot.
"""

import asyncio
from mcp.client.session import ClientSession
from mcp.client.streamable_http import streamablehttp_client

async def test_screenshot():
    print("🔌 Connecting to Screenshot MCP Server...")
    
    async with streamablehttp_client("http://localhost:8001/mcp") as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print("✅ Connected successfully!")
            print("\n📸 Calling take_screenshot tool...")
            
            # Call the tool
            result = await session.call_tool("take_screenshot", {"region": "full"})
            
            print("\n📥 Result received!")
            print(f"   Type: {type(result)}")
            print(f"   Content count: {len(result.content) if hasattr(result, 'content') else 'N/A'}")
            
            # Check if we got an image
            if hasattr(result, 'content') and result.content:
                for i, content in enumerate(result.content):
                    if hasattr(content, 'type') and content.type == 'image':
                        print(f"   ✅ Image received! (index {i})")
                        print(f"   MIME Type: {content.mimeType}")
                        print(f"   Data length: {len(content.data)} chars (base64)")
                        
                        import base64
                        # Decode base64 string to bytes
                        image_bytes = base64.b64decode(content.data)
                        
                        # Save the image
                        with open("test_screenshot.png", "wb") as f:
                            f.write(image_bytes)
                        print("\n💾 Saved as: test_screenshot.png")
                        print(f"   File size: {len(image_bytes)} bytes")
                    else:
                        print(f"   Content {i}: {content}")
            else:
                print(f"   Result: {result}")
    
    print("\n🎉 Test completed successfully!")

if __name__ == "__main__":
    asyncio.run(test_screenshot())
