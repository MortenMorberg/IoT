import pandas as pd

def write_to_csv(x, y, fileName, name):

    toCSV = ['{0}, {1}\n'.format(x, y) for x,y in zip(x,y)]
    with open('{0}.csv'.format(fileName), 'w') as csv_file:
            csv_file.write(name + '\n')
            csv_file.write(''.join(toCSV))

def read_from_csv(fileName):
    with open('{0}.csv'.format(fileName), 'r') as csv_file:
        name = csv_file.readline()
    print(name)
    dataframe = pd.read_csv('{0}.csv' .format( fileName ), skiprows=1, sep=',', dtype=float)
    #print(dataframe.values)
    return zip(*dataframe.values.tolist())

if __name__=="__main__":

    x = [1,2,3,4]
    y = [7,8,9,10]
    write_to_csv(x,y,'test', 'testname')
    
    x,y = read_from_csv('test')
    
    print(list(x), list(y))

    pass



