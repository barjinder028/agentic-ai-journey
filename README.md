
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
