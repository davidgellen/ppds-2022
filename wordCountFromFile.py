def cat(f, next_fnc):
    for line in f:
        next_fnc.send(line)
    next_fnc.close()


def grep(substring, next_fnc):
    try:
        while True:
            line = (yield)
            next_fnc.send(line.count(substring))
    except GeneratorExit:
        next_fnc.close()


def wc(substring):
    n = 0
    try:
        while True:
            n += (yield)
    except GeneratorExit:
        print(substring, n, flush=True)


def dispatch(greps):
    try:
        while True:
            line = (yield)
            for grep in greps:
                grep.send(line)
    except GeneratorExit:
        for grep in greps:
            grep.close()


if __name__ == "__main__":
    f = open("test_file", "r")
    substrings = ["hello"]
    greps = []

    for substring in substrings:
        w = wc(substring)
        next(w)
        g = grep(substring, w)
        next(g)
        greps.append(g)

    d = dispatch(greps)
    next(d)
    cat(f, d)
