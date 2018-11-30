from graphics import *

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
	def __init__(self, position, rof, speed, number):
		Pattern.__init__(self, position, rof, speed)
		self.number = number
		self.list = list()
		self.frame = 0
		self.bullet = 0
		self.step = 0

		for i in range (number):
			self.list.append(Bullet(position, speed, direction))
			self.step = self.step + 20
	pass


class Menu():
	def __init__(self):
		self.logo = Image(Point(220, 160), "assets/logo_120x120.gif")
		self.namePlate = Image(Point(220, 160), "assets/name_180_x_60.gif")
		self.startButton = Image(Point(220, 380), "assets/box_120x40.gif")
		self.startLabel = Image(Point(220, 380), "assets/newgametext01.gif")
		self.scoreButton = Image(Point(220, 430), "assets/box_120x40.gif")
		self.scoreLabel = Image(Point(220, 430), "assets/highscorestext01.gif")
		
		
		self.scorePlate = Image(Point(220, 430), "assets/box_400x300.gif")
		self.exitButton = Image(Point(220, 480), "assets/box_120x40.gif")
		self.exitLabel = Image(Point(220, 480), "assets/exittext01.gif")
		self.isOpen = False

	def draw(self, window):
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

	def undraw(self):
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

	def show_scores(self, window):
		self.file = File("scores.txt")
		self.listScore = self.file.get_scores()
		self.listName = self.file.get_names()
		self.count = 5

		self.anchorScore = Point(60,350)
		self.anchorName = Point(220,350)
		self.textScore = list()
		self.textName = list()

		self.logo.draw(window)
		self.namePlate.draw(window)
		self.scorePlate.draw(window)

		for i in range (self.count): 
			self.textScore.append(Text(self.anchorScore, self.listScore[i]))
			self.textScore[i].setFill("white")
			self.anchorScore.move(0, 40)
			self.textScore[i].draw(window)

			self.textName.append(Text(self.anchorName, self.listName[i]))
			self.textName[i].setFill("white")
			self.anchorName.move(0, 40)
			self.textName[i].draw(window)

		window.getMouse()

		for i in range (self.count):
			self.textScore[i].undraw()
			self.textName[i].undraw()

		self.logo.undraw()
		self.scorePlate.undraw()
		self.namePlate.undraw()

		return

	def run(self, window):
		self.draw(window)

		while (self.isOpen):
			click = window.checkMouse()

			if (click):
				if (self.check_start(click)):
					self.undraw()
					return
				elif (self.check_scores(click)):
					self.undraw()
					self.show_scores(window)
					self.draw(window)
				elif (self.check_exit(click)):
					self.undraw()
					quit()

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

	def game_over(self, window):
		self.waiting = True

		self.score.undraw()
		self.bar.undraw()

		self.gameOverText.draw(window)
		self.menuButton.draw(window)

		while (self.waiting):
			self.click = window.getMouse()
			self.clickX = self.click.getX()
			self.clickY = self.click.getY()

			if (160 < self.clickX < 280):
				if (410 < self.clickY < 450):
					self.gameOverText.undraw()
					self.menuButton.undraw()
					self.waiting = False

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