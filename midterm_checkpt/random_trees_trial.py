from sklearn.ensemble import RandomForestClassifier
import sys
import pandas as pd
import numpy as np


def open_file(index, arr):
    try:
        with open(sys.argv[index]) as f:
            for i, line in enumerate(f):
                if i == 0:
                    continue
                arr.append(line.strip().split(','))
    except:
        print "Unable to open file"
        return
    f.close()


def make_dict(my_dict, data_array):
    for dat in data_array:
        my_dict[int(dat[0])] = str(dat[1:])


def convert_genres():
    dataframe = pd.read_csv('inputs/movie.txt')

    counter = 3
    for value in (pd.Series.unique(dataframe['Genre'])):
        for genre in value.split('|'):
            if genre not in g_dict:
                counter += 1
                g_dict[genre] = counter
    #print(g_dict)

    # Change this XXX


def find_ID(arr, user_id, movie_id, index):
    for i, string in enumerate(user_dict[int(user_id)][1:-1].split(",")):
        corrected_str = string.strip()[1:-1]
        if i == 0:
            if corrected_str[0] == "M":
                arr[index][0] = 1
            else:
                arr[index][0] = 0
        else:
            arr[index][i] = int(corrected_str)
    for i, string in enumerate(movie_dict[int(movie_id)][1:-1].split(",")):
        corrected_str = string.strip()[1:-1]
        if i == 0:
            arr[index][i + 3] = int(corrected_str)
        else:
            for genres in corrected_str.split('|'):
                arr[index][g_dict[genres]] = 1


def main():

    global g_dict
    g_dict = {}
    convert_genres()

    training_data_list = []
    user_data = []
    movie_data = []
    test_data = []
    open_file(1, training_data_list)
    open_file(2, user_data)
    open_file(3, movie_data)
    open_file(4, test_data)

    global movie_dict
    global user_dict
    movie_dict = {}
    user_dict = {}

    make_dict(user_dict, user_data)
    make_dict(movie_dict, movie_data)

    number_dimension = 22
    training_data = np.zeros((len(training_data_list), number_dimension))
    ratings = np.zeros((len(training_data_list)))

    test_arr = np.zeros((len(test_data), number_dimension))

    for index, line in enumerate(training_data_list):
        # Check if errors
        find_ID(training_data, line[1], line[2], index)
        ratings[index] = line[3]

    # print(training_data[0])

    for index, line in enumerate(test_data):
        find_ID(test_arr, line[1], line[2], index)

    rf = RandomForestClassifier(n_estimators=75)
    rf.fit(training_data, ratings)
    results = rf.predict(test_arr)

    with open('result.txt', 'w') as f:
        f.write("Id,rating\n")
        for index in range(len(test_data)):
            # f.write(', '.join(map(str,[line[0],results[]]))+'\n')
            f.write("%s,%s\n" % (test_data[index][0], int(results[index])))

if __name__ == '__main__':
    main()
