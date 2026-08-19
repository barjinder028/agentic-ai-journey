
Learning to build AI agents from scratch, working toward an
agentic AI engineering role. Documenting daily progress, code,
and what I'm learning along the way.

Full daily log: see [log.md](log.md)

## Progress
- Day 1: Environment setup (WSL, Python, Git, GitHub)
- Day 2: Python fundamentals — dictionaries, functions, mutability, debugging
- Day 3: Error handling, file I/O, JSON
- Day 4: First real API call, reusable functions, knowledge cutoffs
- Day 5: First tools — connecting Python functions to the model, docstrings, multi-tool calls
- Day 6: Conversation history — why models have no memory, building a stateful chatbot
- Day 7: Classes and self from scratch — built Person and BankAccount, caught and fixed a real return-value bug
- Day 8: Built a proper Agent class combining tools and conversation memory together
- Day 9: Disabled automatic function calling and rebuilt the tool-call loop by hand
- Day 10: Built the real agent loop with while, handling multiple dependent tool calls
- Day 11: Merged memory, tools, and the loop into one real Agent class, with round limits and tool-failure handling
- Day 12: Embeddings and cosine similarity, built the core retrieval mechanism by hand
- Day 13: Chunked a real document, built a formal search function, found a real limitation in similarity-based retrieval
- Day 14: Built a working RAG pipeline, retrieval plus grounded generation with honest refusal
- Day 15: Built a real evaluation set, caught a hidden bug in my own eval code, found the true root cause
- Day 16: Cached embeddings to a JSON file, debugged three real bugs along the way
- Day 17: Added a hash check so the embedding cache actually detects when the document changes
- Day 18: Ran the full pipeline on a real resume, found and diagnosed a genuine similarity-search limitation and an eval-design fragility
- Day 19: Fixed the eval fragility from Day 18, evaluation now checks retrieved text instead of a fragile chunk index
- **[RAG Resume Assistant](projects/rag-resume-assistant)** — first capstone project: a full retrieval-augmented generation pipeline with a working evaluation harness, built from Day 12 through Day 19
- Day 21: First framework (LangChain) — rebuilt the Day 11 agent with create_agent and @tool, recognized every internal piece from building it by hand
- Day 22: Real cross-conversation memory with LangGraph's checkpointer and thread_id, a capability my own from-scratch agent couldn't do without real extra work
- Day 23: Multi-agent supervisor pattern, migrated to Azure OpenAI with keyless auth after hitting a real provider quota wall
- Day 24: Wired the RAG capstone in as a third supervisor specialist, found and fixed a real routing bug where the supervisor silently answered instead of handing off
- Day 25: Built a routing evaluation harness with a deliberate regression test for the Day 24 supervisor bug, 100% accuracy

- **[Multi-agent supervisor system](projects/multi-agent-supervisor)** - second capstone: a supervisor agent routing across three specialists, with a routing evaluation harness and a diagnosed, fixed delegation bug

- Day 26: Built real cost tracking, tokens and dollars per question, found routing overhead and retrieved-context volume are separate cost drivers