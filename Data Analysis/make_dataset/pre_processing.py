import pandas as pd
import matplotlib.pyplot as plt
import time
import numpy as np
from data_extract import get_file_name


def get_time_list(filename):
    f = open(filename, 'r')
    time_all = []
    for line in f.readlines():
        temp = line.strip('\n')
        time_all.append(temp)
    return time_all


def remove_duplicates(dir_path, filename):
    csv_file = './data/remove_duplicates/' + filename + '_remove_duplicates.csv'
    file = pd.read_csv(dir_path + filename + '_raw.csv', low_memory=False)
    file_list = file.drop_duplicates()
    file_list.to_csv(csv_file)
    return csv_file


def sort_and_filter(filename, save_name, time1, time2):
    """
    Sort by timestamp, and then filter the data every 30 minutes.
    """
    csv_file = './data/sort_and_filter/' + save_name + '_all.csv'
    df = pd.read_csv(filename, usecols=[1, 2, 3, 4], low_memory=False)
    lc = df.sort_values(by=['Time'], ascending=True, kind='quicksort')

    begin = int(time.mktime(time.strptime(time1, '%Y-%m-%d %H:%M:%S')))
    end = int(time.mktime(time.strptime(time2, '%Y-%m-%d %H:%M:%S')))
    # time period, 30 minutes = 1800
    period = 1800

    # First, delete a little bit of data from the day before and after the day
    ld = lc[(lc['Time'] >= begin) & (lc['Time'] <= end)]

    # Then, select the data for a 30 minute period of time.
    # Select the first timestamp as the beginning of the day.
    # start_time = ld.iat[0, 3]
    ld.reset_index(inplace=True)
    del ld['index']

    # Create a new DataFrame
    df1 = pd.DataFrame(columns=['ID', 'Longitude', 'Latitude', 'Time'])

    for index in ld.index:
        # Take the value every 30 minutes.
        if (ld.iat[index, 3] - begin) % period <= 30:
            if (float(ld.iat[index, 1]) >= 114.0060) and (float(ld.iat[index, 1]) <= 114.1060):
                if (float(ld.iat[index, 2]) >= 22.5200) and (float(ld.iat[index, 2]) <= 22.6200):
                    df1 = df1.append(ld.loc[index], ignore_index=True)
    df1.to_csv(csv_file)
    return csv_file


def count(filename, save_name):
    """
    Calculate the inflow and outflow of each grid.
    """
    filename1 = './data/temp/' + save_name + '_time_'
    filename2 = './data/temp/' + save_name + '_count_'

    df = pd.read_csv(filename)
    # df2 = pd.DataFrame(columns=['x2', 'y2', 'ID2'])
    df3 = pd.DataFrame(columns=['time', 'count'])

    lc = []
    for i in range(df.shape[0]):
        lc.append(int((df.iat[i, 4] - df.iat[0, 4]) / 1800))
    for j in range(49):
        df3.loc[j] = {'time': j, 'count': 0}
    for m in range(49):
        for k in range(len(lc)):
            if lc[k] == m:
                df3.iat[m, 1] = df3.iat[m, 1] + 1

    # Determine which area the point is in, and add it to the group in the corresponding ordinal number.
    temp1 = 0
    for n in range(49):
        # Initialize DataFrame
        df1 = pd.DataFrame(columns=['x', 'y', 'ID'])
        index1 = 1
        for i in range(32):
            for j in range(32):
                df1.loc[index1] = {'x': i, 'y': j, 'ID': []}
                index1 = index1 + 1

        for index in range(df3.iat[n, 1]):
            x = int((df.iat[index + temp1, 2] - 114.0060) / 0.003125)
            y = int((df.iat[index + temp1, 3] - 22.5200) / 0.003125)
            loc = 32 * x + y
            df1.iat[loc, 2].append(df.iat[index, 1])
        temp1 = temp1 + df3.iat[n, 1]
        df1.to_csv(filename1 + str(n) + '.csv')

    # Compare two adjacent periods to get inflow and outflow.
    for fileCount in range(48):
        # from time1 to time2
        data1 = pd.read_csv(filename1 + str(fileCount) + '.csv')
        data2 = pd.read_csv(filename1 + str(fileCount + 1) + '.csv')

        # Create a empty DataFrame to store inflow and outflow.
        traffic_flow = pd.DataFrame(columns=['x', 'y', 'inflow', 'outflow'])
        index2 = 1
        for i in range(32):
            for j in range(32):
                traffic_flow.loc[index2] = {'x': i, 'y': j, 'inflow': 0, 'outflow': 0}
                index2 = index2 + 1

        # Complement Set
        for index3 in range(32 * 32):
            intersection = list(set(data1.iat[index3, 3]).intersection(set(data2.iat[index3, 3])))

            outflow = len(data1.iat[index3, 3]) - len(intersection)
            inflow = len(data2.iat[index3, 3]) - len(intersection)

            traffic_flow.iat[index3, 2] = inflow
            traffic_flow.iat[index3, 3] = outflow
        traffic_flow.to_csv(filename2 + str(fileCount) + '.csv')


def change_style(save_name):
    filename = './data/temp/' + save_name + '_count_'
    dicts = {}
    for i in range(32):
        dicts.setdefault(i, 0)

    for f in range(48):
        data = pd.read_csv(filename + str(f) + '.csv')

        df1 = pd.DataFrame(columns=[i for i in range(32)])
        df2 = pd.DataFrame(columns=[i for i in range(32)])

        index1 = 0
        for i in range(32):
            df1.loc[index1] = dicts
            index1 = index1 + 1

        index2 = 0
        for i in range(32):
            df2.loc[index2] = dicts
            index2 = index2 + 1

        for i in range(32):
            for j in range(32):
                df1.iat[i, j] = data.iat[i * 32 + j, 3]
                df2.iat[i, j] = data.iat[i * 32 + j, 4]
        df1.to_csv('./data/InOut/' + save_name + str(f) + 'inflow.csv')
        df2.to_csv('./data/InOut/' + save_name + str(f) + 'outflow.csv')


def show_locations(filename, title):
    """
    Show the data in the form of a scatter diagram.
    """
    data = pd.read_csv(filename)
    city_long_border = (114.0060, 114.1060)
    city_lat_border = (22.5200, 22.6200)

    plt.scatter(data['Longitude'], data['Latitude'], s=10, color='blue')

    plt.xlabel('Longitude')
    plt.ylabel('Latitude')

    plt.title(title)

    plt.xlim(city_long_border)
    plt.ylim(city_lat_border)
    # The following two lines are used to display the grid of 32x32.
    plt.xticks(np.linspace(114.0060, 114.1060, 33))
    plt.yticks(np.linspace(22.5200, 22.6200, 33))

    plt.grid(True)
    plt.show()


def main():
    dir_temp = './temp_data/'
    file_name = get_file_name('./raw_data/')
    time_all = get_time_list('time_1.txt')
    print('Total ' + str(len(file_name)) + ' files')
    for i in range(len(file_name)):
        print('File ' + str(i+1) + '/' + str(len(file_name)) + ': ' + file_name[i])
        file_remove = remove_duplicates(dir_temp, file_name[i])
        print('Removal of duplicate data has been completed!')
        file_sort = sort_and_filter(file_remove, file_name[i], time_all[i], time_all[i+1])
        print('Sorting and filtering are done!')
        count(file_sort, file_name[i])
        print('Statistics have been completed!')
        change_style(file_name[i])
        print('Change style has been done!')
    print('All done! Check the data!')


if __name__ == '__main__':
    main()
