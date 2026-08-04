jobs = [
    {"title": "Data Analyst", "city": "Pune", "salary": 800000},
    {"title": "AI Engineer", "city": "Bangalore", "salary": 1800000},
    {"title": "QA Lead", "city": "Pune", "salary": 1200000},
    {"title": "ML Engineer", "city": "Bangalore", "salary": 2200000},
]
counts = {}


for j in jobs:
    if j["salary"] > 1000000:
        print(j["title"], j["salary"], j["city"])

for j in jobs:
    city = j["city"]
    if city in counts:
        counts[city] = counts[city] + 1
    else:
        counts[city] = 1

print(counts)


