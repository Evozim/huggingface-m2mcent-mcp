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
                    "Price (USDC)": f"${t.get('price', '0.05')}",
                    "Description": t.get("description", "")[:100] + "..."
                })
            return pd.DataFrame(df_data)
    except Exception as e:
        pass
    return pd.DataFrame([
        {"Name": "autonomous-trading-bot-mcp", "Category": "DeFi / Trading", "Price (USDC)": "$0.05", "Description": "Real MACD/RSI indicators computed over 50 live Coinbase Exchange candles"},
        {"Name": "credit-risk-mcp", "Category": "DeFi", "Price (USDC)": "$0.05", "Description": "Real-time algorithmic credit risk scoring and debt solvency modeling"},
        {"Name": "stealth-address-generator-mcp", "Category": "Cryptography", "Price (USDC)": "$0.08", "Description": "EIP-5564 ECDH ephemeral stealth address derivation for private settlement"},
        {"Name": "vouch-agent-trust-verifier", "Category": "Security / Vouch", "Price (USDC)": "$0.02", "Description": "W3C DID and Post-Quantum cryptographic signature validator"}
    ])

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
                    "Price (USDC)": f"${t.get('price', '0.05')}",
                    "Description": t.get("description", "")[:100] + "..."
                })
            return pd.DataFrame(df_data)
    except Exception:
        pass
    return pd.DataFrame()

def inspect_tool(tool_name):
    if not tool_name:
        return "Please enter a tool slug (e.g., 'autonomous-trading-bot-mcp')"
    slug = tool_name.strip().lower()
    try:
        resp = requests.get(f"{API_GATEWAY_URL}/{slug}/server-card.json", timeout=10)
        if resp.status_code == 200:
            return json.dumps(resp.json(), indent=2)
        else:
            return f"Tool schema returned HTTP {resp.status_code}"
    except Exception as e:
        return f"Error querying tool: {str(e)}"

with gr.Blocks(title="M2MCent MCP Universal Gateway (1,062 AI Agent Micro-Services)", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🚀 M2MCent Universal MCP Gateway")
    gr.Markdown("Explore, query, and test **1,062 specialized MCP micro-services** (896 Flagship deterministic engines) for autonomous AI agents monetized via **x402 on Base Mainnet**.")

    with gr.Tab("🔍 Tool Catalog & Search"):
        with gr.Row():
            search_input = gr.Textbox(placeholder="Search by keyword (e.g., 'defi', 'credit', 'security', 'solidity', 'zk', 'stealth')...", label="Semantic Tool Search", scale=4)
            search_btn = gr.Button("Search", variant="primary", scale=1)
        
        catalog_table = gr.Dataframe(value=get_tools_catalog(), interactive=False, label="Available M2MCent Micro-Services")
        search_btn.click(fn=search_tools, inputs=[search_input], outputs=[catalog_table])
        search_input.submit(fn=search_tools, inputs=[search_input], outputs=[catalog_table])

    with gr.Tab("🛠️ Inspect Tool Schema"):
        tool_slug_input = gr.Textbox(placeholder="e.g. autonomous-trading-bot-mcp", label="Tool Slug")
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
        - **Smart Contract Escrow:** `0x5d47070A36A37DAf417e64FF27a1e5B3F1c84efa` (Base Mainnet)
        - **Institutional Treasury Safe:** `0x8aaBAB75bE8825d0f5D514a9a5cBa04B7bF84920`
        - **Protocol:** x402 V2 Micropayment Protocol with EIP-3009 TransferWithAuthorization
        - **Trust & Compliance:** Vouch Protocol Grade A (100/100) & Post-Quantum ML-DSA-65 Readiness
        """)

if __name__ == "__main__":
    demo.launch()
