import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        dataset = sys.argv[1]
    else:
        dataset = 'mnist'
    with open(dataset + 'central.txt', 'r') as f:
        record = [ float(l.strip('\n'))/100 for l in f]

    best = max(record)
    print(best)