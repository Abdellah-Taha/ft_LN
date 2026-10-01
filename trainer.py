import json
import sys
from typing import List


def read_data(path):
    data: List[tuple[int]] = []
    with open(path, "r") as f:
        i = 0
        for line in f:
            line = line.strip('\n')
            if i == 0:
                i+=1
                continue
            line = line.split(',')
            data.append((int(line[0]), int(line[1])))
            i+=1
    max_m = max(data[i][0] for i in range(len(data)))
    min_m = min(data[i][0] for i in range(len(data)))
    scalled_data = [0] * len(data)
    for i in range(len(data)):
        scalled_data[i] = (data[i][0] - min_m) / (max_m - min_m)
    return data, scalled_data, min_m, max_m

def estimate_price(mileage, theta0=0, theta1=0):
    return theta0 * mileage + theta1

learning_rate = 0.05

def train(data, scalled_data):
    theta0, theta1 = 0, 0
    m = len(data)
    for iter in range(1000):
        errors_t0 = [estimate_price(scalled_data[i], theta1, theta0) - data[i][1] for i in range(m)]
        errors_t1 = [(estimate_price(scalled_data[i], theta1, theta0) - data[i][1]) * scalled_data[i] for i in range(m)]
        step0 = (learning_rate/m) * sum(errors_t0)
        step1 = (learning_rate/m) * sum(errors_t1)
        theta0 -= step0
        theta1 -= step1
        # if iter % 100 == 0:
            # print(teta0, teta1)
    return theta0, theta1 

def main():
    data, scalled_data, min_m, max_m = read_data("data.csv")
    teta0, teta1 = train(data, scalled_data)
    a = teta1/(max_m - min_m)
    b = teta0 - (teta1 * min_m)/(max_m - min_m)
    mileage = int(input("Mileage: "))
    price = estimate_price(mileage, a, b)
    print(price)
    
if __name__ == "__main__":
    main()
