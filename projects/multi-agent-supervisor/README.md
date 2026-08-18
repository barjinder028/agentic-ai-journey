# Multi-Agent Supervisor System

A supervisor agent that routes questions across three specialist agents, with an evaluation harness that checks whether routing decisions are actually correct, not just whether the final answers sound right.

## What it does

This project has one supervisor agent that manages task flow across three specialist agents, each built to handle one narrow kind of question: dates, arithmetic, and resume lookups. It includes a pre-written evaluation set that checks whether the supervisor is actually delegating questions to the right specialist, not just whether the final answers sound reasonable.

## How it works

1. The resume, `my_document.txt`, is loaded and split into chunks, once, ahead of time
2. Each chunk is embedded and the results are cached to `my_document_embeddings.json`, so this only has to happen again if the document actually changes
3. Three specialist agents are built, each with its own narrow tool: a date agent, a math agent, and a resume agent that can search the embedded resume
4. All three specialists are handed to a supervisor agent, treated as tools the supervisor can call
5. When a user asks a question, the supervisor's model decides which specialist is relevant and hands the question over to it
6. That specialist runs its own reasoning and its own tool. For the resume agent specifically, that means embedding the question itself, comparing it against every cached document chunk with cosine similarity, and pulling back the closest matches
7. The specialist answers using only what it actually found, then hands control back to the supervisor, which relays the final answer

## Evaluation results

The routing evaluation set currently scores 100%, but it only covers five hand-picked, fairly clear-cut questions. Harder edge cases, like a question that could plausibly belong to two specialists at once, or ambiguous phrasing, aren't covered yet, and are worth exploring further.

## What I found while testing

While testing, I found that when a user asked a question with no real mention in the embedded resume, the supervisor didn't hand the question off to any specialist at all. Instead, it answered directly, with replies like "I don't know which person you are referring to," even though the resume agent, if it had actually been given the question, would have correctly said the resume doesn't cover it.

I confirmed this by printing the full message trace and seeing that no specialist name ever appeared in it, the supervisor had answered the question itself.

The fix was in the supervisor's own prompt, not the specialist's. I added an explicit instruction telling the supervisor that any question mentioning the resume's subject by name should always be handed to the resume agent, even if the supervisor itself doesn't know the answer, rather than letting the supervisor judge on its own whether a question sounded resume-related enough to delegate. This exact question is now included in the evaluation set as a permanent regression test.

## How to run it

Install the dependencies:

```
pip install langchain langchain-openai langchain-core langgraph-supervisor azure-identity google-genai python-dotenv
```

Set up Azure keyless authentication first:

```
az login
```

Create a `.env` file with your Google API key, used for embeddings:

```
GOOGLE_API_KEY=your-key-here
```

Place your document as `my_document.txt` in the same folder, paragraphs separated by blank lines, then run:

```
python3 multi_agent.py
```

## Tech stack

LangChain and LangGraph for the agent framework, `langgraph-supervisor` for routing. Chat runs on Azure OpenAI (`gpt-5-mini`) with keyless authentication via `DefaultAzureCredential`, since embeddings and chat completions are separate services with separate quotas, embeddings run on Gemini's embedding model directly. Cosine similarity is computed from scratch, same as the RAG Resume Assistant project this one builds on.