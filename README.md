---
title: M2MCent Universal MCP Gateway (1,005 AI Agent Micro-Services)
emoji: 🤖
colorFrom: indigo
colorTo: blue
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
pinned: true
tags:
  - mcp
  - model-context-protocol
  - x402
  - base-mainnet
  - autonomous-agents
  - tools
  - api-gateway
license: mit
---

# 🚀 M2MCent Universal MCP Gateway (1,005 Nodes)

**M2MCent** is the world's largest decentralized Model Context Protocol (MCP) micro-service network built for autonomous AI agents, monetized via **x402 V2 on Base Mainnet**.

## 📌 Features
- **1,005 High-Priority Endpoints:** Legal, finance, smart contract security, bioinformatics, IoT, 3D spatial processing.
- **Trustless Micropayments:** Zero-gas cryptographic settlement via EIP-3009 and smart contract escrow (`0xDb48F51A2de8F4a80CD1d0BAdcd18E847734A74a`).
- **Universal Transports:** Supports MCP SSE, JSON-RPC 2.0, REST, and OpenAI Agent Plugin format.

## 🛠️ Tools Connection

Any MCP-compatible client (Claude Desktop, Cursor, LangChain, Transformers, Flowise) can connect to the monolithic gateway:

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

### Full Catalog & API Documentation
- **Tools List:** `https://api.m2mcent.com/api/v1/tools`
- **Semantic Search:** `https://api.m2mcent.com/api/v1/search?q={query}`
- **OpenAPI 3.1 Spec:** `https://api.m2mcent.com/.well-known/openapi.json`
- **LLMs.txt Standard:** `https://api.m2mcent.com/llms.txt`
