from sklearn.ensemble import RandomForestClassifier
import sys
import numpy as np


def open_file(index, arr):
    print sys.argv[index]
    try:
        with open(sys.argv[index]) as f:
            for i, line in enumerate(f):
                if i == 0:
                    continue
                arr.append(line.strip().split(','))
    except:
        print "Unable to open file"
        return


def make_dict(my_dict, data_array):
    for dat in data_array:
        my_dict[int(dat[0])] = str(dat[1:])


def convert_genres(arg):
    pass


def find_ID(arr, user_id, movie_id, index):
    # print list(user_dict[user_id][1:-1])
    for i, string in enumerate(user_dict[user_id][1:-1].split(",")):
        corrected_str = string.strip()[1:-1]
        if i == 0:
            if corrected_str[0] == "M":
                arr[index][0] = 1
            else:
                arr[index][0] = 0
        else:
            arr[index][i] = int(corrected_str)
    for i, string in enumerate(movie_dict[movie_id][1:-1].split(",")):
        corrected_str = string.strip()[1:-1]
        if i == 0:
            arr[index][i + 3] = int(corrected_str)
        else:
            arr[index][i + 3] = convert_genres(corrected_str)


def main():
    ratings = []
    training_data_list = []
    user_data = []
    movie_data = []
    open_file(1, training_data_list)
    open_file(2, user_data)
    open_file(3, movie_data)

    global movie_dict
    global user_dict
    movie_dict = {}
    user_dict = {}

    make_dict(user_dict, user_data)
    make_dict(movie_dict, movie_data)

    training_data = np.zeros((len(training_data_list), 5))
    ratings_array = np.zeros((len(training_data_list)))
    # print user_data[0]
    # print training_data_list[0]
    # for index, i in enumerate(training_data):
    # Check if errors
    #find_ID(training_data, i[1], i[2])
    #ratings_array[index] = i[3]
    find_ID(training_data, 6032, 197, 0)
    print training_data[0]


if __name__ == '__main__':
    main()
