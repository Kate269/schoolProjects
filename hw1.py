from turtle import Turtle, done
from math import sin, sqrt, radians


def polygon_spiral(num_sides, lines, step):
    bob = Turtle()
    angle = (360/num_sides)
    for i in range(1, lines+1):
        bob.forward(step * i)
        bob.right(angle)


def house(size, roof_angle):
    bob = Turtle()
    size_house = sqrt((size*size)*2)

    def down_house():
        bob.left(45)
        bob.forward(size_house)
        bob.left(135)
        for _ in range(4):
            bob.forward(size)
            bob.left(90)

    def roof():
        roof_one_side = ((size/2) / sin(radians(roof_angle/2)))
        bob.left(-90 + roof_angle/2)
        bob.forward(roof_one_side)
        bob.left(180 - roof_angle)
        bob.forward(roof_one_side)
        bob.left(45 + roof_angle/2)
        bob.forward(size_house)
    down_house()
    roof()
    done()


def geometric_sequence(count, start, quotient):
    for _ in range(count):
        print(start, end=" ")
        start = quotient*start


def empty_triangle_right(size):
    i = 0
    j = (size-2)
    print(".", end="")  # 1)
    for row in range(size):
        for col in range(size-1):
            if row == i+1 and col == j:
                print("#", end="")
                i = i+1
                j = j-1

            if row == size-1 or col == size-2:
                print("#", end="")
            else:
                print(end=".")
        print()

def table_div(size):
    def num_of_digits(number):
        i = 0
        while(number > 0):
            i += 1
            number = number // 10
        return i
    number_digits = num_of_digits(size)
    def head_of_table():
        print(" "*(number_digits+1)+"|", end=" ")
        last_dash = 1
        for row in range(1, size+1):
            print("{0:>{1}}".format(row, number_digits), end=" ")
            last_dash += num_of_digits(size) + 1
        print()
        print("-"*(number_digits+1)+"+", end="")
        print("-" * last_dash, end="")
        print()
    def table():
        for col in range(1, size+1):
            print("{0:>{1}}".format(col, number_digits), end=" | ")
            for row in range(1, size+1):
                div = col//row
                print("{0:>{1}}".format(div, number_digits), end=" ")
            print()

    head_of_table()
    table()


def nth_unique_smallest_prime_divisor(num, index):
    start = 2
    list_of_prime_num = []
    while start * start <= num:
        if num % start:
            start += 1
        else:
            num //= start
            list_of_prime_num.append(start)
    if num > 1:
        list_of_prime_num.append(num)
    duplicate = []
    [duplicate.append(i) for i in list_of_prime_num if i not in duplicate]

    if index-1 < len(duplicate):
        print(duplicate[index-1])

"""
HW1 from school subject IB111 (Masaryk university)
"""
