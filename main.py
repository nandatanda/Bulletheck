import graphics
import engine

def main():
	winX = 440
	winY = 660
	winCenter = graphics.Point(winX / 2, winY / 2)
	winName = "| bullet.heck |"
	player_speed = 20
	player_spawn = graphics.Point(winX / 2, winY * (2/3))

	window = graphics.GraphWin(winName, winX, winY, autoflush=False)
	menu = engine.Menu()

	wallpaper = graphics.Image(winCenter, "assets/space.gif")
	wallpaper.draw(window)

	menu.run(window)

	player = engine.Player(player_spawn, player_speed)
	player.image.draw(window)

	attack1 = engine.Line(graphics.Point(220,-50), 25, 3, 100, graphics.Point(.3,1))
	attack2 = engine.Line(graphics.Point(220,-50), 25, 6, 100, graphics.Point(-.3,1))
	attack3 = engine.Line(graphics.Point(220,-50), 30, 7, 100, graphics.Point(.1,1))
	attack4 = engine.Line(graphics.Point(220,-50), 45, 3, 100, graphics.Point(-.1,1))
	attack5 = engine.Line(graphics.Point(220,-50), 53, 5, 100, graphics.Point(0,1))

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

		graphics.update(30)
		# loop ends here

main()