# Assignment 7 
Create an application, that will utilize N (N>2) co-programs (using generators) and switching their routines using custom scheduler.
The implementation is based on lecture https://www.youtube.com/watch?v=kAcKWM4qR6o by Mgr. Ing. Matúš Jókay, PhD. and from website https://uim.fei.stuba.sk/i-ppds/7-cvicenie/.

### Co-program's functionality:
```
def function(id_):
    try:
        while True:
            iteration = (yield)
            print(f"function {id_}, iteration = {iteration}")
    except GeneratorExit:
        print(f"function {id_} stopping")
```
The co-program basically just prints its id iteration count from scheduler.

### Scheduler's functionality:
```
def scheduler(functions_, max_iterations):
    for func in functions_:
        next(func)
    for i in range(1, max_iterations + 1):  # we iterate from 1 instead of 0
        for func in functions_:
            func.send(i)  # using next(func) works too but send lets us send in parameter for better output
        print()
```
Scheduler starts all the co-programs and then runs for __max_iterations__ starting on index 1 for clarity.
Each iteration iterates through all the functions, lets them print out to console and return the flow of the programme to scheduler.
Note how we used func.send(i) instead of next(func). By using send, we are able to pass additional arguments and make the console output easier to read.
The program of course will work using next() too.

The argument __functions__ is just a list of co-programs.

```
def create_functions(n):
    fs = []
    for i in range(n):
        fs.append(function(i))
    return fs
```

The whole program is the put together like so.

```
N = 3  # number of co-programs
M = 10  # number of iterations
functions = create_functions(N)
scheduler(functions, M)
```

file: nCo-programs.py