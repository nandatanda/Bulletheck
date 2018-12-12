from graphics import *
from random import randint, choice

class Player():

	def __init__(self, position, speed):
		self.position = position
		self.speed = speed
		self.image = Image(position, "assets/ship_50x50.gif")
		self.hit = False
		self.radius = 20
		self.lives = 4
		self.hitframes = 0
		self.shieldtime = 45
		self.score = 0

		self.shield = Circle(self.position, self.radius + 10)
		self.shield.setOutline("red")

	def draw(self, window):
		self.image.draw(window)

		return

	def undraw(self):
		self.image.undraw()

		return

	def move(self, key):
		# Moves player image and shield based on keypress & updates position value.
		d = self.speed
		x = self.position.getX()
		y = self.position.getY()

		if ((key == "W" or key == "w") and y > 0):
			self.image.move(0, -d)
			self.shield.move(0, -d)
			self.position = Point(x, y - d)

		elif ((key == "S" or key == "s") and y < 660):
			self.image.move(0, d)
			self.shield.move(0, d)
			self.position = Point(x, y + d)

		elif ((key == "A" or key == "a") and x > 0):
			self.image.move(-d, 0)
			self.shield.move(-d, 0)
			self.position = Point(x - d, y)

		elif ((key == "D" or key == "d") and x < 440):
			self.image.move(d, 0)
			self.shield.move(d, 0)
			self.position = Point(x + d, y)

		return

	def update_hitframes(self):
		if (self.hitframes == 0):
			if (self.hit):
				self.hitframes = self.hitframes + 1

		elif (0 < self.hitframes < self.shieldtime):
			self.hitframes = self.hitframes + 1

		elif (self.hitframes == self.shieldtime):
			self.hitframes = 0

		return

	def update_lives(self):
		if (self.hitframes == 1):
			self.lives = self.lives - 1

		elif (self.score % 500 == 0):
			if (self.lives < 4):
				self.lives = self.lives + 1

			return

	def update_shield(self, window):
		if (self.hitframes == 1):
			if(self.lives > 0):
				self.shield.draw(window)

		if (self.hitframes == 45):
			self.shield.undraw()

		return


class Bullet():

	"""A bullet is a basic circular projectile with a given position, speed, and direction."""

	def __init__(self, position, speed, direction):
		self.position = position
		self.speed = speed
		self.direction = direction
		self.radius = 5
		self.image = Circle(position, self.radius)
		self.image.setFill("white")

	def draw(self, window):
		self.image.draw(window)

		return

	def undraw(self):
		self.image.undraw()

		return

	def move(self):
		# Moves image and updates position value.
		px = self.position.getX()
		py = self.position.getY()
		dx = self.direction.getX() * self.speed
		dy = self.direction.getY() * self.speed

		self.image.move(dx, dy)
		self.position = Point(px + dx, py + dy)

		return

	def detect_hit(self, player):
		# Returns whether the object body has entered given player.
		px = player.position.getX()
		py = player.position.getY()
		bx = self.position.getX()
		by = self.position.getY()
		pr = player.radius
		br = self.radius

		dx = abs(px - bx)
		dy = abs(py - by)

		if (dx + dy <= pr + br):
			return True

		return False


class Pattern():

	"""Generic base class for all enemy attack patterns. Attacks spawn from a given location and consist of projectile objects."""

	def __init__(self, position, rof, speed):
		self.position = position
		self.rof = rof
		self.speed = speed


class Line(Pattern):

	"""Straight attacks consist of a number of bullets travelling in a single direction at a fixed speed and rof of fire."""

	def __init__(self, position, rof, speed, number, direction):
		Pattern.__init__(self, position, rof, speed)
		self.number = number
		self.direction = direction
		self.list = list()
		self.frame = 0
		self.bullet = 0

		for i in range (number):
			self.list.append(Bullet(position, speed, direction))

	def fire(self, window):
		if (self.bullet == self.number):
			pass
		elif (self.frame % self.rof == 0):
			self.list[self.bullet].draw(window)
			self.bullet = self.bullet + 1

		return

	def move(self):
		for i in range (self.bullet):
			self.list[i].move()

		self.frame = self.frame + 1

		return

	def undraw(self):
		for i in range (self.bullet):
			self.list[i].undraw()

		return

	def detect_hit(self, player):
		for i in range (self.bullet):
			if (self.list[i].detect_hit(player)):
				return True

		return False

class Step(Pattern):
	def __init__(self, position, rof, speed, number, direction):
		Pattern.__init__(self, position, rof, speed)
		self.number = number
		self.direction = direction
		self.list = list()
		self.frame = 0
		self.bullet = 0
		self.step = 30

		for i in range (number):
			self.list.append(Bullet(position, speed, Point(0,1)))

			if (direction == "left"):
				position = Point(position.getX() - self.step, 0)
			elif (direction == "right"):
				position = Point(position.getX() + self.step, 0)

	def fire(self, window):
		if (self.bullet == self.number):
			pass
		elif (self.frame % self.rof == 0):
			self.list[self.bullet].draw(window)
			self.bullet = self.bullet + 1

		return

	def move(self):
		for i in range (self.bullet):
			self.list[i].move()

		self.frame = self.frame + 1

		return

	def detect_hit(self, player):
		for i in range (self.bullet):
			if (self.list[i].detect_hit(player)):
				return True

		return False

	def undraw(self):
		for i in range (len(self.list)):
			self.list[i].undraw()

		return

class CrissCross():

	"""Width can be 'narrow', 'medium', or 'wide', and speed can be 'fast', 'medium', or 'slow'."""

	def __init__(self, width, speed):
		self.width = width
		self.speed = speed
		self.framesElapsed = 0

		if (width == 'narrow'):
			aStart = Point(160, 0)
			bStart = Point(280, 0)
			self.number = 4
		elif (width == 'medium'):
			aStart = Point(100, 0)
			bStart = Point(340, 0)
			self.number = 8
		elif (width == 'wide'):
			aStart = Point(40, 0)
			bStart = Point(400, 0)
			self.number = 12

		if (speed == 'fast'):
			pipSpeed = 9
			self.cooldown = 8
		elif (speed == 'medium'):
			pipSpeed = 7
			self.cooldown = 16
		elif (speed == 'slow'):
			pipSpeed = 5
			self.cooldown = 24

		self.criss = Step(aStart, self.cooldown, pipSpeed, self.number, "right")
		self.cross = Step(bStart, self.cooldown, pipSpeed, self.number, "left")

	def fire(self, window):
		if (self.criss.bullet == self.number):
			pass
		elif (self.framesElapsed % self.cooldown == 0):
			self.criss.list[self.criss.bullet].draw(window)
			self.criss.bullet = self.criss.bullet + 1

		if (self.cross.bullet == self.number):
			pass
		elif (self.framesElapsed % self.cooldown == 0):
			self.cross.list[self.cross.bullet].draw(window)
			self.cross.bullet = self.cross.bullet + 1

		return

	def move(self):
		for i in range (self.criss.bullet):
			self.criss.list[i].move()
		for i in range (self.cross.bullet):
			self.cross.list[i].move()

		self.framesElapsed = self.framesElapsed + 1

		return

	def detect_hit(self, player):
		for i in range (self.criss.bullet):
			if (self.criss.list[i].detect_hit(player)):
				return True

		for i in range (self.cross.bullet):
			if (self.cross.list[i].detect_hit(player)):
				return True

		return False

	def undraw(self):
		for i in range (self.criss.bullet):
			self.criss.list[i].undraw()
		for i in range (self.cross.bullet):
			self.cross.list[i].undraw()


class Spiral():
	def __init__(self, position, rotations, speed):
		self.speed = speed
		self.position = position
		self.drawn = 0
		self.framesElapsed = 0

		self.mylist = list()

		spawns = {
			1 : Point(124, 0),
			2 : Point(186, 0),
			3 : Point(248, 0),
			4 : Point(310, 0),
			5 : Point(372, 0)}

		if (speed == 'fast'):
			pipSpeed = 9
			self.cooldown = 1
		elif (speed == 'medium'):
			pipSpeed = 7
			self.cooldown = 3
		elif (speed == 'slow'):
			pipSpeed = 5
			self.cooldown = 5

		for i in range (rotations):
			for n in range (9):
				offset = (n * .1)
				self.mylist.append(Bullet(spawns.get(position), pipSpeed, Point(offset, -1 + offset)))
				self.mylist.append(Bullet(spawns.get(position), pipSpeed, Point(1 - offset, offset)))
				self.mylist.append(Bullet(spawns.get(position), pipSpeed, Point(-offset, 1 - offset)))
				self.mylist.append(Bullet(spawns.get(position), pipSpeed, Point(-1 + offset, offset)))

	def fire(self, window):
		cooldown = self.cooldown

		if (self.drawn == len(self.mylist)):
			pass
		elif (self.framesElapsed % cooldown == 0):
			self.mylist[self.drawn].draw(window)
			self.drawn = self.drawn + 1

			return

	def move(self):
		for i in range (self.drawn):
			self.mylist[i].move()

		self.framesElapsed = self.framesElapsed + 1

		return

	def detect_hit(self, player):
		for i in range (self.drawn):
			if (self.mylist[i].detect_hit(player)):
				return True

		return False

	def undraw(self):
		for i in range (self.drawn):
			self.mylist[i].undraw()

		return


class Menu():
	def __init__(self):
		self.logo = Image(Point(220, 160), "assets/logo_120x120.gif")
		self.namePlate = Image(Point(220, 160), "assets/name_180_x_60.gif")

		self.startButton = Image(Point(220, 380), "assets/box_120x40.gif")
		self.startLabel = Image(Point(220, 380), "assets/newgametext01.gif")

		self.scoreButton = Image(Point(220, 430), "assets/box_120x40.gif")
		self.scoreLabel = Image(Point(220, 430), "assets/highscorestext01.gif")
		self.scorePlate = Image(Point(220, 430), "assets/box_400x300.gif")
		self.scoreTitle = Text(Point(220, 310), "[TOP 5]")
		self.scoreTitle.setFill("red")

		self.exitButton = Image(Point(220, 480), "assets/box_120x40.gif")
		self.exitLabel = Image(Point(220, 480), "assets/exittext01.gif")

		self.isOpen = False

	def draw_main(self, window):
		self.logo.draw(window)
		self.namePlate.draw(window)
		self.startButton.draw(window)
		self.startLabel.draw(window)
		self.scoreButton.draw(window)
		self.scoreLabel.draw(window)
		self.exitButton.draw(window)
		self.exitLabel.draw(window)
		self.isOpen = True

		return

	def undraw_main(self):
		self.logo.undraw()
		self.namePlate.undraw()
		self.startButton.undraw()
		self.startLabel.undraw()
		self.scoreButton.undraw()
		self.scoreLabel.undraw()
		self.exitButton.undraw()
		self.exitLabel.undraw()
		self.isOpen = False

		return

	def check_start(self, click):
		clickX = click.getX()
		clickY = click.getY()

		if (160 < clickX < 280):
			if (360 < clickY < 400):
				return True
		return False

	def check_scores(self, click):
		clickX = click.getX()
		clickY = click.getY()

		if (160 < clickX < 280):
			if (410 < clickY < 450):
				return True
		return False

	def check_exit(self, click):
		clickX = click.getX()
		clickY = click.getY()

		if (160 < clickX < 280):
			if (460 < clickY < 500):
				return True
		return False

	def check_x(self, click, adjustment):
		clickX = click.getX()
		clickY = click.getY()

		if (347.5 < clickX < 372.5):
			if (347.5 - adjustment < clickY < 372.5 + adjustment):
				return True
		return False

	def draw_scores(self, window):
		self.file = File("scores.txt")
		self.listScore = self.file.get_scores()
		self.listName = self.file.get_names()
		self.count = 5

		self.anchorScore = Point(60,360)
		self.anchorName = Point(220,360)
		self.textScore = list()
		self.textName = list()

		self.scorePlate.draw(window)
		self.scoreTitle.draw(window)

		for i in range (self.count): 
			self.textScore.append(Text(self.anchorScore, self.listScore[i]))
			self.textScore[i].setFill("white")
			self.anchorScore.move(0, 40)
			self.textScore[i].draw(window)

			self.textName.append(Text(self.anchorName, self.listName[i]))
			self.textName[i].setFill("white")
			self.anchorName.move(0, 40)
			self.textName[i].draw(window)

		return

	def undraw_scores(self):
		for i in range (self.count):
			self.textScore[i].undraw()
			self.textName[i].undraw()

		self.logo.undraw()
		self.namePlate.undraw()
		self.scorePlate.undraw()
		self.scoreTitle.undraw()

		return

	def main(self, window):
		self.draw_main(window)

		while (self.isOpen):
			click = window.checkMouse()

			if (click):
				if (self.check_start(click)):
					self.undraw_main()
					return

				elif (self.check_scores(click)):
					self.undraw_main()
					self.logo.draw(window)
					self.namePlate.draw(window)
					self.draw_scores(window)

					window.getMouse()

					self.undraw_scores()
					self.draw_main(window)

				elif (self.check_exit(click)):
					self.undraw_main()
					quit()

		return

	def new_score(self, window, score, rank):
			self.isOpen = True
			self.adjustment = 40 * self.rank

			self.newScorePosition = Point(60, 360 + self.adjustment)
			self.scoreTitle = Text(Point(220, 310), "[NEW HIGH SCORE]")
			self.scoreTitle.setFill("red")

			defaultMessage = "Enter name and hit 'return'"

			self.newNamePosition = Point(220, 360 + self.adjustment)
			self.nameEntry = Entry(self.newNamePosition, 20)
			self.nameEntry.setFill("black")
			self.nameEntry.setTextColor("white")
			self.nameEntry.setText(defaultMessage)

			self.nameButton = Image(Point(360, 360 + self.adjustment), "assets/buttons/x_25x25.gif")

			self.draw_scores(window)
			self.nameEntry.draw(window)
			self.nameButton.draw(window)

			self.textName[self.rank].undraw()
			self.textScore[self.rank].undraw()
			self.textScore[self.rank] = Text(self.newScorePosition, score)
			self.textScore[self.rank].setFill("white")
			self.textScore[self.rank].draw(window)

			while(self.isOpen):
				click = window.checkMouse()
				press = window.checkKey()

				if (click):
					if (self.check_x(click, self.adjustment)):
						self.nameEntry.setText("")
				if (press):
					if (press == "Return"):
						name = self.nameEntry.getText()
						self.file.add_entry(score, name)
						self.nameButton.undraw()
						self.nameEntry.undraw()
						self.nameEntry = Text(self.newNamePosition, name)
						self.nameEntry.setFill("white")
						self.nameEntry.draw(window)
						while (True):
							click = window.checkMouse()
							press = window.checkKey()
							if (click or press):
								self.scoreTitle.undraw()
								self.nameEntry.undraw()
								self.scoreTitle = Text(Point(220, 310), "[TOP 5]")
								self.scoreTitle.setFill("red")
								return
					elif (self.nameEntry.getText() == press + defaultMessage):
						self.nameEntry.setText(press)

	def game_over(self, window, score):
		self.file = File("scores.txt")
		self.rank = self.file.rank_score(score)

		self.logo.draw(window)
		self.namePlate.draw(window)

		if (self.rank < 5):
			self.new_score(window, score, self.rank)
			self.undraw_scores()

		self.logo.undraw()
		self.namePlate.undraw()

		return


class Hud():
	def __init__(self):
		self.bar = Image(Point(360, 25), "assets/shield/bar_sized_01.gif")
		self.score = Text(Point(40, 25), 0)
		self.gameOverText = Image(Point(220, 330), "assets/gameover_sized.gif")
		self.menuButton = Image(Point(220,430), "assets/box_120x40.gif")

		self.score.setTextColor("white")


	def draw(self, window):
		self.bar.draw(window)
		self.score.draw(window)

	def update_bar(self, window, player):
		self.bar.undraw()

		if (player.lives == 4):
			self.bar = Image(Point(360, 25), "assets/shield/bar_sized_01.gif")
		if (player.lives == 3):
			self.bar = Image(Point(360, 25), "assets/shield/bar_sized_02.gif")
		if (player.lives == 2):
			self.bar = Image(Point(360, 25), "assets/shield/bar_sized_03.gif")
		if (player.lives == 1):
			self.bar = Image(Point(360, 25), "assets/shield/bar_sized_04.gif")

		self.bar.draw(window)

		return

	def update_score(self, window, score):
		self.score.undraw()
		self.score = Text(Point(40, 25), score)
		self.score.setTextColor("white")
		self.score.draw(window)

		return

	def undraw(self, window):
		self.score.undraw()
		self.bar.undraw()

		return


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

	def rank_score(self, score):
		with open(self.source, 'r') as f:
			self.mylist = f.read().splitlines()

		self.mylist.sort(reverse = True)

		for i in range (len(self.mylist)):
			self.mylist[i] = int(self.mylist[i].split(',')[0])

		for i in range (len(self.mylist)):
			if (score > self.mylist[i]):
				return i

		return len(self.mylist)


def build_attack():
	crisscrosses = {
		1 : CrissCross('narrow', 'fast'),
		2 : CrissCross('narrow', 'medium'),
		3 : CrissCross('narrow', 'slow'),
		4 : CrissCross('medium', 'fast'),
		5 : CrissCross('medium', 'medium'),
		6 : CrissCross('medium', 'slow'),
		7 : CrissCross('wide', 'fast'),
		8 : CrissCross('wide', 'medium'),
		9 : CrissCross('wide', 'slow')}

	point = Point(randint(20, 420), 0)
	cooldown = randint(9, 13)
	speed = randint(5, 9)
	number = randint(6, 12)
	directions = ['left', 'right']
	direction = choice(directions)

	steps = {
		1 : Step(point, cooldown, speed, number, direction),
		2 : Step(Point(420,0), cooldown, speed, 14, 'left'),
		3 : Step(Point(20,0), cooldown, speed, 14, 'right'),
		4 : Step(Point(220,0), cooldown, speed, number, direction)}

	point = randint(1, 5)
	rotations = randint(5, 10)
	speeds = ['fast', 'slow']
	speed = choice(speeds)

	spiral = Spiral(point, rotations, speed)

	type = ['crisscross', 'step', 'spiral']
	type = choice(type)

	if (type == 'crisscross'):
		return crisscrosses.get(randint(1, 9))
	elif (type == 'step'):
		return steps.get(randint(1, 4))
	elif (type == 'spiral'):
		return spiral