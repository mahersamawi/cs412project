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
    f.close()


def make_dict(my_dict, data_array):
    for dat in data_array:
        my_dict[int(dat[0])] = str(dat[1:])


def convert_genres(genre):
    # Change this XXX
    return np.random.randint(1, 10)


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
            arr[index][i + 3] = convert_genres(corrected_str)


def main():
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

    training_data = np.zeros((len(training_data_list), 5))
    ratings = np.zeros((len(training_data_list)))

    test_arr = np.zeros((len(test_data), 5))

    for index, line in enumerate(training_data_list):
        # Check if errors
        find_ID(training_data, line[1], line[2], index)
        ratings[index] = line[3]

    '''for index, line in enumerate(test_data):
        find_ID(test_arr, line[1], line[2],index)


    rf = RandomForestClassifier(n_estimators=100)
    rf.fit(training_data, ratings)
    testArr = np.zeros((len(training_data_list), 5))
    results = rf.predict(test_arr)

    
    print results[0]
    print results[1]
    print results[2]'''


if __name__ == '__main__':
    main()
