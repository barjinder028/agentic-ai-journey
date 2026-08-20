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


## Day 8 — Combining tools and memory into one Agent class

### What I covered
- Merged Day 5 (tools) and Day 6 (memory) into a single Agent class,
  using what Day 7 taught about self
- Tested a conversation that needed both at once: a tool call for
  math, reasoning using a tool's result, and memory reaching back
  across several earlier messages
- Hit a real 503 error and fixed it by switching models

### The actual build
- Took Day 6's ChatBot and added self.tools = [get_today_date,
  add_numbers] in __init__, same way self.history already worked
- Added tools=self.tools into the generate_content call inside
  send(), same config pattern from Day 5, just reading from a
  stored list instead of writing it out fresh each time
- Nothing new syntactically, this was entirely about combining two
  things I already knew how to build

### Real bug: 503 error
- Different from Day 4's 429. 429 meant I'd made too many requests.
  503 means the server itself was temporarily overloaded, nothing
  to do with my account or code.
- Fixed by switching to a different, currently available model
  (gemini-3.5-flash) instead of the one that was failing

### Model versions, worth remembering
- Learned gemini-2.5-flash, the model I'd been using since Day 4,
  is scheduled to shut down in October 2026. Google has a newer
  3.x generation of models now. Not urgent to change yet, but
  something to watch and swap out before the shutdown date.

### The real test, and why it mattered
- Asked one conversation to: state a name, get today's date via a
  tool, add two numbers via a tool and reason about the result
  using a second tool's output, then recall both the name and the
  calculated sum from earlier messages
- All four answers came back correct, proving tools and memory
  were working together in one conversation, not as two separate
  demos

### Why this actually worked (the self question)
- self.tools and self.history both live on the same object,
  reachable through the same self inside send()
- If they lived in two separate, disconnected places with no
  shared self, send() would have no path to reach one of them at
  all. self.history would just throw AttributeError, same shape
  of error as the broken Person example from Day 7.
- The real lesson: everything a method needs has to be reachable
  through self, because self is the object's only real connection
  to its own stored data. This is why adding a new capability to
  an existing class is just "store it on self too", nothing more
  complicated than that once self is actually understood.

### Big picture
First real agent: memory and tools working together, built by
combining three separate days of learning rather than anything
brand new. This is genuinely the shape every agent framework does
under the hood, just with more tools and more structure around it.

## Day 9 — Manual function calling, seeing the automation for real

### What I covered
- Turned off Automatic Function Calling (AFC) on purpose, to see
  what the library has actually been doing behind tools= since
  Day 5
- Manually read a pending function call out of a response, ran the
  real Python function myself, and sent the result back by hand
- Got the exact same final answer as automatic mode gives, proving
  I'd rebuilt the real mechanism, not something different

### What tools= was actually hiding
- Every tools= call since Day 5 secretly involved at least two
  round trips to the model: one where it asks for a function, one
  where it reads the result and writes the real answer. Automatic
  Function Calling (AFC) does both invisibly in what looks like one
  call.
- Disabled it with automatic_function_calling=
  types.AutomaticFunctionCallingConfig(disable=True) in
  GenerateContentConfig

### What the response looks like with AFC off
- response.text was None, since the model hadn't actually answered
  the question yet, only asked for help
- response.function_calls held the real request instead: which
  function (name), and exactly what to call it with (args), parsed
  correctly out of a plain English question and matched onto my
  function's real parameter names

### Running it and sending the result back
- function_call.args is a dictionary, so add_numbers(**function_call.args)
  is really the same as calling add_numbers(a=59, b=97) directly,
  just built dynamically from whatever the model asked for
- types.Part.from_function_response(name=..., response={"result":
  result}) packages the real answer, labeled so the model can match
  it to its own request
- Had to include THREE things in the final call: my original
  question, the model's own function call request (pulled from
  response.candidates[0].content), and my function's response.
  The model needs to see its own request sitting in the
  conversation, not just my answer floating alone with no context.

### function_call vs function_response, the actual difference
- function_call comes FROM the model. It's a request, not an
  answer. The model can only ask for something to be run, it
  cannot run code itself.
- function_response comes FROM me. It's the real result, produced
  by code actually executing on my machine.
- This divide (model asks and reads, my code actually does things)
  is the entire reason tools exist

### Proof it worked
- Got 156 as the final answer, byte-for-byte the same result
  automatic mode gave back on Day 8, confirming I'd rebuilt the
  real mechanism by hand, not something different that just
  happened to also work

### Why this mattered
Not every provider (Groq, for example) offers the automatic version
at all, some require building this exact loop by hand every time.
Already having done it once for real means this isn't a wall
waiting for me later.

### Still open
- Duplicate chat.py / chatbot.py files sitting outside day07/day08
  folders at the repo root, need to check with ls and clean up


## Day 10 — The real agent loop, while instead of a fixed number of steps

### What I covered
- Learned while loops, and why they're different from for loops
- Built a loop that keeps calling tools until the model is actually
  done, how ever many rounds that takes
- Tested it on a question that genuinely needed two separate tool
  calls, one depending on the result of the other
- Corrected a misunderstanding about response.candidates

### while vs for
- for loops over something whose size I already know in advance
  (a list, a range)
- while keeps running as long as a condition stays true, used when
  I don't know ahead of time how many times it needs to run
- while True: with no break is a real danger, an infinite loop.
  The way out is an explicit return or break inside the loop, not a
  condition that goes false on its own

### Why one round wasn't enough today
- Question: get today's date, take the day number, add 100, tell
  me the result
- Couldn't happen in one round like Day 9. The model can't call
  add_numbers until it actually HAS a real day number, and it only
  gets that after get_today_date actually runs and returns
- This needed genuine back and forth: call one tool, get a real
  answer, use that answer to decide the next tool call, then
  finally answer in words

### The actual loop
- available_tools: a dictionary mapping a tool's NAME (as a string)
  to the real function itself, so the code can look up "which
  actual function matches what the model just asked for"
- Loop structure: ask the model, check if it's asking for a tool
  (response.function_calls), if yes run the real tool and send the
  result back, if no (empty function_calls) the model is done,
  return response.text and exit
- The exit condition is the loop's real doorway out, checked fresh
  every single time through

### Traced through what actually happened
- Round 1: model can't answer yet, asks for get_today_date, no
  args needed
- Round 2: has the real date now, works out the day number itself
  (the tool returned the whole date string, not just the day
  number, the model had to read it and pull the number out), asks
  for add_numbers with real numbers this time
- Round 3: has everything it needs, function_calls is empty, hands
  back the finished answer, loop exits
- Confirmed the model was doing real reasoning between tool calls,
  not just relaying tool output word for word

### Corrected misunderstanding: response.candidates
- Thought [0] meant "picking the highest-confidence response out of
  several the model generated automatically"
- Actually: by default Gemini only ever generates ONE candidate.
  [0] just means "the only one that exists", nothing was compared
  or ranked to get there
- There IS a real confidence-like score (avgLogprobs) the API can
  expose, but it's not used to auto-pick anything behind the
  scenes. I'd have to explicitly request multiple candidates and
  compare them myself in code if I ever wanted that

### Big picture
This while loop is the real shape every actual agent framework
runs underneath its own decoration. Not a fixed number of steps
decided in advance, just "keep going until the model says it's
actually finished."


## Day 11 — Merging memory, tools, and the loop into one real Agent

### What I covered
- Combined Day 6 (memory), Day 8 (tools), and Day 10 (the while
  loop) into a single class for the first time
- Added a hard round limit so the loop can never run forever
- Added try/except around the actual tool call, so a broken tool
  doesn't crash the whole program
- Tested memory surviving across separate calls to send(), while
  one of those calls still needed multiple internal tool-call rounds

### The two real gaps closed today
- max_rounds / rounds: while rounds < max_rounds instead of while
  True. If the model somehow never finishes, the loop stops on its
  own and returns an honest message instead of hanging forever
- try/except around the actual function call: if a tool itself
  fails, the error gets caught and sent BACK to the model as a
  normal function response, just labeled "error" instead of
  "result". The model can react to that instead of the whole
  program crashing

### What actually merged
- self.history now lives on the object (from Day 6), so it
  survives between separate calls to .send(), not just within one
- Inside send(), the same while-loop structure from Day 10 still
  runs, multiple tool rounds if needed, before finally returning
- Every round appends to self.history, not just the final answer,
  which is what let the third question later recall a number that
  was only ever produced mid-loop, in an earlier call

### Test and result
- agent.send("My name is Barji.") — established the name
- agent.send("Get today's date, take the day number, add 50.") —
  needed two full tool-call rounds internally (date, then math)
  before answering
- agent.send("What's my name, and what was that final number?") —
  correctly recalled BOTH the name and the number, even though the
  number only existed inside an earlier call's internal loop, never
  said as a standalone fact on its own

### Big picture
This is the real shape from here forward: one class holding memory,
tools, and a safe, bounded loop together. Everything after this is
adding more tools and better tool logic on top of this same base,
not rebuilding it.


## Day 12 — Embeddings, turning text into comparable meaning

### What I covered
- What an embedding is and why retrieval needs it
- Got real embeddings from Gemini's embedding model
- Built cosine similarity by hand, from scratch
- Proved that similar meaning scores higher, even with zero shared words
- Walked through the full retrieval sequence in plain words

### The actual problem this solves
- Tools solved one blind spot (things the model can check right now,
  like the date). Embeddings solve a different one: the model has
  never seen my own documents at all, and I can't just hand over a
  whole document either, most real documents are too big to fit in
  one request, and most of it would be irrelevant noise anyway
- Retrieval means finding just the relevant few paragraphs first,
  then handing only those to the model

### What an embedding actually is
- A piece of text turned into a list of numbers
- Built so that similar MEANING produces similar numbers, not
  similar spelling or shared words
- Compared this to GPS coordinates: close together in "meaning
  space" the same way two nearby cities are close on a map

### Got real embeddings
- client.models.embed_content(model="gemini-embedding-001",
  contents=..., config=EmbedContentConfig(output_dimensionality=10))
- Shrunk dimensions down to 10 just to be able to look at the raw
  numbers. Real embeddings normally have thousands of numbers,
  meant for math, not for a human to eyeball

### Cosine similarity, built by hand
- zip(a, b) pairs up matching positions from two lists at once,
  new to me today
- dot_product: multiply matching numbers together, add up the
  results
- magnitude: how "long" one embedding is on its own, using dot
  product against itself
- cosine_similarity: dot product divided by both magnitudes
  multiplied together, giving a fair score from -1 to 1 regardless
  of how large or small the raw numbers are

### Real proof
- "The cat sat on the mat" vs "A feline rested on the rug": 0.926,
  despite sharing zero real words
- "The cat sat on the mat" vs "Stock prices fell sharply today":
  0.713, noticeably lower
- This is the actual advantage over old-style keyword search. A
  document search for "car problems" would find nothing in a
  document that says "vehicle issues" using keywords, but an
  embedding search finds it immediately, since they're close in
  meaning even with totally different words

### The full retrieval sequence, in order
1. Embed every stored paragraph once, ahead of time, and keep those
   embeddings around
2. When a real question comes in, embed the question itself, fresh,
   right at that moment, same model
3. Run cosine_similarity between the question's embedding and every
   stored paragraph embedding, one at a time
4. Whichever paragraph scores highest is the relevant one
5. Hand just that paragraph, not everything, to the model as
   context to actually answer with

### Big picture
This is the real mechanism behind the document Q&A capstone coming
up. Everything from here builds on top of this: chunking real
documents, storing embeddings properly instead of just in a list,
and doing this search fast across way more than three sentences.


## Day 13 — Chunking a real document, formalizing search, and a real limitation

### What I covered
- Split a real multi-paragraph document into separate chunks
- Embedded every chunk once and stored embeddings alongside their
  original text
- Built a proper search() function, formalizing yesterday's manual
  cosine similarity comparison
- Hit two real bugs: a NameError from an unsaved file, and a typo
  crashing a dictionary lookup
- Found a genuine limitation in embedding search: high similarity
  score does not mean correct answer

### Why documents get chunked
- Embedding models have input limits, a long document might not
  even fit as one piece
- Even if it did fit, one embedding for a whole multi-topic
  document would be a blurry average, not sharp enough to match a
  specific question
- Fix: split into smaller pieces (paragraphs here) first, embed
  each one separately, so search can zero in on the right piece

### New syntax today
- document.strip().split("\n\n") splits text apart at blank lines,
  exactly where paragraphs break
- List comprehension: [p.strip() for p in ...] is a compact way of
  writing a for loop that builds a new list, same result as writing
  the full loop out, just shorter
- scored.sort(key=lambda x: x["score"], reverse=True): key= tells
  sort what to sort BY, since each item is a dictionary not a plain
  number. lambda x: x["score"] is a tiny throwaway function just
  for this one sort. reverse=True means highest score first

### Real bug 1: NameError from an unsaved file
- Pasted code into chat that looked correct, but the actual file
  on disk was missing three whole functions
- Cause: edited the file in VS Code but never actually saved before
  running it, so Python read an older version of the file than what
  was showing in the editor
- Fixed by checking directly with cat chunking.py, which showed the
  real file content, not what the editor displayed
- Lesson: when code looks right but Python disagrees, check the
  actual file on disk directly, don't argue with the editor

### Real bug 2: typo in a dictionary key
- Wrote r["scorae"] instead of r["score"] in a print statement
- Crashed with KeyError, the dictionary version of a NameError,
  same root cause as Day 5's agnet.py typo, just a different kind
  of name this time

### The real finding: similarity score is not correctness
- Asked "who climbed the tallest mountain": Mount Everest paragraph
  correctly scored highest (0.846), even though the paragraph never
  uses the word "climbed", only "summit". Real proof that meaning
  matching works, not just keyword overlap.
- Asked "which structure took centuries to build": Eiffel Tower
  scored highest (0.957), but the Great Wall paragraph is the
  factually correct answer (explicitly says construction "began
  over 2,000 years ago and continued through several dynasties").
  Eiffel Tower was completed for a single event in 1889, nothing
  about centuries.
- Nothing crashed. The code ran perfectly and still returned the
  less correct answer as the top result, because both paragraphs
  share general topic overlap (structures, dates, engineering,
  landmarks) that the embedding picks up on, without actually
  reasoning through the specific logic of "duration" in the
  question

### Big picture lesson
A high similarity score means "this is about the same general
topic," not "this correctly answers the question." Those are
different things. A real retrieval system can't blindly trust its
top result, that result is a first guess that still needs
validating, either by the model reasoning over the retrieved
context, or by some check layered on top, not something to hand
straight to a user as if it were guaranteed correct.## Day 13 — Chunking a real document, formalizing search, and a real limitation

### What I covered
- Split a real multi-paragraph document into separate chunks
- Embedded every chunk once and stored embeddings alongside their
  original text
- Built a proper search() function, formalizing yesterday's manual
  cosine similarity comparison
- Hit two real bugs: a NameError from an unsaved file, and a typo
  crashing a dictionary lookup
- Found a genuine limitation in embedding search: high similarity
  score does not mean correct answer

### Why documents get chunked
- Embedding models have input limits, a long document might not
  even fit as one piece
- Even if it did fit, one embedding for a whole multi-topic
  document would be a blurry average, not sharp enough to match a
  specific question
- Fix: split into smaller pieces (paragraphs here) first, embed
  each one separately, so search can zero in on the right piece

### New syntax today
- document.strip().split("\n\n") splits text apart at blank lines,
  exactly where paragraphs break
- List comprehension: [p.strip() for p in ...] is a compact way of
  writing a for loop that builds a new list, same result as writing
  the full loop out, just shorter
- scored.sort(key=lambda x: x["score"], reverse=True): key= tells
  sort what to sort BY, since each item is a dictionary not a plain
  number. lambda x: x["score"] is a tiny throwaway function just
  for this one sort. reverse=True means highest score first

### Real bug 1: NameError from an unsaved file
- Pasted code into chat that looked correct, but the actual file
  on disk was missing three whole functions
- Cause: edited the file in VS Code but never actually saved before
  running it, so Python read an older version of the file than what
  was showing in the editor
- Fixed by checking directly with cat chunking.py, which showed the
  real file content, not what the editor displayed
- Lesson: when code looks right but Python disagrees, check the
  actual file on disk directly, don't argue with the editor

### Real bug 2: typo in a dictionary key
- Wrote r["scorae"] instead of r["score"] in a print statement
- Crashed with KeyError, the dictionary version of a NameError,
  same root cause as Day 5's agnet.py typo, just a different kind
  of name this time

### The real finding: similarity score is not correctness
- Asked "who climbed the tallest mountain": Mount Everest paragraph
  correctly scored highest (0.846), even though the paragraph never
  uses the word "climbed", only "summit". Real proof that meaning
  matching works, not just keyword overlap.
- Asked "which structure took centuries to build": Eiffel Tower
  scored highest (0.957), but the Great Wall paragraph is the
  factually correct answer (explicitly says construction "began
  over 2,000 years ago and continued through several dynasties").
  Eiffel Tower was completed for a single event in 1889, nothing
  about centuries.
- Nothing crashed. The code ran perfectly and still returned the
  less correct answer as the top result, because both paragraphs
  share general topic overlap (structures, dates, engineering,
  landmarks) that the embedding picks up on, without actually
  reasoning through the specific logic of "duration" in the
  question

### Big picture lesson
A high similarity score means "this is about the same general
topic," not "this correctly answers the question." Those are
different things. A real retrieval system can't blindly trust its
top result, that result is a first guess that still needs
validating, either by the model reasoning over the retrieved
context, or by some check layered on top, not something to hand
straight to a user as if it were guaranteed correct.


## Day 14 — Closing the retrieval gap, a real RAG pipeline

### What I covered
- Widened search from top_n=1 to top_n=3, giving the model multiple
  candidates instead of trusting one blind result
- Wrote an explicit grounding prompt: answer only from context,
  say "I don't know" if the context doesn't contain the answer
- Tested it directly against yesterday's actual failure case
- Tested it against a question the document genuinely cannot answer

### The actual fix for yesterday's problem
- Yesterday, search handed back exactly one paragraph and there was
  no way to catch it being wrong
- Today, three candidates go to the model together, and the model
  itself, which can actually read and reason, works out which one
  (if any) really answers the question, rather than blindly trusting
  whichever one scored highest mathematically

### rag_answer(), the real RAG shape
- "\n\n".join([r["text"] for r in results]) glues the retrieved
  paragraphs into one context block, same list comprehension style
  from Day 13
- The prompt explicitly instructs: answer ONLY using the given
  context, and say "I don't know based on the given context" if the
  answer isn't actually there. Not hoping the model behaves well,
  telling it exactly what to do in both cases

### Real proof, both cases
- "Which structure took centuries to build": correctly answered
  Great Wall of China, even though Eiffel Tower still scored higher
  in the raw search (0.957 vs 0.843). The model reasoned past an
  imperfect retrieval ranking by actually reading the candidates.
- "What is the capital of Japan": correctly said it didn't know,
  based on the given context, instead of answering from its own
  general knowledge. This is Day 4's original lesson (models
  guessing confidently) actually solved this time, not just
  avoided. A model with no grounding instructions would have
  answered "Tokyo" confidently and correctly, technically right but
  defeating the entire purpose of staying grounded to a specific
  document.

### Big picture
This is a real, working RAG pipeline end to end: chunk a document,
embed the chunks, search by meaning, hand multiple candidates to
the model with explicit grounding rules, and get answers that are
either correctly reasoned from real context or honestly refused.
This is the actual mechanism the document Q&A capstone is built on,
not a simplified version of it.## Day 14 — Closing the retrieval gap, a real RAG pipeline

### What I covered
- Widened search from top_n=1 to top_n=3, giving the model multiple
  candidates instead of trusting one blind result
- Wrote an explicit grounding prompt: answer only from context,
  say "I don't know" if the context doesn't contain the answer
- Tested it directly against yesterday's actual failure case
- Tested it against a question the document genuinely cannot answer

### The actual fix for yesterday's problem
- Yesterday, search handed back exactly one paragraph and there was
  no way to catch it being wrong
- Today, three candidates go to the model together, and the model
  itself, which can actually read and reason, works out which one
  (if any) really answers the question, rather than blindly trusting
  whichever one scored highest mathematically

### rag_answer(), the real RAG shape
- "\n\n".join([r["text"] for r in results]) glues the retrieved
  paragraphs into one context block, same list comprehension style
  from Day 13
- The prompt explicitly instructs: answer ONLY using the given
  context, and say "I don't know based on the given context" if the
  answer isn't actually there. Not hoping the model behaves well,
  telling it exactly what to do in both cases

### Real proof, both cases
- "Which structure took centuries to build": correctly answered
  Great Wall of China, even though Eiffel Tower still scored higher
  in the raw search (0.957 vs 0.843). The model reasoned past an
  imperfect retrieval ranking by actually reading the candidates.
- "What is the capital of Japan": correctly said it didn't know,
  based on the given context, instead of answering from its own
  general knowledge. This is Day 4's original lesson (models
  guessing confidently) actually solved this time, not just
  avoided. A model with no grounding instructions would have
  answered "Tokyo" confidently and correctly, technically right but
  defeating the entire purpose of staying grounded to a specific
  document.

### Big picture
This is a real, working RAG pipeline end to end: chunk a document,
embed the chunks, search by meaning, hand multiple candidates to
the model with explicit grounding rules, and get answers that are
either correctly reasoned from real context or honestly refused.
This is the actual mechanism the document Q&A capstone is built on,
not a simplified version of it.


## Day 15 — Real evaluation, a hidden bug, and the actual root cause

### What I covered
- Built an evaluation set with known correct answers for each question
- Measured retrieval accuracy as a real number, top-1 and top-3
- Found the aggregate number hid two separate failures, both the same paragraph
- Tested a dimensionality hypothesis, got a result that looked
  clean but was actually wrong due to a bug in my own test
- Caught the bug on review, before committing, fixed it, and got
  the real, correct result

### Eval set and accuracy function
- eval_set: five questions, each with a known correct chunk index,
  since I wrote the document myself
- evaluate_retrieval(): runs real search() on each question, checks
  if the expected paragraph is in the results, counts correct out
  of total
- Rewrote it to print PASS/FAIL per question, with expected vs
  actual text on failures, since one aggregate percentage hid which
  questions failed and why

### First numbers, and the real bug hiding behind them
- Top-1 accuracy: 60%, two failures, both the Great Wall paragraph
  losing (once to Everest, once to Eiffel Tower)
- First attempt to test this: re-embedded the document chunks at
  full dimension (no output_dimensionality set), concluded
  compression wasn't the cause since the same 60% and same two
  failures came back
- That conclusion was wrong. search() still had
  output_dimensionality=10 hardcoded on the QUESTION side only.
  zip() in my own dot_product doesn't error on mismatched lengths,
  it just silently stops at the shorter list, so the comparison was
  quietly using only the first 10 numbers of every full chunk
  embedding, not the real ones. No crash, no warning, a fully
  plausible-looking wrong result
- Caught this on a review pass before committing, not by the code
  failing

### The real, fixed test
- Removed output_dimensionality entirely from search() too, so the
  question and the chunks are compared at the same true full
  dimension
- Result: 100% at both top-1 and top-3, every failure gone
  completely, not just reduced

### Actual root cause, corrected
- Dimensionality WAS a real part of the problem, contrary to my
  first, buggy test. Using full embeddings on both sides fixed
  every failure in this eval set on its own, no chunking change
  needed at all
- The earlier sentence-splitting experiment is still a real,
  separate, valid finding (splitting into single sentences broke
  pronoun references and made results worse), but it wasn't the fix
  for THIS particular failure. Two different real findings, worth
  keeping both, but not the same one

### Why this matters more than the fix itself
A test that runs clean and gives a plausible number can still be
silently wrong, in my own evaluation code, not just in the system
being evaluated. Reviewing the actual comparison being made, not
just trusting a clean run, is what caught this before it became a
false conclusion in a real report. This is the same discipline as
Day 2's counts bug and Day 4's wrong date, just now showing up
inside my own test harness instead of the system under test.


## Day 16 — Caching embeddings, and three real bugs on the way there

### What I covered
- Learned why recomputing embeddings on every run is wasteful, and
  fixed it with a simple cache to a JSON file
- json.dump() / json.load() do in one step what dumps()/loads() plus
  a separate write/read did before
- os.path.exists() to check whether a cache file is already there
- Hit and fixed three real, separate bugs along the way

### The actual caching logic
- get_or_create_embeddings(): if a cache file exists, load and
  return it, skip the API entirely. If not, compute fresh, save to
  the file, then return it
- json.dump(data, f) converts AND writes in one line, instead of
  json.dumps() then f.write() separately
- Confirmed it properly: fresh run said "No cache found, computing
  embeddings..." and took real time. Second run said "Loading
  cached embeddings..." and was instant, no API call

### Bug 1: curly braces instead of quotes
- Tried to write a list of paragraphs using { } around raw,
  unquoted English text
- { } means dictionary or set in Python, not "a block of text".
  Needed a list [ ] with each paragraph wrapped in " " to make it
  an actual string
- SyntaxError, invalid syntax, was Python correctly refusing to
  guess what unquoted words inside { } were supposed to mean

### Bug 2: a leftover block silently undoing a working fix
- After fixing the chunks list, an old block from a previous
  version of the file was still sitting further down: chunks = []
  followed by a loop reading a document variable that no longer
  existed
- This wiped out the good chunks list immediately, then crashed on
  the very next line trying to read a variable that was never
  defined in this file
- Lesson from Day 13 came back directly here: don't trust what you
  think you edited, check the real file with cat when something
  doesn't add up

### Bug 3: an empty cache file, a different failure than "no file"
- os.path.exists() only checks whether a file exists, not whether
  there's anything usable inside it
- An empty embeddings.json (leftover from an earlier crash) passed
  the exists() check, got handed straight to json.load(), and
  crashed with "Expecting value: line 1 column 1", JSON's way of
  saying it found literally nothing to parse
- Fixed by deleting the empty file and letting a real one get
  created fresh. A real fix for later, not done today: the cache
  check should also confirm the file actually has valid content,
  not just that it exists

### Big picture
This is a real, working cache now, but more importantly, today was
proof that reading actual error messages and checking the real file
on disk, not guessing or assuming an edit landed, is still the same
method that's worked every single day this week, just applied to a
messier, multi-bug session instead of one clean lesson.


## Day 17 — Making the cache trustworthy with a hash check

### What I covered
- Learned what a hash is and why it's the right tool for "has this
  document changed since I last saved a cache"
- Rebuilt get_or_create_embeddings to store a fingerprint alongside
  the embeddings, and check it before trusting the cache
- Hit a real NameError caused by an active line getting accidentally
  commented out
- Genuinely tested the hash logic by editing real content and
  confirming a stale cache gets correctly rejected

### What a hash actually is
- Feed it any text, get back a short, fixed-length fingerprint
- The exact same input always produces the exact same fingerprint
- Even a tiny change, one character, produces a completely
  different fingerprint. Doesn't say WHAT changed, only THAT
  something changed, which is exactly what's needed here
- hashlib.sha256(text.encode()).hexdigest(). .encode() converts
  text into the raw byte form hashing actually works on

### The real gap this closes
- Yesterday's cache only checked whether a file existed, never
  whether it still matched the current document
- Editing a paragraph, or adding a new one, would have silently
  loaded stale, wrong embeddings forever, no error, no warning
- Today: get_chunks_hash() combines all chunks into one string and
  hashes it. That hash gets saved alongside the embeddings in the
  cache file. On load, the CURRENT document's hash gets compared
  against the SAVED hash. Only a match means the cache is trusted

### cached_data.get("hash") instead of square brackets
- .get() returns None quietly if the key doesn't exist, instead of
  crashing
- Matters here because an older cache file (saved before today's
  hash logic existed) wouldn't have a "hash" key at all. .get()
  handles that safely, falls through to recomputing instead of
  crashing on a missing key

### Real bug: an active line accidentally commented out
- chunk_embeddings = get_or_create_embeddings(chunks) had a # in
  front of it, so it silently never ran at all
- Caused a NameError further down, since chunk_embeddings genuinely
  never got created
- Found it with grep -n "chunk_embeddings =" chunking4.py instead
  of scrolling and guessing, same "ask the real file directly"
  instinct from Day 13 and Day 16, just using a faster tool for it
  this time

### The actual proof today was built for
- First test after the fix: real edit made to a chunk, but cache
  still said "Loading cached embeddings...", not "Document
  changed...". Didn't assume the hash logic was broken, verified
  with grep whether the edit had actually landed in the real file
  and whether an old duplicate chunks list was silently overriding
  the edited one, same pattern as Day 16's bugs
- Once that was sorted, reran it: "Document changed, recomputing
  embeddings..." fired correctly, exactly as it should have

### Big picture
The cache is now something that could actually be trusted on a real
capstone document, not just a toy. And the debugging pattern held
again: when a result doesn't match the prediction, check what's
actually in the real file before assuming the new logic itself is
wrong.


## Day 18 — Real document, real bugs, a genuine content-level finding

### What I covered
- Pointed the full pipeline at a real document (my own resume)
  instead of practice paragraphs
- Extended eval_set to support multiple acceptable answers per
  question (expected_chunk_indices as a list, checked with any())
- Chased a real retrieval failure through several wrong guesses
  before finding the actual cause
- Found a genuine, non-bug limitation in semantic search
- Found a real fragility in my own eval design

### Multi-answer eval questions
- expected_chunk_indices: [0, 1] instead of a single index, for
  questions with more than one acceptable correct chunk
- any(text in retrieved_texts for text in expected_texts): passes
  if AT LEAST ONE acceptable answer was found. all() would be the
  stricter version, requiring every listed answer to show up

### Chasing the Amazon question failure, several wrong turns first
- First guess: the Day 15 dimensionality bug again (question
  embedded small, chunks embedded full). Checked the actual code,
  ruled out, neither side set output_dimensionality
- Second guess: a stale cache holding embeddings from an older,
  buggy version of the script. Deleted the cache, forced a fresh
  compute, same failure persisted. Ruled out.
- Real cause, found by comparing scores side by side instead of
  just PASS/FAIL: the question contained my own name ("Barjinder"),
  which strongly matched chunk 0 (name and title) and chunk 1
  (contact info), pulling them above the real answer

### Testing the name theory, and finding a second real cause
- Removed my name from the question, added a real specific detail
  from the resume (the actual date range) instead. The real Amazon
  chunk jumped up, but the chunk containing "PROFESSIONAL
  EXPERIENCE" (merged with the first job, LTIMindtree, because of
  how blank lines sat in the original file) still won, since it
  literally shares the word "experience" with the question
- Tried splitting the heading into its own separate chunk to give
  every job equal footing. Confirmed Day 17's hash correctly
  detected the real change and recomputed automatically when this
  edit was made

### The real, final finding: a heading can beat real content
- Even split into its own three-word chunk, "PROFESSIONAL
  EXPERIENCE:" still scored highest (0.67-0.684 across runs), ahead
  of the actual Amazon paragraph (0.666)
- This is not a bug. A short chunk sharing a literal word with the
  question can legitimately outscore a full, correct paragraph that
  doesn't repeat that exact word. Genuine limitation of similarity
  search, same category as Day 15's Great Wall finding, different
  specific cause
- At top_n=1 this is a real failure (50% accuracy). At top_n=3, the
  real Amazon chunk is close enough behind the top result to land
  inside the wider net and recover completely (100% accuracy), same
  safety net built on Day 14

### A second real bug, in my own eval design
- Editing the document (adding a blank line) shifted every chunk
  index after it by one. A hardcoded expected_chunk_indices that was
  correct before the edit silently pointed at the wrong chunk
  afterward, with zero warning
- The resulting FAIL had nothing to do with retrieval quality, it
  was my own eval set going stale the moment the document changed
- Real conclusion: hardcoded position numbers are fragile on any
  document that keeps changing. A sturdier design would check
  whether a distinctive piece of the expected TEXT shows up in
  results, not a position number that silently shifts. Noted as a
  real fix for next time, not solved today

### End of day state
- Ended the day with the document back in its original, unsplit
  form (heading merged with the first job), the version most of
  today's findings were diagnosed and confirmed against. The
  split-heading version was a real, useful experiment along the way
  but wasn't kept in the final file. Learned firsthand, twice, that
  the actual file on disk has to be checked directly (grep) rather
  than trusted from memory or an editor's appearance

### Big picture
Real documents are messier than four tidy practice paragraphs, and
today proved that in three genuinely different ways: a real
vocabulary-matching limitation in semantic search, a structural
accident in how the source document was formatted, and a fragility
in my own evaluation code's design. All three are worth keeping
in a capstone writeup honestly, not smoothed over into a clean
number.

## Day 19 — Fixing the eval fragility from Day 18

### What I covered
- Replaced expected_chunk_indices (fragile position numbers) with
  expected_text_contains (a real word or phrase that should appear
  in a correct answer)
- Rewrote evaluate_retrieval to check retrieved TEXT for that
  phrase, instead of comparing against a hardcoded chunk position
- Fixed a real TypeError caused by an old function call not matching
  a changed function signature
- Reran Day 18's exact breaking scenario (editing the document,
  shifting every chunk index after the edit) and confirmed the new
  eval survives it correctly

### The actual fix
- Old: expected_chunk_indices: [13], compared against chunks[13].
  Broke silently the moment an edit shifted what sat at position 13
- New: expected_text_contains: ["Amazon"], checked with
  any(phrase in combined_retrieved for phrase in ...). Doesn't care
  about position at all, only whether the real answer's content
  actually got retrieved
- evaluate_retrieval no longer needs chunks passed in at all, a
  visible sign the fragility is gone, it only depends on what
  search() actually returns now

### Real bug: function signature changed, call site didn't
- Removed chunks as a parameter from evaluate_retrieval, but the
  code calling it still passed chunks as an argument
- Produced a confusing error: "got multiple values for argument
  'top_n'", not because top_n was wrong, but because the extra
  chunks argument shifted every later argument over by one position,
  silently colliding with top_n
- Lesson: changing what a function expects means every place that
  calls it needs updating to match, or arguments land in the wrong
  slot

### The real test: recreating Day 18's exact failure
- Re-added the blank line after PROFESSIONAL EXPERIENCE, same edit
  that broke the old eval, shifting chunk count from 16 to 17 and
  moving every later index by one
- Result: Top-1 still FAILS the Amazon question, Top-3 still PASSES,
  identical numbers to before the edit
- Confirmed this is NOT the same bug returning by coincidence. With
  the new text-based check, the FAIL is real and honest: chunk 11
  (the isolated heading) doesn't contain the word "Amazon" at all,
  so top-1 correctly fails. Chunk 13 (the real Amazon paragraph)
  does contain it and gets pulled in at top-3, correctly passing.
  The eval never went stale, it just kept telling the truth,
  through a structural change that would have broken it yesterday

### Why this matters
Yesterday's FAIL and today's FAIL look identical on screen, but
mean completely different things. Yesterday's was the test itself
lying, broken by an edit unrelated to retrieval quality. Today's is
the test correctly reporting a real, known limitation (a bare
heading outscoring real content at top-1). A trustworthy eval
should survive document changes and still report the true state of
the system, not just produce numbers that happen to look the same.

### Big picture
This closes the loop from Day 18 properly. The pipeline now has
retrieval, caching that's actually trustworthy, and an evaluation
harness that won't quietly lie after the document it's testing
changes shape.


## Day 21 — First real framework: LangChain

### What I covered
- Installed langchain and langchain-google-genai
- Rebuilt Day 10's tools using LangChain's @tool decorator
- Built and ran a working agent with create_agent, in under 15 lines
- Hit and fixed a real bug: a filename shadowing an installed package
- Explained precisely what create_agent is doing internally, using my
  own Day 11 code as the reference

### Same concepts, framework's clothes
- @tool decorator wraps a plain function, same shape as every tool
  I've written since Day 5. The docstring underneath still does the
  exact same job it always did, telling the model when this tool is
  relevant, no new concept, just a new way of marking it
- tools = [get_today_date, add_numbers], a plain list, replaces the
  self.available_tools dictionary I built by hand in Day 11.
  LangChain builds that name-to-function lookup internally
- {"role": "user", "content": ...} is the same role/content shape
  I built by hand in Day 6's history list, just wrapped in a
  dictionary called "messages" instead of a list I managed myself

### Real bug: naming a file after the package I was importing
- Named my file langchain.py, then wrote "from langchain.agents
  import create_agent" inside it
- Python checks the current folder before installed packages, so it
  found my own file first and tried to import from itself:
  "'langchain' is not a package"
- Fixed by renaming to agent_test.py. General rule: never name a
  personal file the same as a package being imported, this applies
  to any package name, not just langchain

### Real test, same as Day 11's
- Asked one question needing two separate tool calls (today's date,
  then add two numbers). Got the correct final answer,
  "Today's date is August 17, 2026, and 59 plus 97 is 156," on the
  first try
- Noticed the raw response object is wrapped in extra metadata
  (signatures, internal bookkeeping) that has nothing to do with the
  actual answer, real content lives in the "text" field. Frameworks
  wrap things in more layers than my own hand-built code did

### What create_agent is actually doing (the real answer, not the
vague one)
- On every single iteration, it checks whether the model's response
  needs another tool call. If yes, it runs the tool (possibly the
  same tool again, possibly a different one) and loops back with the
  new information. If no, it returns the final answer to the user.
- This is exactly my own Day 11 while loop (rounds < max_rounds,
  checking response.function_calls each pass), just running
  invisibly. My first answer to this question was too vague ("it
  automates the cycle"), had to trace back through my own code to
  state precisely what decision gets made on each pass

### Line count comparison
- My Day 11 Agent class (with round limits and tool error handling):
  well past 50 lines
- Same real capability with create_agent: under 15 lines
- The gap is the actual value of a framework, and it's only visible
  to me now because I already know what those missing 35+ lines were
  doing, rather than treating create_agent as unexplained magic

### Big picture
Nothing conceptually new happened today. Every piece of LangChain's
agent, tool decorator, message list, the tool-call loop, is something
I already built by hand between Day 9 and Day 11. Today was about
recognizing the same mechanism wearing a framework's clothes, not
learning it for the first time.


## Day 22 — Real memory across separate conversations with thread_id

### What I covered
- Added InMemorySaver as a checkpointer to create_agent
- Learned thread_id, a label identifying one specific conversation
- Proved two separate threads on the same agent stay completely
  independent, unlike anything my own Day 11 code could do without
  real extra work

### The actual gap in my own Day 11 code
- self.history lived on one Agent object. Serving two people at once
  meant creating two separate Agent objects by hand
  (agent_1 = Agent(), agent_2 = Agent()), each managing its own
  history
- That doesn't scale to a real deployed agent serving many users at
  once. LangGraph's checkpointer solves this properly: one agent
  object, many independent conversations, identified by thread_id

### How it works
- checkpointer=InMemorySaver() gives the agent a real memory store,
  same conceptual job as self.history, but built to hold many
  separate histories at once, not just one
- thread_id, passed as {"configurable": {"thread_id": "..."}} on
  every invoke() call, tells LangGraph which conversation's history
  to load and continue
- InMemorySaver only holds memory while the program runs, same
  limitation as my own self.history always had. Real deployed
  agents use a database-backed version instead (PostgresSaver, for
  Postgres), so memory survives a restart. Not needed yet, just
  worth knowing the name for later

### The real test
- thread_1: told the agent my name, then asked for it back.
  Correctly remembered it, same as Day 6's test
- thread_2, brand new, never used before: asked for my name.
  Correctly said it didn't know, "I don't know your name yet,"
  even though thread_1 had learned it moments earlier in the same
  running script
- This is the actual proof memory is scoped to the thread, not to
  the agent or the script. Same agent, same memory store, two fully
  independent conversations

### Reading LangChain's response shape
- Every response comes back as a list holding one dictionary:
  [{'type': 'text', 'text': '...', 'extras': {...}}]
- The real content always sits at response["messages"][-1].content,
  the "extras" field is internal signature/bookkeeping data, safe
  to ignore

### Big picture
Yesterday was the same mechanism, fewer lines. Today was a genuine
new capability my own from-scratch code didn't have: one agent
serving many completely separate conversations at once, which is
exactly what a real deployed agent needs to do.


## Day 23 — Multi-agent supervisor, and switching to Azure OpenAI

### What I covered
- Built two specialized agents (date_agent, math_agent) and a
  supervisor routing between them
- Hit a hard daily quota wall on Gemini's free tier for
  gemini-3.5-flash (20 requests/day), switched providers entirely
  to my own Azure OpenAI deployment (gpt-5-mini)
- Set up keyless authentication with DefaultAzureCredential instead
  of a static API key
- Diagnosed and fixed a real bug caused by a retry wrapper hiding a
  method the supervisor needed
- Confirmed routing worked correctly across a real multi-part
  question

### The supervisor pattern
- Two specialist agents, each with a narrow tool set and a
  system_prompt explicitly telling it to refuse anything outside
  its lane
- create_supervisor([date_agent, math_agent], model=..., prompt=...)
  builds a third agent whose only job is reading a question and
  deciding which specialist should handle it
- Confirmed real routing: one question needing both specialists in
  a single turn ("today's date, and separately, 100 plus 250") got
  the correct answer from both

### Why retries hit a wall here, and the real fix
- .with_retry() doesn't add retry behavior to the model object
  directly, it wraps the model inside a different, generic object
  (RunnableRetry) that only exposes the few methods every runnable
  shares
- create_supervisor internally needs .bind_tools(), a specific
  method only the real AzureChatOpenAI object has. Once wrapped,
  that method was hidden, hence: AttributeError: 'RunnableRetry'
  object has no attribute 'bind_tools'
- Real fix: use max_retries=5 as a normal constructor argument on
  AzureChatOpenAI directly, instead of wrapping the finished object
  afterward. Keeps the actual object intact with every method it
  originally had

### Switching to Azure OpenAI, keyless
- Used DefaultAzureCredential + get_bearer_token_provider instead
  of a static API key, no secret string sitting in .env at all
- Needed az login first, so DefaultAzureCredential has a real local
  session to authenticate with, since this isn't running inside an
  Azure-hosted service with automatic managed identity
- AzureChatOpenAI takes azure_deployment, api_version,
  azure_endpoint, and azure_ad_token_provider instead of an api_key

### Raw SDK call vs. framework layer, a real distinction
- Considered using client.responses.create(...) directly (the raw
  OpenAI SDK's Responses API) inside the LangChain code
- These are two separate ways of calling the same underlying model,
  not one built on top of the other. create_agent and
  create_supervisor are built to work with LangChain model objects
  (AzureChatOpenAI), not raw SDK client calls
- The raw SDK call is what I'd write by hand, no framework, the way
  Day 4 through Day 11 worked. AzureChatOpenAI is LangChain's
  equivalent, wired so the framework functions can use it directly

### Real bug count today
1. Missing imports (tool, create_supervisor) after assembling code
   from several separate messages, same "every name needs a real
   import in this specific file" lesson from Day 21
2. Gemini daily quota exhausted (20/day on gemini-3.5-flash),
   solved by switching providers entirely, not something retry
   logic could fix
3. RunnableRetry wrapper hiding bind_tools, fixed by using
   max_retries as a constructor argument instead of wrapping

### Big picture
Genuinely hit and diagnosed three different real-world failure
modes today, on a provider I'd never touched before this session,
by reading each error for what it actually said rather than
guessing. That's the actual skill this whole program has been
building toward.


## Day 24 — Resume search as a third specialist, and a real routing bug

### What I covered
- Wrapped the RAG capstone's search into a LangChain tool
  (search_resume) and built resume_agent as a third specialist
  alongside date_agent and math_agent
- Hit and fixed a real chain of missing-function bugs while
  assembling the file from several separate pieces
- Clarified a real architecture decision: chat model on Azure
  (gpt-5-mini), embeddings kept on Gemini, two separate systems
  with separate quotas, not a leftover mistake
- Found and fixed a real, subtle bug: the supervisor silently
  answering a question itself instead of routing it to the
  specialist that actually had the answer

### Missing functions, same lesson as before, several times over
- load_document, then get_or_create_embeddings and its dependencies
  (save_embeddings, load_embeddings, get_chunks_hash, search,
  cosine_similarity), then date_agent and math_agent themselves,
  none of it carried over automatically from earlier files
- Fixed by checking the actual file directly (grep -n "^def ")
  instead of guessing which functions were missing one error at a
  time. Assembling a file from pieces of several different
  conversations means every dependency needs to be checked for
  directly, not assumed present

### Chat model vs. embedding model, a real distinction
- These are genuinely separate services with separate quotas, not
  one thing. Switching AzureChatOpenAI for chat never touched
  embeddings at all, since embed_content is a different call
  entirely
- Kept embeddings on Gemini deliberately (never actually hit that
  quota), chat on Azure. A full Azure-only setup is possible too
  (AzureOpenAIEmbeddings, a separate model deployment) but is a
  real, separate task, not something to bolt on mid-debugging

### The real bug: routing failure, not grounding failure
- Asked resume_agent-shaped questions about real resume content
  (Amazon, programming languages): both correct, grounded, real
  proof the specialist's Day 14 discipline held up inside the
  framework
- Asked a question the resume doesn't cover ("favorite food"): got
  "I don't have any information about who Barjinder is", even
  though the SAME script had just correctly discussed Barjinder's
  real work history moments earlier
- Diagnosed by printing the full message trace
  (type, name, content for every message), not by guessing from the
  final answer's tone. This showed the response came from
  "supervisor" directly, not "resume_agent" at all: the question
  never reached the specialist in the first place
- Root cause: the supervisor's prompt described what each
  specialist covers by topic, but never said what to do with a
  question that doesn't obviously match any topic by name. It
  silently judged the question unrelated to "resume" and answered
  it itself, with no tools and no context

### The fix
- Made the supervisor's routing instruction explicit: any question
  mentioning Barjinder should go to resume_agent, even if the
  supervisor doesn't personally know the answer, and it should never
  answer directly if a specialist might have relevant information
- Reran the same food question and the same trace afterward.
  Confirmed a full six-message round trip this time: supervisor
  hands off (transfer_to_resume_agent), resume_agent correctly says
  it doesn't know, hands back (transfer_back_to_supervisor),
  supervisor relays the honest answer rather than overriding it

### Big picture
This is a genuinely different failure mode than anything hit before
in this project: not a tool failing, not a specialist guessing, but
the routing layer itself silently deciding a question wasn't worth
handing off. Multi-agent systems add exactly this kind of new
failure surface on top of everything a single agent can already get
wrong, and the fix has to happen at the level where the decision
was actually made, not by patching the specialist that never even
ran.

## Day 25 — A real evaluation harness for routing, not just answers

### What I covered
- Built a reusable function to identify which specialist actually
  answered a question, by reading the message trace
- Built a routing-specific evaluation set and harness, same shape
  as Day 15 and Day 19's retrieval evals, but testing a different
  layer of the system
- Deliberately included yesterday's exact bug as a regression test
- Ran it and confirmed 100% routing accuracy across all five cases

### Why this needed its own eval, separate from retrieval
- Yesterday's bug wasn't in resume_agent's grounding, it was in
  whether the question ever reached resume_agent at all. Testing
  specialists individually (already proven solid) says nothing
  about whether the supervisor is routing questions to them
  correctly in the first place
- Needed a test aimed specifically at the routing decision, not the
  final answer's content

### get_routed_agent(), the reusable version of yesterday's manual trace
- Loops through response["messages"], same as the manual print from
  Day 24, and returns the name of the first real specialist that
  shows up
- Returns "supervisor" if no specialist ever appears, exactly what
  would have flagged yesterday's bug immediately and automatically,
  instead of relying on noticing the wording of an answer sounded
  off

### The eval set, including a deliberate regression test
- Five questions, each with a known correct specialist
  (expected_agent)
- Included the exact "What is Barjinder's favorite food?" question
  that broke routing on Day 24, on purpose. This turns a bug I
  already found and fixed into something that gets automatically
  re-checked every time this eval runs, rather than something that
  could quietly break again unnoticed

### Result
- 100% routing accuracy, all five questions correctly routed,
  including the regression case
- Confirms the Day 24 supervisor prompt fix is a real, checkable
  property of the system now, not just something that happened to
  work the one time I retested it by hand

### Honest limit of this eval
- Five hand-picked, fairly clear-cut questions. Doesn't test harder
  cases: a question that plausibly touches two specialists at once,
  or ambiguous phrasing where reasonable routing could go either
  way. A real scope limit, not a claim the router is bulletproof

### Big picture
Same evaluation discipline from Day 15 and Day 19, applied to a
new layer of the system. Retrieval accuracy, grounding, and now
routing accuracy are all separately measured and separately
regression-tested, rather than trusting the system just because a
few manual test questions happened to look right.


## Day 26 — Real cost visibility, per question

### What I covered
- Learned that every model response carries its own usage_metadata,
  token counts, automatically
- Built get_total_usage(), summing token counts across every
  message in a multi-agent response, not just the last one
- Built a real cost calculator from per-token pricing
- Ran it against the Day 25 eval set and found a real, explainable
  cost pattern

### Why summing matters
- A single app.invoke() on the supervisor can trigger several
  separate model calls under the hood (supervisor decides,
  specialist runs, supervisor relays), same trace structure from
  Day 24/25
- Each of those calls has its own separate usage_metadata. Looking
  only at the final message would undercount the real cost of the
  whole question

### Real numbers from the eval set
- Date question: 876+322 tokens, $0.000863
- Math question: 874+166 tokens, $0.000550
- Amazon question (resume_agent, real retrieved context): 1191+680
  tokens, $0.001658
- Food question (resume_agent, honest refusal, no real context to
  relay): 985+427 tokens, $0.001100
- Languages question (resume_agent, real retrieved context):
  1036+388 tokens, $0.001035

### The real finding
- Questions that route to resume_agent cost roughly double the
  date/math questions, confirms the prediction: more agents
  involved means more total tokens
- But cost isn't just about HOW MANY agents get involved. The food
  question also reached resume_agent but cost less than Amazon or
  languages, because the answer was a short refusal with no
  retrieved context to relay, while Amazon and languages carried
  several hundred words of real resume text in the prompt
- Real, useful distinction: routing overhead (deciding who answers)
  and context volume (how much retrieved text gets relayed) are two
  separate cost drivers, not one

### Pricing honesty
- Found genuinely conflicting numbers for gpt-5-mini pricing across
  different sources while researching this, some roughly double
  others, likely reflecting pricing changes over time
- Used placeholder constants (INPUT_COST_PER_MILLION,
  OUTPUT_COST_PER_MILLION) instead of hardcoding a number I wasn't
  fully confident in, with a note to verify against Azure's actual
  current pricing page for the real deployment before trusting the
  dollar figures for anything beyond relative comparison

### Big picture
This is the actual "agent that costs ₹40 a call is a failed agent"
lesson from Day 1, made concrete and measurable for the first time.
Cost per question is now something I can report a real number for,
and explain what drives it, not just something I vaguely know
exists.

## Day 27 — Making cost and latency permanent

- Today was about making yesterday's cost numbers permanent instead of throwaway. Everything from Day 26 printed to the terminal and vanished the moment the script ended, which is fine for a one-off test and useless for anything you'd want to look back on later. So I built a trace log: every call to the supervisor now appends one line to a file called `trace_log.jsonl`, recording the question, which agent handled it, the token counts, the cost, and how long the whole thing took.

- The format matters more than it looks. JSONL means one complete JSON object per line, not one giant array. That's the difference between appending a single line to the end of a file and rewriting the entire file every time you add something, the same wasteful pattern I avoided back on Day 17 with the embeddings cache. Cheap to write, and you can read it one line at a time without loading the whole thing into memory.

- Building it turned up the usual kind of bug. I'd copied fifteen of the sixteen functions this needed into the new file and missed exactly one, `get_total_usage`, the very function `traced_invoke` calls first. Found it fast with `grep -n "^def "`, comparing what the file actually had against what the code was asking for, rather than guessing line by line.

- Once it ran, two things stood out. First, I ran the script twice, and the analysis correctly reported six calls to `resume_agent` instead of three, because append mode means every past run stays in the file. That's not a side effect, that's the whole point working exactly as intended.

- Second, and more interesting: I predicted `resume_agent`'s average latency would land somewhere between `date_agent` and `math_agent`, since one of its three questions gets a short, fast refusal that should pull the average down. The real numbers said otherwise. `date_agent` averaged 14.09 seconds, `resume_agent` averaged 13.93, essentially tied. My reasoning wasn't wrong, exactly, it just wasn't the whole picture. `math_agent`, doing the least real work of the three, still beat both by several seconds.

- Digging into why, both `date_agent` and `math_agent` make exactly two calls to Azure per question, the supervisor deciding, then the specialist answering. `resume_agent` adds a third real network call in between, embedding the question through Gemini before it can even search. That extra hop should have made it noticeably slower. It barely moved the number. Which points at something worth remembering: the fixed cost of just reaching the model provider and getting anything back seems to dominate total latency far more than how much actual work happens once you're there. If that holds up, the way to make this system faster isn't to speed up what any single agent does internally, it's to cut the number of separate round trips a question needs in the first place.