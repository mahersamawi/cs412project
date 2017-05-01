#!/usr/bin/python

# -*- coding: utf-8 -*-
from dataclass import Train, Test, User, Movie

from operator import itemgetter
from time import time

start_time = time()
def time_elapse(info):
	global start_time
	now = time()
	elapse, start_time = now - start_time, now
	print info, 'took', elapse, 'seconds'



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

class MovieData:
	def __init__(self, ages, occs):
		self.gender = [[1 for col in range(2)] for row in range(5)]
		self.age = [[1 for col in range(ages)] for row in range(5)]
		self.occupation = [[1 for col in range(occs)] for row in range(5)]

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
			g[i] = float(g[i]) / gt
		a = mdata[mid].age[r];
		for i in range(len(a)):
			a[i] = float(a[i]) / at
		o = mdata[mid].occupation[r];
		for i in range(len(o)):
			o[i] = float(o[i]) / ot
time_elapse('Generating Movie Data ...')
	
class UserData:
	def __init__(self, gns, yrs):
		self.genre = [[1 for col in range(gns)] for row in range(5)]
		self.year = [[1 for col in range(yrs)] for row in range(5)]
	
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
			g[i] = float(g[i]) / gt
		y = udata[uid].year[r];
		for i in range(len(y)):
			y[i] = float(y[i]) / yt
time_elapse('Generating User Data ...')

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
		ur[r] = float(max(gr)) * udata[uid].year[r][y]
	for r in range(5):
		g = user.gender[uid]
		a = user.age[uid]
		o = user.occupation[uid]
		mr[r] = float(mdata[mid].gender[r][g]) * mdata[mid].age[r][a] * mdata[mid].occupation[r][o]
	result = []
	for r in range(5):
		result.append((ur[r]*mr[r], r))
	rating = sorted(result, key=itemgetter(0), reverse=True)[0][1]
	#print rating, sorted(result, key=itemgetter(0), reverse=True)
	line[3] = rating+1
test.write('result.txt')
time_elapse('Rating Test Data ...')
