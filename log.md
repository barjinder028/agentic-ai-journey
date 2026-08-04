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
