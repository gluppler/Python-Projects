#!/usr/bin/env python3

greeting = "Hello World!"

print(greeting)

a = 'HTB'
b = "Academy"

print(a, b)

advice = "Don't panic" #This is a string
advice2 = 'This too'

ultimate_answer = 42 #This is an integer
potential_question = 6 * 7 #This too

confident = True #This is a boolean
something_false = False #This is also a boolean
problems = None #This is null

# This is a comment

add = 10 + 10 #Addition

sub = 20 - 10 #Subtraction

multi = 5 * 5 #Multiplication

div = 10 / 5 #Division

print(add, sub, multi, div)

result = (add * sub) - (multi * div) #(20 * 10) - (25 * 2)

print('Result: ', result)

# If-Elif-Else Statement
happy = 2

if happy == 1:
    print("Happy and we know it!")
elif happy == 2:
    print("Excited about it!")
else:
    print("Not happy...")

# While Loop
counter = 0

while counter < 5:
    print(f'Hello #{counter}')
    counter = counter + 1

# Format Strings
equation = f'The meaning of life might be {6 * 7}.'  # -> The meaning of life might be 42.

me = 'Birb'
greeting = f'Hello {me}!'  # -> Hello Birb!

# For-Each Loop
groceries = ['Walnuts', 'Grapes', 'Bird seeds']

for food in groceries:
    print(f'I bought some {food} today.')

# CodeBlock
list_3 = ['Accidental', '4daa7fe9', 'eM131Me', 'Y!.90']
secret = []

for x in list_3:
    secret.append(x[:2])

print(''.join(secret))

# CodeBlock2
list_2 = [4, 3, 2, 1]

for num in list_2:
    print(num)
