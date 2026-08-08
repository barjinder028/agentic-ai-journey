def dot_product(a, b):                                                  #defines a function that takes two vectors a and b as input and returns their dot product
    total = 0
    for x, y in zip(a, b):                                              #iterates over the elements of the two vectors a and b simultaneously using the zip function
        total += x * y
    return total

def magnitude(v):                                                       #defines a function that takes a vector v as input and returns its magnitude (length)
    return dot_product(v, v) ** 0.5

def cosine_similarity(a, b):                                            #defines a function that takes two vectors a and b as input and returns their cosine similarity
    return dot_product(a, b) / (magnitude(a) * magnitude(b))


cat = [-0.022607181, 0.015246871, 0.001684601, -0.0769077, 0.0045841224, 0.004410481, 0.002776919, 0.011506936, 0.005208321, 0.019448007]
feline = [-0.02797855, 0.02481298, -0.016868742, -0.08025024, -0.002099059, -0.0050075497, 0.021626232, 0.019801918, -0.004602447, 0.0064060204]
stocks = [0.015420642, 0.014837707, -0.016661834, -0.06344831, -0.009507145, 0.027634429, -0.008880608, -0.014410841, -0.017238302, 0.024441158]

print("cat vs feline:", cosine_similarity(cat, feline))                 #prints the cosine similarity between the vectors cat and feline
print("cat vs stocks:", cosine_similarity(cat, stocks))                 #prints the cosine similarity between the vectors cat and stocks