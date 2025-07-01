#!/usr/bin/env python3
import smolagents
import databricks.sdk
import mcp
import os

MODEL = "data-science-gpt-4o"

wc = databricks.sdk.WorkspaceClient()
client = wc.serving_endpoints.get_open_ai_client()

# create a smolagents agent
model = smolagents.OpenAIServerModel(
    model_id=MODEL,
    client=client,
)

# Connect to your Monday MCP server (assuming you have monday_server.py in same directory)
params = mcp.StdioServerParameters(
    command="python",
    args=["src/monday_ai_agent/monday_server.py"],
    env={"MONDAY_API_KEY": os.environ["MONDAY_API_KEY"]}
)

def main() -> None:
    with smolagents.ToolCollection.from_mcp(
        params, trust_remote_code=True
    ) as tool_collection:
        agent = smolagents.ToolCallingAgent(
            tools=[*tool_collection.tools], 
            model=model, 
            add_base_tools=False
        )
        
        # create ui
        ui = smolagents.GradioUI(
            agent, 
            file_upload_folder="uploads", 
            reset_agent_memory=False
        )
        ui.launch()

if __name__ == "__main__":
    main()