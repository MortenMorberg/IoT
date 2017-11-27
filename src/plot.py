import matplotlib.pyplot as plt


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
    x = [1,2,3,4,5,6,7,8,9]
    y = [5,3,8,3,9,5,7,2,4]
    param = {'x' : x, 'y' : y, 'x_name' : 'this is x name', 'y_name' : 'this is y name'}
    plot(param, 'test')
