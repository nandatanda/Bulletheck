from graphics import *

class Unit():

	def __init__(self, position):
		self.position = position


class Player(Unit):

	def __init__(self, position, speed):
		Unit.__init__(self, position)
		self.speed = speed
		self.image = Image(position, "player_ship_50.gif")
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


class Mob(Unit):
	def __init__(self, speed):
		Unit.__init(self, speed)


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

	def move(self):
		# Moves image and updates position value.
		px = self.position.getX()
		py = self.position.getY()
		dx = self.direction.getX() * self.speed
		dy = self.direction.getY() * self.speed

		self.image.move(dx, dy)
		self.position = Point(px + dx, py + dy)

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


class Attack():

	"""Generic base class for all enemy attack patterns. Attacks spawn from a given location and consist of projectile objects."""

	def __init__(self, position, rate):
		self.position = position
		self.rate = rate


class LineAttack(Attack):

	"""Straight attacks consist of a number of bullets travelling in a single direction at a fixed speed and rate of fire."""

	def __init__(self, position, rate, number, speed, direction):
		Attack.__init__(self, position, rate)
		self.number = number
		self.speed = speed
		self.direction = direction
		self.list = list()
		self.frame = 0
		self.bullet = 0

		for i in range (number):
			self.list.append(Bullet(position, speed, direction))

	def fire(self, window):
		if (self.bullet == self.number):
			pass
		elif (self.frame % self.rate == 0):
			self.list[self.bullet].draw(window)
			self.bullet = self.bullet + 1

	def move(self):
		for i in range (self.bullet):
			self.list[i].move()

		self.frame = self.frame + 1

	def detect_hit(self, player):
		for i in range (self.bullet):
			if (self.list[i].detect_hit(player)):
				return True