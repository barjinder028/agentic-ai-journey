def greet(names):
    greetings = [] 
    for n in names:
        greetings.append("hello " + n)
    return greetings

people = ["asha", "ravi", "meera"]
result = greet(people)
print(result)


