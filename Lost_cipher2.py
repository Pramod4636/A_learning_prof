def fibonacci(n):
    fibs = [0, 1]
    while len(fibs) <= n:
        fibs.append(fibs[-1] + fibs[-2])
    return fibs[:n+1]

def shift_char(c, shift):
    if c.isupper():
        base = ord('A')
    elif c.islower():
        base = ord('a')
    else:
        return c  # Keep punctuation/symbols unchanged
    return chr((ord(c) - base + shift) % 26 + base)

def encode_fibonacci_cipher(text):
    fib_seq = fibonacci(len(text))
    encoded = ""
    for i, char in enumerate(text):
        encoded += shift_char(char, fib_seq[i])
    return encoded

# Test Examples
examples = [
    "HELLO",
    "abcxyz",
    "Graduate",
    "SuperCoolChallenge",
]

for word in examples:
    print(f"{word} → {encode_fibonacci_cipher(word)}")
