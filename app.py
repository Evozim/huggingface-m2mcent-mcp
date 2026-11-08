import gradio as gr
import requests
import json
import pandas as pd

API_GATEWAY_URL = "https://api.m2mcent.com"


def get_tools_catalog():
    try:
        resp = requests.get(f"{API_GATEWAY_URL}/api/v1/tools", params={"limit": 100}, timeout=8)
        if resp.status_code == 200:
            data = resp.json()
            tools = data.get("tools", [])
            df_data = []
            for t in tools:
                price_val = t.get("price_usdc") or t.get("price") or "0.025"
                sla_str = (t.get("sla") or {}).get("engine_compute_latency", "<250ms deterministic")
                df_data.append({
                    "Slug": t.get("id") or t.get("name", ""),
                    "Domain": t.get("domain") or t.get("category", "utility"),
                    "Price (USDC)": f"${price_val}",
                    "Compute SLA": sla_str,
                    "Description": (t.get("description", "") or "")[:110]
                })
            if df_data:
                return pd.DataFrame(df_data)
    except Exception:
        pass
    return pd.DataFrame([
        {"Slug": "autonomous-trading-bot-mcp", "Domain": "Industrial Finance & Crypto", "Price (USDC)": "$0.025", "Compute SLA": "<250ms deterministic", "Description": "Real EMA-12/26/9 MACD & Wilder RSI-14 computed over 50 live Coinbase Exchange candles"},
        {"Slug": "credit-risk-mcp", "Domain": "DeFi & Risk", "Price (USDC)": "$0.050", "Compute SLA": "<250ms deterministic", "Description": "Real-time algorithmic credit risk scoring and debt solvency modeling"},
        {"Slug": "stealth-address-generator-mcp", "Domain": "Cryptography", "Price (USDC)": "$0.050", "Compute SLA": "<250ms deterministic", "Description": "EIP-5564 ECDH ephemeral stealth address derivation for private settlement"},
        {"Slug": "gas-pulse-mcp", "Domain": "Base L2 Telemetry", "Price (USDC)": "$0.010", "Compute SLA": "<250ms deterministic", "Description": "Live Base Mainnet feeData & L1/L2 execution cost estimator (<140ms RPC budget)"}
    ])


def search_tools(query):
    if not query:
        return get_tools_catalog()
    try:
        resp = requests.get(f"{API_GATEWAY_URL}/api/v1/search", params={"q": query, "limit": 30}, timeout=8)
        if resp.status_code == 200:
            results = resp.json().get("results", [])
            df_data = []
            for t in results:
                price_val = t.get("price_usdc") or t.get("price") or "0.025"
                df_data.append({
                    "Slug": t.get("id") or t.get("name", ""),
                    "Domain": t.get("domain") or t.get("category", "General"),
                    "Price (USDC)": f"${price_val}",
                    "Compute SLA": "<250ms deterministic",
                    "Description": (t.get("description", "") or "")[:110]
                })
            return pd.DataFrame(df_data)
    except Exception:
        pass
    return get_tools_catalog()


def inspect_tool(tool_name):
    if not tool_name:
        return json.dumps({"error": "Please enter a tool slug (e.g., 'autonomous-trading-bot-mcp')"}, indent=2)
    slug = tool_name.strip().lower()
    try:
        resp = requests.get(f"{API_GATEWAY_URL}/{slug}/schema", timeout=8)
        if resp.status_code == 200:
            return json.dumps(resp.json(), indent=2)
        return json.dumps({"error": f"Schema returned HTTP {resp.status_code}", "slug": slug}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e), "slug": slug}, indent=2)


def preview_tool_dry_run(tool_name, raw_payload):
    if not tool_name:
        return json.dumps({"error": "Enter a tool slug (e.g., autonomous-trading-bot-mcp)"}, indent=2)
    slug = tool_name.strip().lower()
    try:
        payload = json.loads(raw_payload) if raw_payload else {}
    except Exception as e:
        return json.dumps({"error": f"Invalid JSON payload: {e}"}, indent=2)
    try:
        resp = requests.post(f"{API_GATEWAY_URL}/{slug}/api/preview", json=payload, timeout=8)
        return json.dumps(resp.json(), indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


with gr.Blocks(title="M2MCent Universal MCP Gateway (1,057 Deterministic Nodes)", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🚀 M2MCent Universal MCP Gateway (x402 V2 · Vouch Grade A 100/100)")
    gr.Markdown(
        "Explore, validate, and connect to **1,057 deterministic AI agent micro-services** (`$0.010`–`$0.250` USDC, `<250ms` compute SLA) "
        "monetized via **x402 V2 EIP-3009** on **Base Mainnet (`eip155:8453`)**."
    )

    with gr.Tab("🔍 Tool Catalog & Search"):
        with gr.Row():
            search_input = gr.Textbox(
                placeholder="Search by keyword (e.g., 'trading', 'credit', 'security', 'solidity', 'zk', 'gas')...",
                label="Semantic / Keyword Tool Search",
                scale=4
            )
            search_btn = gr.Button("Search", variant="primary", scale=1)

        catalog_table = gr.Dataframe(value=get_tools_catalog(), interactive=False, label="M2MCent Deterministic Micro-Services")
        search_btn.click(fn=search_tools, inputs=[search_input], outputs=[catalog_table])
        search_input.submit(fn=search_tools, inputs=[search_input], outputs=[catalog_table])

    with gr.Tab("🛠️ Inspect Schema & Free Dry-Run Preview"):
        with gr.Row():
            tool_slug_input = gr.Textbox(value="autonomous-trading-bot-mcp", label="Tool Slug")
            payload_input = gr.Textbox(value='{"symbol": "ETH"}', label="JSON Payload (Free /api/preview Dry-Run)")
        with gr.Row():
            inspect_btn = gr.Button("Fetch /:slug/schema", variant="secondary")
            preview_btn = gr.Button("Run Free /:slug/api/preview", variant="primary")
        schema_output = gr.Code(language="json", label="Gateway Output")
        inspect_btn.click(fn=inspect_tool, inputs=[tool_slug_input], outputs=[schema_output])
        preview_btn.click(fn=preview_tool_dry_run, inputs=[tool_slug_input, payload_input], outputs=[schema_output])

    with gr.Tab("📖 Quickstart & SDKs"):
        gr.Markdown("""
### Official Agent Connectors
- **ElizaOS:** `npm install @evozim/eliza-plugin-x402@1.0.6`
- **LangChain (Python):** `pip install m2mcent-langchain-x402==1.0.3`
- **LangChain (TypeScript):** `npm install @evozim/langchain-plugin-x402`
- **CrewAI:** `pip install crewai-plugin-x402==1.0.3`
- **LlamaIndex:** `pip install m2mcent-llamaindex-x402==1.0.3`
- **AutoGen:** `pip install autogen-plugin-x402==1.0.3`
- **Hugging Face Agents:** `pip install m2mcent-huggingface-x402`

### Smart Contract & Trust Architecture
- **Base Mainnet Escrow Contract:** `0x5d47070A36A37DAf417e64FF27a1e5B3F1c84efa`
- **Institutional Treasury Safe:** `0x8aaBAB75bE8825d0f5D514a9a5cBa04B7bF84920`
- **Vouch Trust Index:** Grade A (`100/100`) · `did:web:m2mcent.com` · Post-Quantum `ML-DSA-65` (FIPS 204)
- **SLA Boundary:** `<250ms` deterministic in-memory engine compute · `<5,000ms` Base L2 EIP-3009 on-chain settlement
        """)

if __name__ == "__main__":
    demo.launch()
