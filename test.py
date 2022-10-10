with open("Measurement_summary.csv", "r")as f:
    for line in f:
        basket = line.strip().split(',')
        print(basket)