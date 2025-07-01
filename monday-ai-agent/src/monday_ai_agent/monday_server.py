import os
import httpx
from mcp.server.fastmcp import FastMCP

# Create MCP server
mcp = FastMCP("Monday Server")

# Monday.com API setup
API_KEY = os.getenv("MONDAY_API_KEY")
API_URL = "https://api.monday.com/v2"

@mcp.tool()
async def get_boards() -> str:
    """Get Monday boards"""
    
    query = '''{
  boards {
    id
    name
    items_page(limit: 500) {
      cursor
      items {
        id
        name
        column_values {
          id
          text
          value
        }
         updates {
          id
          body
          created_at
          creator {
            name
          }
          replies {
            id
            body
            created_at
            creator {
              name
            }
          }
        }
    
      }
    }
  }
}'''
    headers = {"Authorization": API_KEY}
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            API_URL, 
            json={"query": query}, 
            headers=headers
        )
        data = response.json()
        return str(data)
        #return str([b["name"] for b in boards])

if __name__ == "__main__":
    mcp.run()