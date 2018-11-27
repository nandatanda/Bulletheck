class File():
	def __init__(self, source):
		self.source = source

	def get_entries(self):
		with open(self.source) as f:
			self.mylist = f.read().splitlines()

		self.mylist.sort(reverse = True)

		return self.mylist

	def get_scores(self):
		with open(self.source) as f:
			self.mylist = f.read().splitlines()

		self.mylist.sort(reverse = True)

		for i in range (len(self.mylist)):
			self.mylist[i] = self.mylist[i].split(',')[0]

		return self.mylist

	def get_names(self):
		with open(self.source) as f:
			self.mylist = f.read().splitlines()

		self.mylist.sort(reverse = True)

		for i in range (len(self.mylist)):
			self.mylist[i] = self.mylist[i].split(',')[1]
			self.mylist[i] = self.mylist[i].strip()

		return self.mylist

	def add_entry(self, score, name):
		with open(self.source, 'a+') as f:
			f.write('\n' + str(score) + ',' + name)

		return


def main():
	file = File("scores.txt")

	file.add(999, "Spaghetti Man")

	contents = file.list()
	print(contents, '\n')
	contents = file.list_scores()
	print(contents, '\n')
	contents = file.list_names()
	print(contents, '\n')



main()



#		self.stream = open("scores.txt", "r")
#		self.contents = self.stream.readline()