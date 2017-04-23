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
    # print(g_dict)

    # Change this XXX


def find_ID(arr, user_id, movie_id, rating):
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


def find_rating(arr, user_id, movie_id, totals):
    probs = np.ones(5)
    for j in range(5):
        for i, string in enumerate(user_dict[int(user_id)][1:-1].split(",")):
            corrected_str = string.strip()[1:-1]
            getFrom = ratingsdict[j][i]
            if i == 0:
                gender = corrected_str[0]
                probs[j] *= (getFrom.get(gender, 0) + 1)*1.0/(totals[j] + 5)
            else:
                value_to_add = int(corrected_str)
                probs[j] *= (getFrom.get(value_to_add, 0) + 1)*1.0/(totals[j] + 5)

        for i, string in enumerate(movie_dict[int(movie_id)][1:-1].split(",")):
            corrected_str = string.strip()[1:-1]
            getFrom = ratingsdict[j][i + 3]
            if i == 0:
                year = int(corrected_str)
                probs[j] *= (getFrom.get(year, 0) + 1)*1.0/(totals[j]+5)
            else:
                for genres in corrected_str.split('|'):
                    num = g_dict[genres]
                    probs[j] *= (getFrom.get(num, 0) + 1)*1.0/(totals[j]+5)
        probs[j] *= totals[j]*1.0/sum(totals)
    global flag
    if flag == 0:
        print(probs)
        flag += 1
    return (np.argmax(probs) + 1)

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
    totals = [0]*5
    number_dimension = 22
    training_data = np.zeros((len(training_data_list), number_dimension))
    results = np.zeros((len(test_data)))

    for line in training_data_list:
        # Check if errors
        find_ID(training_data, line[1], line[2], int(line[3]))
        totals[int(line[3]) - 1] += 1

    for index, line in enumerate(test_data):
        results[index] = find_rating(test_data,line[1],line[2],totals)
    # print(training_data[0])

    # Here we'll use our ratingsdict

    with open('Bayes_result.txt', 'w') as f:
        f.write("Id,rating\n")
        for index in range(len(test_data)):
            # f.write(', '.join(map(str,[line[0],results[]]))+'\n')
            f.write("%s,%s\n" % (test_data[index][0], int(results[index])))

if __name__ == '__main__':
    main()
