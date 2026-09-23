# LangChain + DeepWiki starter agent

An interactive terminal agent using OpenAI `gpt-5-mini` and the three public DeepWiki MCP tools. The model decides whether to call a tool for each prompt; tool calls are printed in the terminal. DeepWiki covers public GitHub repositories.

## Set up

In PowerShell:

```powershell
cd 'C:\Users\ma_na\Documents\JobHunting2026\ai_playground\langchain'
.\setup.ps1
```

Create an OpenAI API key at <https://platform.openai.com/api-keys>. API billing is separate from ChatGPT Plus. Add a payment method or prepaid credit at <https://platform.openai.com/settings/organization/billing/overview>. Do not paste your key into a chat or commit it to Git.

Set the key for the current PowerShell session and start the agent:

```powershell
$env:OPENAI_API_KEY = 'paste-your-key-here'
.\run.ps1
```

The key exists only in this PowerShell session. To use a different model, set `$env:OPENAI_MODEL` before launching.

For a potentially faster and cheaper non-reasoning model, try `$env:OPENAI_MODEL = 'gpt-4o-mini'` before `./run.ps1`. It may be less capable at deciding when to use a tool. The agent prints elapsed time for each reply. A dropped DeepWiki SSE response is retried once; if that happens, the turn can take longer and may use extra model tokens.

## Try it

Ask `Say hello in one sentence.` for a prompt that should not need DeepWiki. Then ask `Using DeepWiki, what does the langchain-ai/langchain repository say about agents?` to observe an MCP call. The model makes the tool decision, so a particular call is not guaranteed unless you explicitly request it. Type `/quit` to exit. Chat history lasts for the current run only.

DeepWiki endpoint: <https://mcp.deepwiki.com/mcp>. It requires no DeepWiki key, but each model request uses your OpenAI API credits. If the endpoint is unavailable, the app reports a connection error.
