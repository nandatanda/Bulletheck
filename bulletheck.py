from graphics import *
from methods import *

def main():
	winX = 440
	winY = 660
	winCenter = Point(winX / 2, winY / 2)
	winName = "| bullet.heck |"
	player_speed = 20
	player_spawn = Point(winX / 2, winY * (2/3))

	window = GraphWin(winName, winX, winY, autoflush=False)

	wallpaper = Image(winCenter, "space.gif")
	wallpaper.draw(window)

	player = Player(player_spawn, player_speed)
	player.image.draw(window)

	attack1 = LineAttack(Point(220,-50), 25, 100, 3, Point(.3,1))
	attack2 = LineAttack(Point(220,-50), 25, 100, 3, Point(-.3,1))
	attack3 = LineAttack(Point(220,-50), 30, 100, 7, Point(.1,1))
	attack4 = LineAttack(Point(220,-50), 45, 100, 7, Point(-.1,1))
	attack5 = LineAttack(Point(220,-50), 53, 100, 8, Point(0,1))


	x = True
	while (x):
		# Game loop starts here.
		attack1.fire(window)
		attack1.move()
		if (attack1.detect_hit(player)):
			print("COLLISION!!!")
			window.getKey()
		attack2.fire(window)
		attack2.move()
		if (attack2.detect_hit(player)):
			print("COLLISION!!!")
			window.getKey()
		attack3.fire(window)
		attack3.move()
		if (attack3.detect_hit(player)):
			print("COLLISION!!!")
			window.getKey()
		attack4.fire(window)
		attack4.move()
		if (attack4.detect_hit(player)):
			print("COLLISION!!!")
			window.getKey()
		attack5.fire(window)
		attack5.move()
		if (attack5.detect_hit(player)):
			print("COLLISION!!!")
			window.getKey()

		player.move(window.checkKey())

		update(30)

main()