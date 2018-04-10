import pandas as pd
import numpy as np
import h5py
import re


def save2h5():
    """
    Compress the CSV files into a HDF5 file
    """
    path_date = 'date_1.txt'
    file_hdf5 = 'SZ16_M32x32_InOut.h5'
    pattern1 = re.compile('GPS')
    pattern2 = re.compile('_')
    date_txt = open(path_date, 'r')
    date = []
    for line in date_txt.readlines():
        temp = line.strip('\n')
        date.append(temp)
    # Create an empty HDF5
    f = h5py.File(file_hdf5, 'w')
    data = np.zeros((48*31, 2, 32, 32))

    # Write the CSV files to the table.
    for m in range(len(date)):
        f_in = './data/InOut/' + date[m] + 'inflow.csv'
        f_out = './data/InOut/' + date[m] + 'outflow.csv'
        data_in = pd.read_csv(f_in).values[:, 1:]
        data_out = pd.read_csv(f_out).values[:, 1:]
        data[m][0][:][:] = data_in
        data[m][1][:][:] = data_out

    date_final = []
    for line in date:
        temp1 = pattern1.sub('', str(line))
        temp2 = pattern2.sub('', str(temp1))
        temp3 = temp2.strip('\n')
        date_final.append(temp3)
    date_h5 = [n.encode('ascii', 'ignore') for n in date_final]
    dset = f.create_dataset(name='data', shape=(len(date), 2, 32, 32), data=data)
    dest = f.create_dataset(name='date', data=date_h5)


def main():
    save2h5()


if __name__ == '__main__':
    main()
