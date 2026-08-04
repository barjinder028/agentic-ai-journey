import json

jobs = [
    {"title": "Data Analyst", "city": "Pune", "salary": 800000},
    {"title": "AI Engineer", "city": "Bangalore", "salary": 1800000},
    {"title": "QA Lead", "city": "Pune", "salary": 1200000},
    {"title": "ML Engineer", "city": "Bangalore", "salary": 2200000},
]

with open("json.json", "w") as f:
    f.write(json.dumps(jobs))

with open("json.json", "r") as f:
    content = f.read()

jobs_again = json.loads(content)
print(jobs_again[1]["title"])


