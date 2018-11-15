from graphics import *

class Unit():

	def __init__(self, position):
		self.position = position


class Player(Unit):

	def __init__(self, position, speed):
		Unit.__init__(self, position)
		self.speed = speed
		self.image = Image(position, "assets/player_ship_50.gif")
		self.radius = 20
		self.lives = 3

	def move(self, key):
		# Moves player image based on keypress & updates position value.
		d = self.speed
		x = self.position.getX()
		y = self.position.getY()

		if ((key == "W" or key == "w") and y > 0):
			self.image.move(0, -d)
			self.position = Point(x, y - d)

		elif ((key == "S" or key == "s") and y < 660):
			self.image.move(0, d)
			self.position = Point(x, y + d)

		elif ((key == "A" or key == "a") and x > 0):
			self.image.move(-d, 0)
			self.position = Point(x - d, y)

		elif ((key == "D" or key == "d") and x < 440):
			self.image.move(d, 0)
			self.position = Point(x + d, y)

		return


class Projectile():

	"""Generic base class for all enemy attack components."""

	def __init__(self, position, speed, direction):
		self.position = position
		self.speed = speed
		self.direction = direction


class Bullet(Projectile):

	"""A bullet is a basic circular projectile with a given position, speed, and direction."""

	def __init__(self, position, speed, direction):
		Projectile.__init__(self, position, speed, direction)
		self.radius = 5
		self.image = Circle(position, self.radius)
		self.image.setFill("white")

	def draw(self, window):
		self.image.draw(window)

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


#class NewGameButton():

#	""" Buttons are centered to an anchor. Switches: new"""

#	def __init__(self, anchor):
#		self.anchor = anchor
#		self.panel = Image(anchor)
#		pass





class StartMenu():
	def __init__(self):
		self.namePlate = Image(Point(220, 180), "assets/nameplate01.gif")
		self.startButton = Image(Point(220, 380), "assets/menubutton01.gif")
		self.startLabel = Image(Point(220, 380), "assets/newgametext2.gif")
		self.scoreButton = Image(Point(220, 430), "assets/menubutton01.gif")
		self.exitButton = Image(Point(220, 480), "assets/menubutton01.gif")

	def draw(self, window):
		self.namePlate.draw(window)
		self.startButton.draw(window)
		self.startLabel.draw(window)
		self.scoreButton.draw(window)
		self.exitButton.draw(window)
		return

	def undraw(self):
		self.namePlate.undraw()
		self.startButton.undraw()
		self.startLabel.undraw()
		self.scoreButton.undraw()
		self.exitButton.undraw()
		return