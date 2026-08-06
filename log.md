## Day 1 — Environment setup

### What I covered
- Got WSL2 with Ubuntu working on Windows
- Installed Python, pip, git
- Set up Git identity and SSH keys properly, linked to GitHub
- Created the agentic-ai-journey repo and made the first commit
- Learned what a virtual environment actually does, by comparing
  package lists inside and outside one

### Terminal, bash, PowerShell
- A terminal is just typing commands instead of clicking through
  folders. Same computer, same files, typed instead of clicked.
- PowerShell is Windows' own shell. Bash is the shell Linux and
  Mac use. Same kind of job, different vocabulary.
- Most tutorials and tools assume bash, since most servers run
  Linux. WSL gives a real Ubuntu Linux inside Windows so I can
  follow bash instructions directly instead of translating them.

### Locked myself out, recovered without losing anything
- Forgot my Ubuntu password partway through setup
- Fixed it by logging in as root (wsl -d Ubuntu -u root), which
  skips the password check, then used passwd to set a new one
- Lesson: almost nothing on a dev machine is unrecoverable, the
  right move when stuck is to look for the actual recovery path,
  not panic

### Git identity and GitHub
- user.name is just the label shown on commits, cosmetic
- user.email is what GitHub actually uses to match commits to my
  account. Has to be an address registered on the account or
  commits won't link to my profile properly.
- Used GitHub's private noreply email address instead of my real
  one, since public repos expose the commit email to anyone,
  including scrapers. Commits still count toward my profile, but
  my real inbox stays out of it.
- Set up an SSH key (ssh-keygen) and added the public half to
  GitHub, so I can push without typing a password every time

### Virtual environments (venv)
- Every project can build up its own pile of installed packages,
  and two projects can need different versions of the same
  package. Without separation, installing one can break the other.
- python3 -m venv .venv creates an isolated folder just for this
  project's packages
- source .venv/bin/activate turns it on for the current terminal,
  shown by (.venv) appearing at the start of the prompt
- Proved this to myself: ran pip list with the venv active, then
  deactivated and ran it again. Completely different lists. The
  venv's requests version was newer than the system one, proving
  they really are separate.
- .venv never goes into Git, added it to .gitignore since it's
  huge and easily rebuilt by anyone who clones the repo

### Things to remember
- Ubuntu refuses plain pip install outside a venv on purpose
  (externally managed environment error), it's protecting its own
  Python. The fix is always: activate the venv first.
- git status before git add, every time, to actually see what's
  about to be committed rather than assuming

## Day 2 — Python fundamentals, placement test

### What I covered
- Placement test across variables, loops, dictionaries, functions,
  mutability, and debugging
- Turned out I already knew more than I thought (input, f-strings,
  loops, conditionals), so this day was about filling the real gaps

### Real bug found: off-by-one in range()
- range(1, 100) stops at 99, never reaches 100, since range()
  includes the start but excludes the end
- The bug didn't show up in the output because 100 isn't divisible
  by 3 anyway, so it looked correct by accident
- Lesson: correct-looking output doesn't prove correct code

### Dictionaries
- A list holds things by position, a dictionary holds things by
  name (key). job["title"] reaches in by label instead of by index.
- Looping over a list of dictionaries gives one dictionary per turn
- Built a counting pattern: start an empty dict, for each item
  check "have I seen this key before" (if key in counts), add 1 if
  yes, start at 1 if no
- Real bug I hit: used the whole dictionary as the key instead of
  just the city name (counts[j] instead of counts[city]).
  TypeError: unhashable type, because dictionaries can be changed
  after the fact so they can't be used as keys, only fixed values
  like strings and numbers can.
- Second bug in the same exercise: had print(counts) BEFORE the
  loop that fills it, so it printed an empty dict. Order matters,
  a variable holds whatever was in it at the moment you look, not
  what will be there later.

### Functions
- def starts it, parameters are placeholders for whatever gets
  passed in, return sends a value back to whoever called it
- return is not print. print shows something and throws it away.
  return hands the value back so the caller can store it, use it,
  or pass it along.
- Wrote average() with a guard at the very top (if len == 0: return
  0) to avoid crashing on an empty list. The check has to come
  BEFORE the division, since Python runs top to bottom and a crash
  stops everything below it from ever running.

### Mutability (lists vs numbers)
- b = a does not copy a list, it points a second name at the exact
  same list. Changing it through b changes what a sees too, since
  there's only ever one list.
- y = x with numbers looks the same but isn't. Numbers can't be
  changed in place, only replaced. y = y + 1 makes a brand new
  number and re-points y at it, x still points at the original,
  untouched.
- The real rule: = never copies data, it just points a name at
  something. Whether that something can be edited in place
  (mutable, like lists) or only replaced (immutable, like numbers)
  determines whether a second name sees the change.

### Debugging exercise (fixed a broken function)
- Missing colon after def greet(names) — every compound statement
  needs one (def, for, if, while, class), not just functions
- Used the wrong loop variable name inside the loop (name instead
  of n), which is just a plain typo, not something deep
- Result vs result — Python is case sensitive everywhere, always.
  These are two completely unrelated names as far as Python cares.
- Deeper issue in the same function, not an error but a design
  smell: it printed the greetings from inside itself and returned
  a hardcoded "done" string that had nothing to do with the actual
  work. Fixed by collecting results into a list and returning that
  list instead, letting the caller decide what to do with it.

### Things to remember
- A function that computes something should return it, not print
  it, so the caller decides what happens next
- Read error messages properly before guessing, they usually name
  the exact problem and where it is

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

## Day 6 — Conversation history, why models have no built-in memory

### What I covered
- Proved a raw model call has zero memory between calls, tested it directly
- Learned that "memory" in any chat app is really the full conversation
  being resent every time, not the model remembering anything itself
- Built a history list manually, appending both my messages and the
  model's replies
- Used a ChatBot class as a working tool, full understanding of
  class/self pushed to Day 7 on purpose

### The real proof
- Asked "what is my name" with no history sent: model had no idea
- Asked the same question after sending full history back: correct
  answer
- Same model, same question, only difference was whether past
  messages were included in the request

### Why both roles matter
- A list of messages with no reply lines in between doesn't read as
  a real conversation, it reads as disconnected notes
- The "model" role entries aren't just labels for me, they're what
  makes the whole thing legible as an actual back-and-forth
- Removing them wouldn't delete my name from history, but it would
  break the shape of the conversation enough that a memory-dependent
  question wouldn't work properly

### Where history actually lives
- self.history is a plain Python list, sitting only in memory while
  the script runs
- Closing the script or terminal wipes it completely, nothing is
  saved anywhere permanent
- Same pattern as Day 3's json.dumps/json.loads could be used to
  save history to a file and reload it later, not built today, just
  noted as a natural next step

### Open question, unresolved, follow up on Day 7
- Used "role": "assistant" instead of "role": "model" by mistake,
  expected it to error, it didn't crash. Never confirmed whether the
  memory-dependent third answer was actually correct under the wrong
  role name, or just didn't fail visibly. Check this properly once
  class/self is solid.

### Class and self
- Deliberately not covering this properly today, pushed to Day 7 on
  purpose rather than half-learning it mixed into another topic


## Day 7 — class and self, properly this time

### What I covered
- What class and self actually are, from scratch, not glossed over
- Built Person and BankAccount classes by hand
- Found and fixed a real bug in my own withdraw method, more than once
- Closed an open question from Day 6 about role names

### The core idea, in plain words
- A function forgets everything the moment it finishes running.
  A class lets you bundle data together with functions (methods)
  so the data survives between calls.
- Every method automatically receives the object itself as an
  invisible first argument, every time it's called. self is just
  the name I choose to catch that argument with, in the method's
  own definition.
- __init__ runs once, automatically, the moment a new object is
  created (Person("Barji", 30) triggers it immediately).

### self.name vs plain name, the actual difference
- self.name = name attaches the value permanently to the object.
  It survives after the method ends.
- name = name (no self) creates an ordinary local variable that
  gets thrown away the instant the method finishes, same as any
  variable in any regular function.
- Tested this directly: removing self from __init__'s parameters
  entirely causes a real error (too many arguments), because
  Python always passes the object in first whether or not the
  method is written to catch it.
- Tested it again a different way: self.balance = self.balance +
  amount vs balance = self.balance + amount. Second version reads
  the correct value but saves it into a variable that vanishes,
  so the object's real balance never actually changes. No crash,
  no warning, just silently wrong. Confirmed this by running it
  and getting 1000 instead of 1500.

### BankAccount, and the bug I actually walked into
- Built deposit, withdraw, get_balance
- withdraw first version: checked balance correctly with an if,
  but only PRINTED "insufficient funds" on failure and returned
  nothing at all in the success case. Same return-vs-print mistake
  from Day 2's greet function, showing up again in new clothes.
- Fixed it to return real values, but got the MEANING backwards
  first: returned True from the failure branch by mistake. This
  ran with no errors and confidently reported "It worked!" for a
  withdrawal that had actually been refused. Caught this by
  checking the account balance afterward and noticing it hadn't
  actually decreased.
- Real fix: return True only when money genuinely leaves the
  account (inside the successful branch), return False only when
  the withdrawal is refused (inside the else branch). Verified
  with two calls in sequence and checked both the return value AND
  the balance after each one.

### Big lesson from today
A method that can succeed or fail should return something the
CALLER can check (True/False, or similar), not just print a
message for a human to read. And matching the right TYPE of
return value isn't enough, the MEANING has to be correct too,
returning the right kind of value (True/False) in the wrong branch
is just as broken as not returning anything at all, and it's
harder to catch because nothing errors, it just quietly lies.

### Closed from Day 6
- Tested "role": "assistant" again deliberately. It didn't crash
  and gave a correct answer this time too, but decided not to trust
  that, since it's not Gemini's documented role name ("user" and
  "model" are). Reverted ChatBot back to "model" properly. Lesson:
  something not erroring once isn't the same as it being correct
  or safe to rely on.