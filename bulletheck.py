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

	bullet1 = Bullet(Point(50, 50), 2, Point(.2,1))
	bullet2 = Bullet(Point(50, 50), 3, Point(.3,1))
	bullet3 = Bullet(Point(50, 50), 4, Point(.4,1))
	bullet4 = Bullet(Point(50, 50), 5, Point(.5,1))
	bullet5 = Bullet(Point(50, 50), 6, Point(.6,1))
	bullet6 = Bullet(Point(400, 50), 6, Point(-.6,1))
	bullet7 = Bullet(Point(400, 50), 5, Point(-.5,1))
	bullet1.draw(window)
	bullet2.draw(window)
	bullet3.draw(window)
	bullet4.draw(window)
	bullet5.draw(window)
	bullet6.draw(window)
	bullet7.draw(window)

	x = True
	while (x):
		player.move(window.checkKey())
		bullet1.move()
		bullet2.move()
		bullet3.move()
		bullet4.move()
		bullet5.move()
		bullet6.move()
		bullet7.move()

		q=bullet1.detect_hit(player)
		if(q==True):
			print("COLLISION!")
			window.getKey()
		q=bullet2.detect_hit(player)
		if(q==True):
			print("COLLISION!")
			window.getKey()
		q=bullet3.detect_hit(player)
		if(q==True):
			print("COLLISION!")
			window.getKey()
		q=bullet4.detect_hit(player)
		if(q==True):
			print("COLLISION!")
			window.getKey()
		q=bullet5.detect_hit(player)
		if(q==True):
			print("COLLISION!")
			window.getKey()
		q=bullet6.detect_hit(player)
		if(q==True):
			print("COLLISION!")
			window.getKey()
		q=bullet7.detect_hit(player)
		if(q==True):
			print("COLLISION!")
			window.getKey()

		update(30)

main()