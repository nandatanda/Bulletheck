import graphics
import engine

def main():
	winX = 440
	winY = 660
	winCenter = graphics.Point(winX / 2, winY / 2)
	winName = "| bullet.heck |"

	playerSpeed = 20
	playerSpawn = graphics.Point(winX / 2, winY * (2/3))

	menu = engine.Menu()
	hud = engine.Hud()
	player = engine.Player(playerSpawn, playerSpeed)
	window = graphics.GraphWin(winName, winX, winY, autoflush=False)
	wallpaper = graphics.Image(winCenter, "assets/space.gif")
	window.setBackground("black")
	wallpaper.draw(window)

	while (window):
		menu.run(window)

		player.score = 0
		player.lives = 4

		player = engine.Player(playerSpawn, playerSpeed)

		player.image.draw(window)
		hud.draw(window)

		hud.update_bar(window, player)
		hud.update_score(window, player.score)

		attack1 = engine.Line(graphics.Point(220,-50), 25, 3, 100, graphics.Point(.3,1))
		attack2 = engine.Line(graphics.Point(220,-50), 25, 6, 100, graphics.Point(-.3,1))
		attack3 = engine.Line(graphics.Point(220,-50), 30, 7, 100, graphics.Point(.1,1))
		attack4 = engine.Line(graphics.Point(220,-50), 45, 3, 100, graphics.Point(-.1,1))
		attack5 = engine.Line(graphics.Point(220,-50), 53, 5, 100, graphics.Point(0,1))

		while (player.lives > 0):
			# Game loop starts here.

			player.hit = False
			player.move(window.checkKey())

			attack1.fire(window)
			attack1.move()
			if (attack1.detect_hit(player)):
				player.hit = True

			attack2.fire(window)
			attack2.move()
			if (attack2.detect_hit(player)):
				player.hit = True

			attack3.fire(window)
			attack3.move()
			if (attack3.detect_hit(player)):
				player.hit = True

			attack4.fire(window)
			attack4.move()
			if (attack4.detect_hit(player)):
				player.hit = True

			attack5.fire(window)
			attack5.move()
			if (attack5.detect_hit(player)):
				player.hit = True

			player.score = player.score + 1

			player.update_hitframes()
			player.update_lives()
			player.update_shield(window)

			hud.update_bar(window, player)
			hud.update_score(window, player.score)

			if (player.lives == 0):
				attack1.undraw()
				attack2.undraw()
				attack3.undraw()
				attack4.undraw()
				attack5.undraw()
				hud.game_over(window)
				player.image.undraw()

			graphics.update(30)

	return

main()