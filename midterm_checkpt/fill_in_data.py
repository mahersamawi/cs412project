import fileinput
import sys
from scipy import stats


def populate_array(arr, index):
    for i in documents:
        if i[index] == "N/A":
            continue
        arr.append(i[index])


def main():
    global documents 
    documents = []
    try:
        with open(sys.argv[1]) as f:
            for line in f:
                documents.append(line.strip().split(','))
    except:
        print "Unable to open file"
        return
    print len(documents)

    years = []
    genres = []

    populate_array(years, 1)
    populate_array(genres, 2)

    freq_year = ''.join(stats.mode(years)[0])
    freq_genre = ''.join(stats.mode(genres)[0])

    for i in documents:
        if i[1] == "N/A":
            i[1] = freq_year
        if i[2] == "N/A":
            i[2] = freq_genre

    with open("newMovies.txt", "w") as f:
        for i in documents:
            f.write(','.join(i) + "\n")
    f.close()


if __name__ == '__main__':
    main()
