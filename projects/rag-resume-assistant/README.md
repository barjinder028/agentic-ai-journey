# RAG Resume Assistant

Answers questions about a resume using retrieval-augmented generation, backed by a tested evaluation harness that measures how often it actually finds the right answer.

## What it does

This project lets you ask questions about a document, in this case my old resume file, and get answers grounded in what the document actually says. Instead of relying on the model's general training, the system searches the real document that was provided and provides back the most relevant sections first, then builds an answer only from that retrieved content. If the document doesn't contain the answer, it says so honestly instead of guessing.

## How it works

1. Load the document and split it into chunks (by paragraph)
2. Embed every chunk once using Gemini's embedding model, and cache the results to disk. This caching saves new embedding evry time we retieve the same document that is already embedded. 
3. On a new run, check whether the document has changed using a hash of its content, and only recompute embeddings if something actually changed
4. Embed the incoming question the same way
5. Compare the question's embedding against every chunk using cosine similarity, computed from scratch, and rank the results
6. Hand the top matching chunks to the model with explicit instructions to answer only from that context, and to say "I don't know" if the context doesn't contain the answer

## Evaluation results

Retrieval accuracy was measured against a small set of real questions with known correct answers, at two different settings.

- Top-1 accuracy (best single match): 50%
- Top-3 accuracy (best three matches): 100%

The gap between these two numbers is the most useful finding in this project, explained below.

## What I found while testing

**A section heading can outscore real content.** One question, asking about a specific job, kept retrieving the bare "PROFESSIONAL EXPERIENCE" heading ahead of the paragraph that actually answered it. The heading shared a literal word with the question, "experience," while the real answer paragraph never repeated that word. This isn't a bug. It's a genuine limitation of similarity search: a short chunk sharing vocabulary with a question can beat a longer, correct chunk that expresses the same idea differently. Widening the search to the top three results recovered the correct answer every time, since the real answer chunk was always close behind the heading in score.

**A hardcoded evaluation index is fragile.** The evaluation set originally pointed at expected answers using a fixed chunk position, like "the correct answer is chunk 13." Editing the source document, adding a single blank line, shifted every chunk position after that point, silently pointing the evaluation at the wrong content with no warning. The fix was to check for a known piece of expected text inside the retrieved results instead of a position number. This version survives document edits and keeps reporting the true state of retrieval quality, rather than breaking quietly whenever the source document changes shape.

This also changed how I read a failing eval. A FAIL doesn't automatically mean retrieval is broken, it can just as easily mean the eval question itself is flawed, poor phrasing, or an expected phrase that doesn't actually appear anywhere in the correct chunk. Worth checking both possibilities before assuming the system is at fault.

## How to run it

Install the dependencies:

```
pip install google-genai python-dotenv
```

Create a `.env` file with your Gemini API key:

```
GOOGLE_API_KEY=your-key-here
```

Place your document as `my_document.txt` in the same folder, paragraphs separated by blank lines, then run:

```
python3 rag_pipeline.py
```

## Tech stack

Python, Google Gemini (embeddings and generation), no external RAG framework. Cosine similarity, chunking, and caching were all built from scratch rather than using a library, to understand the actual mechanics before relying on one.