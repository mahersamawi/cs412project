import sys
import random
import pandas as pd
import numpy as np


# Opens the file and reads the contents into an array
def open_file(arg_num, arr_to_populate):
    try:
        with open(sys.argv[arg_num]) as f:
            for i, line in enumerate(f):
                if i == 0:
                    continue
                content = line.strip().split(',')
                arr_to_populate.append(content)
    except:
        print "Unable to open file"
        return


# Creates a dictionary for the users and movies
def make_dict(dict_to_populate, data_array):
    for dat in data_array:
        dict_to_populate[int(dat[0])] = str(dat[1:])


# Populates the g_dict (genre dictionary)
def convert_genres():
    dataframe = pd.read_csv('inputs/movie.txt')
    counter = 3
    for value in (pd.Series.unique(dataframe['Genre'])):
        for genre in value.split('|'):
            if genre not in g_dict:
                counter += 1
                g_dict[genre] = counter


# Finds the user attributes and the movie attributes
# Combines them into one entry in the array
def find_ID(user_id, movie_id, rating):
    # User part
    for i, string in enumerate(user_dict[int(user_id)][1:-1].split(",")):
        corrected_str = string.strip()[1:-1]
        adding_at = rating_dict[rating - 1][i]
        if i == 0:
            gender = corrected_str[0]
            adding_at[gender] = adding_at.get(gender, 0) + 1
        else:
            value_to_add = int(corrected_str)
            adding_at[value_to_add] = adding_at.get(value_to_add, 0) + 1
    # Movie part
    for i, string in enumerate(movie_dict[int(movie_id)][1:-1].split(",")):
        corrected_str = string.strip()[1:-1]
        adding_at = rating_dict[rating - 1][i + 3]
        if i == 0:
            year = int(corrected_str)
            adding_at[year] = adding_at.get(year, 0) + 1
        else:
            for genres in corrected_str.split('|'):
                num = g_dict[genres]
                adding_at[num] = adding_at.get(num, 0) + 1


# Used to predict what rating a user will give a movie
# Similar to find_ID but used to actually predict the rating
# Returns an array that tells us the probabilities of the user labeling a
# movie between 1 and 5
# Bayes Classifier Algorithm
def find_rating(user_id, movie_id, totals):
    probs = np.ones(5)
    for j in range(5):
        for i, string in enumerate(user_dict[int(user_id)][1:-1].split(",")):
            corrected_str = string.strip()[1:-1]
            get_from = rating_dict[j][i]
            if i == 0:
                gender = corrected_str[0]
                probs[j] *= (get_from.get(gender, 0) + 1) * \
                    1.0 / (totals[j] + 5)
            else:
                value_to_add = int(corrected_str)
                probs[j] *= (get_from.get(value_to_add, 0) + 1) * \
                    1.0 / (totals[j] + 5)

        for i, string in enumerate(movie_dict[int(movie_id)][1:-1].split(",")):
            corrected_str = string.strip()[1:-1]
            get_from = rating_dict[j][i + 3]
            if i == 0:
                year = int(corrected_str)
                probs[j] *= (get_from.get(year, 0) + 1) * 1.0 / (totals[j] + 5)
            else:
                for genres in corrected_str.split('|'):
                    num = g_dict[genres]
                    probs[j] *= (get_from.get(num, 0) + 1) * \
                        1.0 / (totals[j] + 5)
        probs[j] *= totals[j] * 1.0 / sum(totals)
        probs[j] *= (len(sorted_train[j]) * 1.0) / num_lines
    return probs


# Takes the test data and results arrray
# Results stores the probabilities of the each label for that example
# Prints to the file the max of the array entries in results
def print_results(test_data, results):
    with open('Bayes_result_final.txt', 'w') as f:
        f.write("Id,rating\n")
        for index in range(len(test_data)):
            f.write("%s,%s\n" %
                    (test_data[index][0], int(np.argmax(results[index]) + 1)))


def main():
    # Genre dictionary
    global g_dict
    g_dict = {}
    convert_genres()

    training_data_list = []
    user_data = []
    movie_data = []
    test_data = []
    # Populate arrays
    open_file(1, training_data_list)
    open_file(2, user_data)
    open_file(3, movie_data)
    open_file(4, test_data)

    # Movie and user dictionaries
    global movie_dict
    global user_dict
    movie_dict = {}
    user_dict = {}

    make_dict(user_dict, user_data)
    make_dict(movie_dict, movie_data)

    # Array of dictionaries of size 5 for each label
    # Ratings dictionary for each attribute for each label
    global rating_dict
    rating_dict = [[{} for i in range(5)] for j in range(5)]

    totals = [0] * 5
    number_dimension = 22
    training_data = np.zeros((len(training_data_list), number_dimension))
    results = np.zeros((len(test_data), 5))

    global sorted_train
    sorted_train = [[]for i in range(5)]

    # Sort the training data based on the labels
    num_lines = 0
    for line in training_data_list:
        sorted_train[int(line[3]) - 1].append(line)
        num_lines += 1
    num_lines -= 1

    # Bagging Method
    # Pick random label from 0 - 4
    # Pick random example from label
    # Totals array stores the sums of each label
    for count in range(30):
        rating_dict = [[{} for i in range(5)] for j in range(5)]
        for line in training_data_list:
            ran_out = random.randint(0, 4)
            ran_in = random.randint(0, len(sorted_train[ran_out]) - 1)
            s_line = sorted_train[ran_out][ran_in]

            find_ID(s_line[1], s_line[2], int(s_line[3]))
            totals[int(s_line[3]) - 1] += 1

        for index, line in enumerate(test_data):
            results[index] += find_rating(line[1], line[2], totals)

    # Output the predicted values
    print_results(test_data, results)


if __name__ == '__main__':
    main()
