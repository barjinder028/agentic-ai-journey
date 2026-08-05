Completed the steup and got familarized with the linex commands

- set up WSL and installed ubantu and python.
- familarized with the git and linux commands. 

Day 2:

- Worked through dictionaries and functions.
- Fixed a bug where I used the whole job dictionary as a key instead of just the city name.
- Learnt that lists share references when you do b = a but numbers don't.
- fixed three separate bugs in a broken function including a case-sensitivity typo.

## Day 3 — Error handling, files, JSON

### What I covered
- try/except for handling errors without crashing the program
- Reading and writing plain text files
- JSON: converting Python data to text and back, for talking to APIs later

### try/except
- try: holds code that might fail. except ErrorName: runs only if that
  specific error happens, instead of the program crashing.
- Can group several error types in one except with parentheses:
  except (ValueError, ZeroDivisionError, TypeError): instead of three
  separate blocks doing the same thing.
- Never use a bare `except:` with no error name — it silently swallows
  errors you didn't expect, which is worse than crashing.
- Mistake I made: had except blocks that printed the error message
  instead of returning None. Function should RETURN on every path,
  not print from inside and return nothing on others — same
  print-vs-return issue as Day 2's greet() function.
- ValueError is for bad conversions like int("abc"). Passing the wrong
  type entirely (like a string into division) raises TypeError instead
  — confirmed this by actually triggering it rather than guessing.

### Files
- open("name.txt", "w") — write mode, wipes the file and starts fresh
- open("name.txt", "r") — read mode
- open("name.txt", "a") — append mode, adds to the end without wiping
- Always use `with open(...) as f:` — it closes the file automatically
  even if something goes wrong partway through
- f.write() only accepts a string. Passing anything else (a list, a
  dict) throws: TypeError: write() argument must be str, not list
- A file written by a script lands in the same folder the script runs
  from. Checked it independently with `cat filename` from the
  terminal instead of only trusting my own script's read-back.

### JSON
- import json — built into Python, no install needed
- json.dumps(data) — converts a Python list/dict into a JSON string.
  Needed before writing non-string data to a file. Memory hook:
  dumps = dump to string.
- json.loads(text) — takes a JSON string and turns it back into a
  real Python list/dict you can index into normally. Memory hook:
  loads = load from string.
- This dumps/loads pair is exactly what happens when calling an AI
  API: the request and response are both JSON text, and loads() is
  what turns the response back into usable Python data.

### Things to remember going forward
- Read the error message properly before guessing — it usually names
  the exact problem (expected type vs. actual type, undefined name,
  etc.)
- A function that computes something should RETURN it, not print it
  — let the caller decide what to do with the result. This came up
  three separate times now (greet, safe_divide, and the write/read
  file pattern).
- Repeated code across except blocks (or anywhere) is a signal to
  simplify, not just a style nitpick.

## Day 4 — First real API call, reusable function, knowledge cutoff

### What I covered
- Getting and using an API key safely
- Calling a real AI model (Gemini) from Python
- Wrapping a repeated action into a reusable function
- Why models can be confidently wrong (knowledge cutoff)
- What an "agent" actually is, as opposed to a raw model

### API keys and secrets
- API key = a password, but for code instead of a person
- Never write a key directly into a .py file, and never paste it
  anywhere public (chat, GitHub, etc.) — once it's out, treat it as
  compromised
- .env file holds secrets in KEY=value format, one per line, no
  quotes needed
- .env must be listed in .gitignore so it never gets committed
- python-dotenv package + load_dotenv() reads the .env file and
  loads it into os.environ, same as `export` does, but permanent
  across sessions instead of disappearing when the terminal closes

### The four-step shape of calling an AI model
1. Load the key (load_dotenv + os.environ)
2. Create a client (the "phone line" to the provider, logged in
   with the key)
3. Send a request (model name + the actual question/content)
4. Read the response — the real text answer is buried inside a
   bigger response object, pulled out with something like
   response.text or response.choices[0].message.content depending
   on the provider

### Real bug: rate limit (429 error)
- Got: 429 RESOURCE_EXHAUSTED, limit: 0, on gemini-2.0-flash
- Cause: free tier model availability had changed — old model name
  no longer covered, not a mistake in my code
- Fixed by switching to gemini-2.5-flash, which was actually listed
  as free tier
- Lesson: rate limits are expected behavior for any real API, not a
  bug to avoid — try/except from Day 3 exists partly for exactly
  this kind of error
- Rate limits count REQUESTS made in a time window, not whether the
  content/wording changes between calls

### Reusable ask() function
- Moved load_dotenv() and client creation OUTSIDE the function —
  only need to log in once, not once per question
- The part that changes each call (the question) becomes the
  function's parameter
- Function returns the answer as a string, doesn't print it —
  same return-vs-print rule from Day 2/3, let the caller decide
  what to do with the result

### Knowledge cutoff
- Asked the model "what year is it" — it confidently answered 2024,
  which was wrong
- This isn't a code bug. The model was trained on data up to some
  past point and has no built-in way to know anything after that,
  including today's date, unless it's told
- Important: it answered confidently and wrong, not "I don't know."
  Sounding sure and being right are not the same thing with these
  models

### Brain vs. hands — what an agent actually is
- The model I called directly = the raw model, no extra tools,
  nothing but its training data to draw on
- Gemini's chat product (gemini.google.com) = same kind of model,
  but wired up with extra tools like live web search, so it can
  check things instead of guessing
- An agent = a model (the brain) + tools it's allowed to use
  (the hands) + the judgment to decide when to use them
- The date mistake today is the exact reason agents need to exist —
  if the raw model already knew everything, nobody would need to
  build tool access around it
- Next step in the course: start building that tool access myself,
  starting with something simple like giving the model a way to
  check the real current date


## Day 5 — First real tools, connecting functions to the model

### What I covered
- Writing a plain Python function and handing it to the model as a tool
- Seeing the model use a tool correctly vs. guessing without one
- Building a second tool from scratch (add_numbers)
- Splitting tools into their own file and importing them
- Reading a function's docstring with __doc__ and help()
- Watching one request use two different tools correctly

### What a tool actually is
- A tool is just a normal Python function. Nothing AI about the
  function itself.
- You hand the function to the model using tools=[function_name],
  no parentheses, since you're not calling it, you're introducing it.
- The model decides on its own whether it needs the tool, based on
  what was asked. Nothing forces it to use one.

### The docstring matters, it's not just a comment
- The text in triple quotes under a function definition is read by
  the model to decide whether that tool is relevant to the question.
- A vague docstring means the model might not realize the tool applies.
- Confirmed this by using __doc__ and help() to view a function's
  docstring directly from code.

### Proof: with tool vs. without tool
- Asked "what is today's date" WITH get_today_date wired in:
  correct answer, real date from the system clock.
- Asked the exact same question with the tools= line removed:
  model guessed, gave a wrong date and wrong day of the week,
  stated just as confidently as when it was right.
- This is the actual point of an agent: giving a model a way to
  check something instead of only being able to guess from training.

### Type hints on tool functions
- def add_numbers(a: float, b: float) -> float:
- The hints tell the model (and anyone reading the code) exactly
  what kind of value each parameter expects and what comes back.
- Not just decoration, the model needs this to know how to call
  the function correctly.

### Splitting into separate files
- Put get_today_date and add_numbers in their own file, tools.py.
  That file does nothing on its own, just defines functions.
- In the main file: from tools import get_today_date, add_numbers
  Same idea as import os or import json, just importing from a
  file I wrote instead of a built-in one.
- Both files need to be in the same folder for a plain import like
  this to work.

### Multiple tools, one request
- Asked one question containing two separate asks: today's date,
  and 59 plus 97.
- The model quietly split this into two tool calls, one to each
  function, matched by what each part of the question actually
  needed, then merged both real answers into one written reply.
- Not one fixed tool call every time, the model works out how many
  tools it needs and which ones, fresh, based on the actual question.

### Bugs and mistakes today
- Typo running the file: typed agnet.py instead of agent.py.
  Lesson: "file not found" errors are almost always a typo, check
  with ls first before assuming something bigger is wrong.
- Used os.environ.get("KEY") instead of os.environ["KEY"]. The
  .get() version fails silently with None if the key is missing,
  square brackets crash immediately with a clear error instead.
  Square brackets are safer for something as important as an API key,
  since you want to know right away if it's missing.
- Noticed I had two different names floating around for the same
  environment variable (GOOGLE_API_KEY vs GENAI_API_KEY). Worth
  picking one name and using it everywhere, in every file.

### Big idea for today
This is the actual shift from "model that talks" to "model that
does something." A tool is nothing fancy, just a normal function
with a good description, handed to the model, and trusted to be
used only when actually needed.