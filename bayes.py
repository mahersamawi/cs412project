import sys
import random
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
    # print(g_dict)

    # Change this XXX


def find_ID(user_id, movie_id, rating):
    for i, string in enumerate(user_dict[int(user_id)][1:-1].split(",")):
        corrected_str = string.strip()[1:-1]
        addingAt = ratingsdict[rating - 1][i]
        if i == 0:
            gender = corrected_str[0]
            addingAt[gender] = addingAt.get(gender, 0) + 1
        else:
            value_to_add = int(corrected_str)
            addingAt[value_to_add] = addingAt.get(value_to_add, 0) + 1

    for i, string in enumerate(movie_dict[int(movie_id)][1:-1].split(",")):
        corrected_str = string.strip()[1:-1]
        addingAt = ratingsdict[rating - 1][i + 3]
        if i == 0:
            year = int(corrected_str)
            addingAt[year] = addingAt.get(year, 0) + 1
        else:
            for genres in corrected_str.split('|'):
                num = g_dict[genres]
                addingAt[num] = addingAt.get(num, 0) + 1


def find_rating(user_id, movie_id, totals):
    # Call function to randomly select tuples
    # Change Ratings Dict
    # Now we have the tuples, now find the ratings based on the probabilities
    # Grab more tuples (10 times)
    # Add up probability vectors and chose best
    probs = np.ones(5)
    for j in range(5):
        for i, string in enumerate(user_dict[int(user_id)][1:-1].split(",")):
            corrected_str = string.strip()[1:-1]
            getFrom = ratingsdict[j][i]
            if i == 0:
                gender = corrected_str[0]
                probs[j] *= (getFrom.get(gender, 0) + 1) * \
                    1.0 / (totals[j] + 5)
            else:
                value_to_add = int(corrected_str)
                probs[j] *= (getFrom.get(value_to_add, 0) + 1) * \
                    1.0 / (totals[j] + 5)

        for i, string in enumerate(movie_dict[int(movie_id)][1:-1].split(",")):
            corrected_str = string.strip()[1:-1]
            getFrom = ratingsdict[j][i + 3]
            if i == 0:
                year = int(corrected_str)
                probs[j] *= (getFrom.get(year, 0) + 1) * 1.0 / (totals[j] + 5)
            else:
                for genres in corrected_str.split('|'):
                    num = g_dict[genres]
                    probs[j] *= (getFrom.get(num, 0) + 1) * \
                        1.0 / (totals[j] + 5)
        probs[j] *= totals[j] * 1.0 / sum(totals)
        probs[j] *= (len(sorted_train[j])* 1.0) / num_lines 
    
    global flag
    if flag == 0:
        print(probs)
        flag += 1
    return probs


def prob():
    pass


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

    global flag
    flag = 0
    global movie_dict
    global user_dict
    movie_dict = {}
    user_dict = {}

    make_dict(user_dict, user_data)
    make_dict(movie_dict, movie_data)

    global ratingsdict
    ratingsdict = [[{} for i in range(5)] for j in range(5)]
    totals = [0] * 5
    number_dimension = 22
    training_data = np.zeros((len(training_data_list), number_dimension))
    results = np.zeros((len(test_data), 5))

    global sorted_train 
    sorted_train = [[]for i in range(5)]

    global num_lines
    num_lines = 0
    for line in training_data_list:
        sorted_train[int(line[3]) - 1].append(line)
        num_lines += 1
    num_lines -= 1


    for count in range(30):
        ratingsdict = [[{} for i in range(5)] for j in range(5)]
        for line in training_data_list:
            # Check if errors
            ran_out = random.randint(0,4)
            ran_in = random.randint(0, len(sorted_train[ran_out]) - 1)
            s_line = sorted_train[ran_out][ran_in]

            find_ID(s_line[1], s_line[2], int(s_line[3]))
            totals[int(s_line[3]) - 1] += 1

        for index, line in enumerate(test_data):
            results[index] += find_rating(line[1], line[2], totals)

    # Here we'll use our ratingsdict

    with open('Bayes_result_final.txt', 'w') as f:
        f.write("Id,rating\n")
        for index in range(len(test_data)):
            f.write("%s,%s\n" % (test_data[index][0], int(np.argmax(results[index]) + 1 )))
    

if __name__ == '__main__':
    main()
