import graphics
import engine
import random

def build_attack():
	crisscrosses = {
		1 : engine.CrissCross('narrow', 'fast'),
		2 : engine.CrissCross('narrow', 'medium'),
		3 : engine.CrissCross('narrow', 'slow'),
		4 : engine.CrissCross('medium', 'fast'),
		5 : engine.CrissCross('medium', 'medium'),
		6 : engine.CrissCross('medium', 'slow'),
		7 : engine.CrissCross('wide', 'fast'),
		8 : engine.CrissCross('wide', 'medium'),
		9 : engine.CrissCross('wide', 'slow')}

	point = graphics.Point(random.randint(20, 420), 0)
	cooldown = random.randint(9, 13)
	speed = random.randint(5, 9)
	number = random.randint(6, 12)
	direction = ['left', 'right']
	direction = random.choice(direction)

	steps = {
		1 : engine.Step(point, cooldown, speed, number, direction),
		2 : engine.Step(graphics.Point(420,0), cooldown, speed, 14, 'left'),
		3 : engine.Step(graphics.Point(20,0), cooldown, speed, 14, 'right'),
		4 : engine.Step(graphics.Point(220,0), cooldown, speed, number, direction)}

	point = random.randint(1, 5)
	rotations = random.randint(5, 10)
	speed = ['fast', 'slow']
	speed = random.choice(speed)

	spiral = engine.Spiral(point, rotations, speed)

	choice = ['crisscross', 'step', 'spiral']
	choice = random.choice(choice)

	if (choice == 'crisscross'):
		choice = crisscrosses.get(random.randint(1, 9))
	elif (choice == 'step'):
		choice = steps.get(random.randint(1, 4))
	elif (choice == 'spiral'):
		choice = spiral

	return choice

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
		nextSpawn = random.randint(125, 160)

		player = engine.Player(playerSpawn, playerSpeed)

		player.draw(window)
		hud.draw(window)

		hud.update_bar(window, player)
		hud.update_score(window, player.score)

		patternList = list()

		while (player.lives > 0):
			# Game loop starts here.

			if (player.score % nextSpawn == 0):
				nextSpawn = random.randint(125, 160)
				patternList.append(build_attack())

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