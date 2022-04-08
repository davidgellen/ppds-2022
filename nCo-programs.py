"""
Lecture 7 assignment https://uim.fei.stuba.sk/i-ppds/7-cvicenie/
Author: David Gellen
License: GPL-3.0
"""


def function(id_):
    """
    Represents co-program, gets the current iteration from scheduler and prints out it's id and current iteration count
    :param id_: id to identify when printing to console
    """
    try:
        while True:
            iteration = (yield)
            print(f"function {id_}, iteration = {iteration}")
    except GeneratorExit:
        print(f"function {id_} stopping")


def scheduler(functions_, max_iterations):
    """
    Starts all the co-programs and manages them - iterates through the list and sends them the current
    iteration count for clearer console output
    :param functions_: list of co-programs
    :param max_iterations: number of iterations
    """
    for func in functions_:
        next(func)
    for i in range(1, max_iterations + 1):  # we iterate from 1 instead of 0
        for func in functions_:
            func.send(i)  # using next(func) works too but send lets us send in parameter for better output
        print()


def create_functions(n):
    """
    Creates list of n co-programs
    :param n: number of co-programs
    :return: list of co-programs
    """
    fs = []
    for i in range(n):
        fs.append(function(i))
    return fs


N = 3  # number of co-programs
M = 10  # number of iterations
functions = create_functions(N)
scheduler(functions, M)
