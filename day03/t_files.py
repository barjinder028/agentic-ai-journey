titles= ["Data Analyst", "AI Engineer" , "QA Lead"]

with open("job_titles.txt", "w") as f:
    for title in titles:
        f.write(title + "\n")

with open("job_titles.txt", "r") as f:
    contents = f.read()
    print(contents)

