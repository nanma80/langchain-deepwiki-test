"""A small interactive LangChain agent with DeepWiki MCP tools."""

import asyncio
import os
import sys
import time

from langchain.agents import create_agent
from langchain.mcp import MCPAdapter
from langchain_openai import ChatOpenAI


DEEPWIKI_URL = "https://mcp.deepwiki.com/mcp"
MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")


def show_content(content):
    if isinstance(content, str):
        return content
    return "\n".join(
        block.get("text", str(block)) if isinstance(block, dict) else str(block)
        for block in content
    )


async def main():
    if not os.getenv("OPENAI_API_KEY"):
        print("OPENAI_API_KEY is missing. See README.md for setup.", file=sys.stderr)
        return 1

    print(f"Connecting to DeepWiki MCP at {DEEPWIKI_URL}...")
    try:
        async with MCPAdapter(DEEPWIKI_URL) as adapter:
            tools = await adapter.list_tools()
            print("DeepWiki tools: " + ", ".join(tool.name for tool in tools))
            agent = create_agent(
                model=ChatOpenAI(model=MODEL),
                tools=tools,
                system_prompt=(
                    "You are a helpful assistant. Use DeepWiki tools when the user asks "
                    "about a public GitHub repository and the tools would help. "
                    "For ordinary chat, answer without calling a tool. "
                    "If you use DeepWiki, say which repository the answer concerns. "
                    "Do not claim to have consulted DeepWiki unless you called it."
                ),
            )
            messages = []
            print("Ready. Type /quit to exit. Tool calls are shown after each reply.\n")
            while True:
                try:
                    prompt = input("You> ").strip()
                except (EOFError, KeyboardInterrupt):
                    print()
                    break
                if not prompt:
                    continue
                if prompt.lower() in {"/quit", "/exit"}:
                    break
                started = time.perf_counter()
                result = None
                for attempt in range(2):
                    try:
                        result = await agent.ainvoke(
                            {"messages": messages + [{"role": "user", "content": prompt}]}
                        )
                        break
                    except Exception as exc:
                        if attempt == 0 and "SSE stream ended without a response" in str(exc):
                            print("DeepWiki connection dropped; retrying once...")
                            await asyncio.sleep(1)
                            continue
                        print(f"Request failed: {exc}", file=sys.stderr)
                if result is None:
                    continue
                new_messages = result["messages"][len(messages) + 1 :]
                for message in new_messages:
                    for call in getattr(message, "tool_calls", []) or []:
                        print(f"[MCP tool: {call['name']} {call['args']}]")
                print("Agent> " + show_content(result["messages"][-1].content) + "\n")
                print(f"[Elapsed: {time.perf_counter() - started:.1f}s]\n")
                messages = result["messages"]
                print("**** messages list starts ****")
                for message in messages:
                    print(message)
                print("**** messages list ends ****")
                print("messages length:", len(messages))
    except Exception as exc:
        print(f"Could not connect to DeepWiki MCP: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
