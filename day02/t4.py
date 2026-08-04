def average(numbers):
    if len(numbers) == 0:
        return 0
    total = sum(numbers)
    count = len(numbers)
    return total/count


print(round(average([10, 20, 30])))
print(round(average([100])))
print(round(average([])))
print(round(average([10, 15])))
