# Embedded file name: C:\Works\dataclass.py
from operator import itemgetter
from time import time

class Train:
	def __init__(self, datafile):
		self.rating = {}
		self.uidx = []
		self.midx = []
		with open(datafile) as ifile:
			lc = 0
			for line in ifile:
				lc += 1
				if lc == 1:
					continue
				cols = line.strip().split(',')
				uidx = int(cols[1])
				if uidx >= len(self.uidx):
					for i in range(len(self.uidx), uidx + 1):
						self.uidx.append([])
				midx = int(cols[2])
				if midx >= len(self.midx):
					for i in range(len(self.midx), midx + 1):
						self.midx.append([])
				self.uidx[uidx].append(midx)
				self.midx[midx].append(uidx)
				rating = int(cols[3]) - 1
				if rating not in range(5):
					print 'Invild rating', line
				rating = {(uidx, midx): rating}
				self.rating.update(rating)

	def is_uid(self, id):
		if len(self.uidx[id]) > 0:
			return True
		return False

	def is_mid(self, id):
		if len(self.midx[id]) > 0:
			return True
		return False


class Test:
	def __init__(self, datafile):
		self.rating = [[-1, 0, 0, 0]]
		self.uidx = []
		self.midx = []
		with open(datafile) as ifile:
			lc = 0
			for line in ifile:
				lc += 1
				if lc == 1:
					continue
				cols = line.strip().split(',')
				uidx = int(cols[1])
				if uidx >= len(self.uidx):
					for i in range(len(self.uidx), uidx + 1):
						self.uidx.append(-1)
				self.uidx[uidx] = 1
				midx = int(cols[2])
				if midx >= len(self.midx):
					for i in range(len(self.midx), midx + 1):
						self.midx.append(-1)
				self.midx[midx] = 1
				self.rating.append([int(cols[0]), uidx, midx, -1])

	def is_uid(self, id):
		if self.uidx[id] > 0:
			return True
		return False

	def is_mid(self, id):
		if self.midx[id] > 0:
			return True
		return False

	def write(self, datafile):
		with open(datafile, 'w') as f:
			for line in self.rating:
				id, uid, mid, rating = line
				if id == -1:
					f.write("Id,rating\n")
					continue
				f.write("%s,%s\n" % (id, rating))
			f.close()	


class User:
	def __init__(self, datafile, train, test):
		self.id = []
		self.gender = []
		self.age = []
		self.occupation = []
		self.alabel = []
		self.olabel = []
		self.line = [-1]
		with open(datafile) as ifile:
			total = 0
			skip = 0
			lc = 0
			for line in ifile:
				lc += 1
				if lc == 1:
					continue
				cols = line.strip().split(',')
				id = int(cols[0])
				self.line.append(id)
				if id >= len(self.id):
					for i in range(len(self.id), id + 1):
						self.id.append(-1)
						self.gender.append(-1)
						self.age.append(-1)
						self.occupation.append(-1)
				self.id[id] = id
				if cols[1] in ('M', 'f'):
					self.gender[id] = 0
				elif cols[1] in ('F', 'f'):
					self.gender[id] = 1
				try:
					age = int(cols[2])
					if age not in self.alabel:
						self.alabel.append(age)
					self.age[id] = self.alabel.index(age)
				except ValueError:
					pass
				try:
					occupation = int(cols[3])
					if occupation not in self.olabel:
						self.olabel.append(occupation)
					self.occupation[id] = self.olabel.index(occupation)
				except ValueError:
					pass
				if not train.is_uid(id) and not test.is_uid(id):
					skip += 1
					#self.id[id] = -2
					continue
				total += 1
		print 'Uesr Total:', total, '  Skiped:', skip, '  Invalid:', len(self.id) - total

	def get(self, id):
		if id < len(self.id):
			age = self.age[id]
			if age != -1:
				age = self.alabel[age]
			occupation = self.occupation[id]
			if occupation != -1:
				occupation = self.olabel[occupation]
			return [self.id[id], self.gender[id], age, occupation]
		return [-1, -1, -1, -1]

	def id_used(self, id):
		return self.id[id] >= 0

	def write(self, datafile):
		genders = ['M', 'F', 'N/A']
		ages = list(self.alabel)
		ages.append('N/A')
		occupations = list(self.olabel)
		occupations.append('N/A')
		with open(datafile, 'w') as f:
			for id in self.line:
				if id == -1:
					f.write("ID,Gender,Age,Occupation\n")
					continue
				if self.id[id] == -1:
					print 'Something wrong ....'
					break;
				gender = genders[self.gender[id]]
				age = ages[self.age[id]]
				occupation = occupations[self.occupation[id]]
				f.write("%s,%s,%s,%s\n" % (id, gender, age, occupation))
			f.close()	


class Movie:
	def __init__(self, datafile, train, test):
		self.id = []
		self.year = []
		self.ylabel = ['1999~', '1998~1995', '1994~1990', '1989~1980', '~1979']
		self.genre = []
		self.glabel = []
		self.line = [[-1, -1]]
		with open(datafile) as ifile:
			total = 0
			skip = 0
			lc = 0
			for line in ifile:
				lc += 1
				if lc == 1:
					continue
				cols = line.strip().split(',')
				id = int(cols[0])
				if id >= len(self.id):
					for i in range(len(self.id), id + 1):
						self.id.append(-1)
						self.year.append(-1)
						self.genre.append([])
				self.id[id] = id
				year = -1
				try:
					year = int(cols[1])
					if year > 1998:
						y = 0
					elif year > 1994:
						y = 1
					elif year > 1989:
						y = 2
					elif year > 1979:
						y = 3
					else:
						y = 4
					self.year[id] = y
				except ValueError:
					pass
				gens = cols[2].split('|')
				if gens[0].upper() != 'N/A':
					for g in gens:
						if g not in self.glabel:
							self.glabel.append(g)
						self.genre[id].append(self.glabel.index(g))
				self.line.append([id, year])
				if not train.is_mid(id) and not test.is_mid(id):
					skip += 1
					self.id[id] = -2
					continue
				total += 1
		print 'Movie Total:', total, '  Skiped:', skip, '  Invalid:', len(self.id) - total

	def get(self, id):
		if id < len(self.id):
			return [self.id[id], self.year[id], self.genre[id]]
		return [-1, -1, []]

	def id_used(self, id):
		return self.id[id] >= 0
		
	def write(self, datafile):
		years = ['1999', '1996', '1991', '1984', '1975', 'N/A']
		with open(datafile, 'w') as f:
			for line in self.line:
				id, year = line
				if id == -1:
					f.write("Id,Year,Genre\n")
					continue
				if self.id[id] == -1:
					print 'Something wrong ....'
					break;
				if self.id[id] == -2:
					if year == -1:
						ystr = 'N/A'
					else:
						ystr = year
				else:
					if year == -1:
						ystr = years[self.year[id]]
					else:
						ystr = year
				gstr = ""
				if len(self.genre[id]) > 0:
					tag = False;
					for g in self.genre[id]:
						if tag:
							gstr = gstr + "|"
						tag = True
						gstr = gstr + self.glabel[g]
				else:
					gstr = 'N/A'
				f.write("%s,%s,%s\n" % (id, ystr, gstr))
			f.close()	
				
				
				
				