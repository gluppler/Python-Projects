def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

# Get input from the user
n = int(input("Enter the value of n: "))

# Print the Fibonacci number at the nth position
print(f"The {n}th Fibonacci number is: {fibonacci(n)}")

