"""
    This script is used to extract the data.
    each line in raw data is like "粤SL604H,113.871201,22.928350,2016-01-01 00:05:13,1490017,43,98,0,,,0,,"
    we need to extract the first four columns.
    the first four columns are: ID, longitude, latitude and time
"""
import csv
import codecs
import re
import time
import os


def get_file_name(file_path):
    files = []
    for file in os.listdir(file_path):
        files.append(file)
    files.sort()
    return files


def change_to_time_stamp(date):
    """
    Change time from '%Y-%m-%d %H:%M:%S' to timestamp
    """
    stamp = '%Y-%m-%d %H:%M:%S'
    time_stamp = time.mktime(time.strptime(date, stamp))
    return time_stamp


def main():
    # get file name
    dir_raw = './raw_data/'
    file_name = get_file_name(dir_raw)

    for i in range(len(file_name)):
        print('Total ' + str(len(file_name)) + ' files')
        print('File ' + str(i) + ': ' + file_name[i])
        # load raw data
        raw_data = csv.reader(open(dir_raw + file_name[i], 'r', encoding='utf-8'))

        # create csv file
        csv_file = codecs.open('./temp_data/' + file_name[i] + '_raw.csv', 'w', 'utf_8_sig')

        writer = csv.writer(csv_file)
        writer.writerow(['ID', 'Longitude', 'Latitude', 'Time'])

        # define a pattern to replace all Chinese characters with regular expressions.
        pattern = re.compile(u'[\u4e00-\u9fa5]')
        stamp = '%Y-%m-%d %H:%M:%S'
        # Remove the wrong data, line by line.
        for lines in raw_data:
            # Some data is incomplete.
            # print(lines[3])
            if len(lines) < 4:
                continue
            try:
                time.strptime(str(lines[3]), stamp)
                data3 = lines[3]
            except ValueError:
                continue
            # Take the first four fields
            data1 = lines[0]
            data2 = lines[1:3]

            # Replace the Chinese
            data1 = pattern.sub('', str(data1)).split(' ')

            # Convert time to a timestamp
            time_stamp = change_to_time_stamp(data3)

            data2.append(time_stamp)

            data1.extend(data2)
            writer.writerow(data1)
        print('File ' + file_name[i] + ' has been Done!')
        csv_file.close()


if __name__ == '__main__':
    main()
