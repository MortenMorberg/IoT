import matplotlib.pyplot as plt
from csv_helper import read_from_csv, write_to_csv 
import sys

# array of dict, with (x, y, x_name, y_name) as keys
def plot(xy, name, x_label, y_label):

    for x,y in xy:
        plt.plot(x,y)

    plt.plot(params['x'], params['y'])
    plt.title(name)
    plt.xlabel(x_a)
    plt.ylabel(params['y_name'])
    plt.show()

# array of dict, with (x, y, x_name, y_name) as keys
def histogram(xy, name, x_label, y_label):
    pass

if __name__ == '__main__':
    plot_type = sys.argv[1]
    
    name = 'test'
    x_label = 'x axis'
    y_label = 'y_axis'

    xy = [ read_from_csv(f) for f in sys.argv[2:] ] 

    if plot_type == '-p':
        plot(xy, name, x_label, y_label)
    elif plot_type == '-h':
        histogram(xy, name, x_label, y_label)
    else:
        print('wrong type argument given')
        sys.exit(1)

