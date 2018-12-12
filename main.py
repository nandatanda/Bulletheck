from random import randint
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
		menu.main(window)

		player.score = 0
		player.lives = 4
		patternNumber = 0
		nextSpawn = randint(125, 160)

		player = engine.Player(playerSpawn, playerSpeed)

		player.draw(window)
		hud.draw(window)

		hud.update_bar(window, player)
		hud.update_score(window, player.score)

		patternList = list()

		while (player.lives > 0):
			# Game loop starts here.

			if (player.score % nextSpawn == 0):
				nextSpawn = randint(125, 160)
				patternList.append(engine.build_attack())

			player.hit = False
			player.move(window.checkKey())
			for i in range (len(patternList)):
				patternList[i].fire(window)
				patternList[i].move()
				if (patternList[i].detect_hit(player)):
					player.hit = True

			player.score = player.score + 1

			player.update_hitframes()
			player.update_lives()
			player.update_shield(window)

			hud.update_bar(window, player)
			hud.update_score(window, player.score)


			if (player.lives == 0):
				for i in range (len(patternList)):
					patternList[i].undraw()

				player.undraw()
				hud.undraw(window)

				menu.game_over(window, player.score)

			graphics.update(30)
			# Game loop ends here.

	return

main()