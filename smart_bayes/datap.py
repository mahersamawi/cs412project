#!/usr/bin/python

# -*- coding: utf-8 -*-
from dataclass import Train, Test, User, Movie

from operator import itemgetter
from time import time

# sequential code style
start_time = time()
'''
helper funciton time_elapse: print the input information and time information
can be both used to debug and tell the current progress
'''
def time_elapse(info):
	global start_time
	now = time()
	elapse, start_time = now - start_time, now
	print info, 'took', elapse, 'seconds'

'''
first convert all datafile into dataclass information
'''
datafile = "data/train.txt"
train = Train(datafile);
time_elapse('Loading '+datafile)
datafile = "data/test.txt"
test = Test(datafile);
time_elapse('Loading '+datafile)
datafile = "data/user.txt"
user = User(datafile, train, test)
time_elapse('Loading '+datafile)
print user.alabel
datafile = "data/movie.txt"
movie = Movie(datafile, train, test)
time_elapse('Loading '+datafile)
print len(movie.glabel), movie.glabel
user.write('user.txt') # check if info is printed correctly
movie.write('movie.txt')

'''
Then for each N/A value in genres do as followed:
1. for all the movies rated the same score by the same users (associated in the train data), consider their genres 
2. If still no enough data, consider the genres of all movies in the same year
In general, a heuristical imputation based on nearest movie
'''
for midx in range(0, len(movie.id)):
	if not movie.id_used(midx):
		continue
	if len(movie.genre[midx]) > 0:
		continue
	#print 'Updating Moive', movie.get(midx)
	fgen = [0] * len(movie.glabel)
	for uidx in train.midx[midx]:
		rating = train.rating[(uidx,midx)]
		for m in train.uidx[uidx]:
			if rating != train.rating[(uidx,m)]:
				continue
			for g in movie.genre[m]:
				fgen[g] += 1
	sgen = []
	total = 0
	for i in range(0, len(fgen)):
		#print i, ":", movie.glabel[i], "  ", fgen[i]
		total += fgen[i]
	if total < 10:
		print 'too few train data, tring year'
		if movie.year[midx] == -1:
			print 'no year also, do nothing'
			continue
		total = 0
		year = movie.year[midx]
		for i in range(0, len(movie.year)):
			if i == midx or year != movie.year[i]:
				continue
			for g in movie.genre[i]:
				fgen[g] += 1
	for i in range(0, len(fgen)):
		total += fgen[i]
	if total < 10:
		print 'too few year data, do nothing'
		continue
				
	for i in range(0, len(fgen)):
		sgen.append((float(fgen[i])/total, i))
	#print sorted(sgen, key=itemgetter(0), reverse=True)
	#sgen.sort(reverse=True);
	cnt = 0.0
	ths = [0.25, 0.34, 0.40]
	stp = 0
	last = 0.0
	for key in sorted(sgen, key=itemgetter(0), reverse=True):
		cnt += key[0]
		if last / key[0] > 1.6:
			break;
		last = key[0];
		#print key, movie.glabel[key[1]]
		movie.genre[midx].append(key[1])
		if cnt >= ths[stp]:
			break;
		stp += 1;
		if stp >= len(ths):
			break;
time_elapse('Replacing movie genre')

'''
For missing values in year of movie
Do the same kind of imputation to year except not considering complexity of genres, just do following for each movie with year missing:
1. for all the movies rated the same score by the same users, record year. replace with most count
'''
for midx in range(0, len(movie.id)):
	if not movie.id_used(midx):
		continue
	if movie.year[midx] != -1:
		continue
	#print 'Updating Moive', movie.get(midx)
	fyear = [0] * len(movie.ylabel)
	for uidx in train.midx[midx]:
		rating = train.rating[(uidx,midx)]
		#print uidx, midx, ":", user.alabel[user.age[uidx]], "-", rating, movie.genre[midx]
		for m in train.uidx[uidx]:
			if rating != train.rating[(uidx,m)]:
				continue
			if movie.year[m] == -1:
				continue
			#gs = [g for g in movie.genre[midx] if g in movie.genre[m]]
			#if len(gs) > 0:
				#continue
			#print movie.ylabel[movie.year[m]], movie.genre[m], gs
			fyear[movie.year[m]] += 1;
	syear = []
	total = 0
	for i in range(0, len(fyear)):
		total += fyear[i]
	if total < 1:
		print 'too few train data for movie year, do nothing'
		continue
	for i in range(0, len(fyear)):
		syear.append((float(fyear[i])/total, i))
	#print sorted(syear, key=itemgetter(0), reverse=True)
	key = sorted(syear, key=itemgetter(0), reverse=True)[0];
	movie.year[midx] = key[1];
	#print 'Replace with ', key, movie.ylabel[movie.year[m]]
time_elapse('Replacing movie year')

for midx in range(0, len(movie.id)):
	if not movie.id_used(midx):
		continue
	if movie.year[midx] == -1:
		print 'Still have invlaid year for movie id:', movie.get(midx)
		for uidx in train.midx[midx]:
			rating = train.rating[(uidx,midx)]
			print uidx, midx, ":", user.alabel[user.age[uidx]], "-", rating, movie.genre[midx]
		movie.year[midx] = 4
	if len(movie.genre[midx]) == 0:
		print 'Still have invlaid genre for movie id:', movie.get(midx)
time_elapse('Replacing movie year and genre')


'''
For missing values of any user attribute
Do the same kind of imputation as year's except from user's perspective
1. for all the users rated the same score for the same movie, record each attribute. replace any missing value with corresponding most count 
'''
for uidx in range(0, len(user.id)):
	if not user.id_used(midx):
		continue
	good = True
	if user.gender[uidx] == -1:
		good = False
	elif user.age[uidx] == -1:
		good = False
	elif user.occupation[uidx] == -1:
		good = False
	if good:
		continue
	#print 'Updating User', user.get(uidx)
	fgender = [0] * 2
	fage = [0] * len(user.alabel)
	foccupation = [0] * len(user.olabel)
	total = [0] * 3
	for midx in train.uidx[uidx]:
		rating = train.rating[(uidx,midx)]
		for u in train.midx[midx]:
			if rating != train.rating[(u,midx)]:
				continue;
			if user.gender[u] != -1:
				fgender[user.gender[u]] += 1
			if user.age[u] != -1:
				fage[user.age[u]] += 1
			if user.occupation[u] != -1:
				foccupation[user.occupation[u]] += 1
	for i in fgender:
		total[0] += i
	for i in fage:
		total[1] += i
	for i in foccupation:
		total[2] += i
	good = True
	if user.gender[uidx] == -1:
		sfreq = []
		if total[0] > 0:
			for i in range(0, len(fgender)):
				sfreq.append((float(fgender[i])/total[0], i))
			#print sorted(sfreq, key=itemgetter(0), reverse=True)
			key = sorted(sfreq, key=itemgetter(0), reverse=True)[0];
			user.gender[uidx] = key[1];
		else:
			good = False
	if user.age[uidx] == -1:
		sfreq = []
		if total[1] > 0:
			for i in range(0, len(fage)):
				sfreq.append((float(fage[i])/total[1], i))
			#print sorted(sfreq, key=itemgetter(0), reverse=True)
			key = sorted(sfreq, key=itemgetter(0), reverse=True)[0];
			user.age[uidx] = key[1];
		else:
			good = False
	if user.occupation[uidx] == -1:
		sfreq = []
		if total[2] > 0:
			for i in range(0, len(foccupation)):
				sfreq.append((float(foccupation[i])/total[2], i))
			#print sorted(sfreq, key=itemgetter(0), reverse=True)
			key = sorted(sfreq, key=itemgetter(0), reverse=True)[0];
			user.occupation[uidx] = key[1];
		else:
			good = False
	if not good:
		print 'Still Need Update User', user.get(uidx)
time_elapse('Replacing user data')
user.write('new_user.txt')
movie.write('new_movie.txt')
