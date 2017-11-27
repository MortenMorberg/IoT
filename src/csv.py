import pandas as pd

def write_to_csv(x, y, fileName):
    toCSV = ['{0}, {1}\n'.format(x, y) for x,y in zip(x,y)]
    with open('{0}.csv'.format(fileName), 'w') as csv_file:
            csv_file.write(''.join(toCSV))

def read_from_csv(fileName):
    dataframe = pd.read_csv('{0}.csv' .format( fileName ), sep=',', header=None, dtype=float)
    return zip(*dataframe.values.tolist())

if __name__=="__main__":
    pass


