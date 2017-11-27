import matplotlib.pyplot as plt
from csv import read_from_csv, write_to_csv 
import sys

# array of dict, with (x, y, x_name, y_name) as keys
def plot(params, name):
    plt.plot(params['x'], params['y'])
    plt.title(name)
    plt.xlabel(params['x_name'])
    plt.ylabel(params['y_name'])
    plt.show()

# array of dict, with (x, y, x_name, y_name) as keys
def histogram(params, name):
    pass

if __name__ == '__main__':
    plot_type = sys.argv[1]
    if plot_type == '-p':
        pass
    elif plot_type == '-h':
        pass
    else:
        print('wrong type argument given')
        sys.exit(1)
    pass
