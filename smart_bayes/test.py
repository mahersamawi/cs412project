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
first convert all (user,movie converted) datafiles into dataclass information
'''
datafile = "data/train.txt"
train = Train(datafile);
time_elapse('Loading '+datafile)
datafile = "data/test.txt"
test = Test(datafile);
time_elapse('Loading '+datafile)
datafile = "new_user.txt"
user = User(datafile, train, test)
time_elapse('Loading '+datafile)
datafile = "new_movie.txt"
movie = Movie(datafile, train, test)
time_elapse('Loading '+datafile)



'''
data validation
'''
for line in test.rating:
	id, uid, mid, rating = line
	if id == -1:
		continue
	good = True
	if not user.id_used(uid):
		good = False
	if user.gender[uid] == -1:
		good = False
	if user.age[uid] == -1:
		good = False
	if user.occupation[uid] == -1:
		good = False
	if not good:
		print 'Imcompleted User', uid, user.get(uid)
	good = True
	if not movie.id_used(mid):
		good = False
	if movie.year[mid] == -1:
		good = False
	if len(movie.genre[mid]) == 0:
		good = False
	if not good:
		print 'Imcompleted Movie', mid, movie.get(mid)
time_elapse('Checking User and Movie...')


'''
class MovieData: initial a possibility table of specified size for each user attribute (since cross evaluated)
'''
class MovieData:
	def __init__(self, ages, occs):
		self.gender = [[1 for col in range(2)] for row in range(5)]
		self.age = [[1 for col in range(ages)] for row in range(5)]
		self.occupation = [[1 for col in range(occs)] for row in range(5)]


'''
Calculating modified Bayes possibilities for user part with laplace smoothing
'''
mdata = [-1] * len(movie.id);
next = []
for mid in range(len(movie.id)):
	if not movie.id_used(mid):
		continue
	mdata[mid] = MovieData(len(user.alabel), len(user.olabel))
	total = 0
	for uid in train.midx[mid]:
		g = user.gender[uid]
		a = user.age[uid]
		o = user.occupation[uid]
		rating = train.rating[(uid, mid)]
		#print uid, mid, rating, gender, age
		mdata[mid].gender[rating][g] += 1
		mdata[mid].age[rating][a] += 1
		mdata[mid].occupation[rating][o] += 1
		total += 1
	gt = total + 2
	at = total + len(user.alabel)
	ot = total + len(user.olabel)
	for r in range(5):
		g = mdata[mid].gender[r];
		for i in range(len(g)):
			g[i] = 100.0 * float(g[i]) / float(gt)
		a = mdata[mid].age[r];
		for i in range(len(a)):
			a[i] = 100.0 * float(a[i]) / float(at)
		o = mdata[mid].occupation[r];
		for i in range(len(o)):
			o[i] = 100.0 * float(o[i]) / float(ot)
time_elapse('Generating Movie Data ...')
	

'''
class UserData: initial a possibility table of specified size for each movie attribute
'''
class UserData:
	def __init__(self, gns, yrs):
		self.genre = [[1 for col in range(gns)] for row in range(5)]
		self.year = [[1 for col in range(yrs)] for row in range(5)]
	

'''
Calculating Bayes possibilities for movie part with laplace smoothing
'''
udata = [-1] * len(user.id);
for uid in range(len(user.id)):
	if not user.id_used(uid):
		continue
	udata[uid] = UserData(len(movie.glabel), len(movie.ylabel))
	gt, yt = len(movie.glabel), len(movie.ylabel)
	for mid in train.uidx[uid]:
		gs = movie.genre[mid]
		y = movie.year[mid]
		rating = train.rating[(uid, mid)]
		#print uid, mid, rating, g, y
		for g in gs:
			udata[uid].genre[rating][g] += 1
			gt += 1
		udata[uid].year[rating][y] += 1
		yt += 1
	for r in range(5):
		g = udata[uid].genre[r];
		for i in range(len(g)):
			g[i] = 100.0 * float(g[i]) / float(gt)
		y = udata[uid].year[r];
		for i in range(len(y)):
			y[i] = 100.0 * float(y[i]) / float(yt)
time_elapse('Generating User Data ...')







'''
The last part: Combine User and Movie parts to figure out the final rating of each test data
'''
import sys
methods = ['default', 'user', 'movie', 'weight']
method = 0
if len(sys.argv) > 1:
	if sys.argv[1].lower() in methods:
		method = methods.index(sys.argv[1].lower())

print "Start Rating with method [%s]" % methods[method]
for line in test.rating:
	if line[0] == -1:
		continue
	uid = line[1]
	mid = line[2]
	#print uid, udata[uid].genre
	ur = [0] * 5
	mr = [0] * 5
	for r in range(5):
		gr = []
		for g in movie.genre[mid]:
			gr.append(udata[uid].genre[r][g])
		if len(gr) == 0:
			print 'Wrong at', uid, mid
			exit()
		y = movie.year[mid]
		#ur[r] = float(max(gr)) * float(udata[uid].year[r][y])
		gr = float(sum(gr)) / float(len(gr))
		ur[r] = float(gr) * float(udata[uid].year[r][y])
	for r in range(5):
		g = user.gender[uid]
		a = user.age[uid]
		o = user.occupation[uid]
		mr[r] = float(mdata[mid].gender[r][g]) * float(mdata[mid].age[r][a]) #* float(mdata[mid].occupation[r][o])
	result = []
	if   method == 3:
		# weight user data + movie data
		for r in range(5):
			w = ur[r]*0.6
			w += mr[r]*0.4
			w += ur[r]*mr[r]
			result.append((w, r))
	elif method == 2:
		# movie data only
		for r in range(5):
			result.append((mr[r], r))
	elif method == 1:
		# user data only
		for r in range(5):
			result.append((ur[r], r))
	else:
		#default for user data + movie data
		for r in range(5):
			result.append((ur[r]*mr[r], r))
	rating = sorted(result, key=itemgetter(0), reverse=True)[0][1]
	#print rating, sorted(result, key=itemgetter(0), reverse=True)
	line[3] = rating+1
outfile = 'smart_result.txt'
if method != 0:
	outfile = '%s_result.txt' % methods[method]
test.write(outfile)
time_elapse('Rating Test Data ...')
