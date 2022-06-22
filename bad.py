import os  # For sending clear screen command
from time import sleep  # For having some delay between rounds

""" Well, what do we have here? The code does EXACTLY the same thing as the code in "good.py",
but this one is way shorter and clearer. Why's that? The main reason is of course because this
is just a simple example of Object Oriented Design - take a simple program, convert it to OOD
and show the important issues. But in addition, it is obvious that this small piece of software
is extremely dedicated to its operation. It does exactly what it was designed for, and any
change to the original design will be painful. On the other hand, the OOD example of course
took more time to construct, but it offers both great flexibility and one of the most important
aspects in software engineering, which is code reuse. This means you can take classes written
for that project and combine them in other programs that may need similar operation with minimal
changes. Hurray!"""

x, y, dx, dy, max_x, max_y = 3, 1, 1, 1, 13, 10

while True:
    os.system('cls')
    for i in range(max_y):
        for j in range(max_x):
            if (j, i) == (x, y):
                print("O ", end="")
            else:
                print("· ", end="")
        print()
    if x + dx < 0 or x + dx >= max_x:
        dx = -dx
    if y + dy < 0 or y + dy >= max_y:
        dy = -dy
    x += dx
    y += dy
    sleep(0.5)
