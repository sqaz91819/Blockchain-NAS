if __name__ == "__main__":
    with open('central.txt', 'r') as f:
        record = [ float(l.strip('\n'))/100 for l in f]

    best = max(record)
    print(best)