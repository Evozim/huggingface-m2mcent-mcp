import gradio as gr
import requests
import json
import pandas as pd

API_GATEWAY_URL = "https://api.m2mcent.com"

def get_tools_catalog():
    try:
        resp = requests.get(f"{API_GATEWAY_URL}/api/v1/tools", timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            tools = data.get("tools", [])
            df_data = []
            for t in tools:
                df_data.append({
                    "Name": t.get("name", ""),
                    "Category": t.get("category", "utility"),
                    "Price (USDC)": f"${t.get('price', '0.15')}",
                    "Description": t.get("description", "")[:100] + "..."
                })
            return pd.DataFrame(df_data)
    except Exception as e:
        pass
    return pd.DataFrame([{"Name": "Credit Risk", "Category": "DeFi", "Price (USDC)": "$0.05", "Description": "Real-time credit risk scoring"}])

def search_tools(query):
    if not query:
        return get_tools_catalog()
    try:
        resp = requests.get(f"{API_GATEWAY_URL}/api/v1/search", params={"q": query, "limit": 25}, timeout=10)
        if resp.status_code == 200:
            results = resp.json().get("results", [])
            df_data = []
            for t in results:
                df_data.append({
                    "Name": t.get("name", t.get("id", "")),
                    "Category": t.get("category", "General"),
                    "Price (USDC)": f"${t.get('price', '0.15')}",
                    "Description": t.get("description", "")[:100] + "..."
                })
            return pd.DataFrame(df_data)
    except Exception:
        pass
    return pd.DataFrame()

def inspect_tool(tool_name):
    if not tool_name:
        return "Please enter a tool slug (e.g., 'credit-risk-mcp')"
    slug = tool_name.strip().lower()
    try:
        resp = requests.get(f"{API_GATEWAY_URL}/{slug}/server-card.json", timeout=10)
        if resp.status_code == 200:
            return json.dumps(resp.json(), indent=2)
        else:
            return f"Tool schema returned HTTP {resp.status_code}"
    except Exception as e:
        return f"Error querying tool: {str(e)}"

with gr.Blocks(title="M2MCent MCP Universal Gateway (1,005 AI Agent Micro-Services)", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🚀 M2MCent Universal MCP Gateway")
    gr.Markdown("Explore, query, and test **1,005 specialized MCP micro-services** for autonomous AI agents monetized via **x402 on Base Mainnet**.")

    with gr.Tab("🔍 Tool Catalog & Search"):
        with gr.Row():
            search_input = gr.Textbox(placeholder="Search by keyword (e.g., 'defi', 'credit', 'security', 'solidity', 'zk')...", label="Semantic Tool Search", scale=4)
            search_btn = gr.Button("Search", variant="primary", scale=1)
        
        catalog_table = gr.Dataframe(value=get_tools_catalog(), interactive=False, label="Available M2MCent Micro-Services")
        search_btn.click(fn=search_tools, inputs=[search_input], outputs=[catalog_table])
        search_input.submit(fn=search_tools, inputs=[search_input], outputs=[catalog_table])

    with gr.Tab("🛠️ Inspect Tool Schema"):
        tool_slug_input = gr.Textbox(placeholder="e.g. credit-risk-mcp", label="Tool Slug")
        inspect_btn = gr.Button("Fetch Server Card & Schema", variant="secondary")
        schema_output = gr.Code(language="json", label="MCP Server Card & Capabilities")
        inspect_btn.click(fn=inspect_tool, inputs=[tool_slug_input], outputs=[schema_output])

    with gr.Tab("📖 Quickstart Guide"):
        gr.Markdown("""
        ### Connecting your MCP Client
        Add M2MCent to your `mcpServers` configuration:
        ```json
        {
          "mcpServers": {
            "m2mcent": {
              "url": "https://api.m2mcent.com/sse",
              "type": "sse"
            }
          }
        }
        ```
        - **Smart Contract Escrow:** `0xDb48F51A2de8F4a80CD1d0BAdcd18E847734A74a` (Base Mainnet)
        - **Protocol:** x402 V2 Micropayment Protocol with EIP-3009 TransferWithAuthorization
        """)

if __name__ == "__main__":
    demo.launch()
