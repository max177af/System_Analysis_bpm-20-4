import numpy as np
from io import StringIO

def task(csv_string):
    csv_data = StringIO(csv_string)
    data = np.genfromtxt(csv_data, delimiter=',', dtype=float)
    n = len(data)-1
    total_entropy = 0

    for i in range(len(data)):
        row_entropy = 0
        for j in range(len(data[i])):
            if not data[i][j]:
                continue
            row_entropy += data[i][j] /n * np.log2(data[i][j] / n)
        total_entropy += -row_entropy

    return total_entropy



if __name__ == '__main__':
    path = 'task3.csv'
    with open(path, 'r') as file:
        reader_csv = file.read()
        task(reader_csv)
