import hashlib

text1 = "The Great Wall of China is a series of fortifications."
text2 = "The Great Wall of China is a series of fortifications!"

hash1 = hashlib.sha256(text1.encode()).hexdigest()
hash2 = hashlib.sha256(text2.encode()).hexdigest()

print(hash1)
print(hash2)
print(hash1 == hash2)