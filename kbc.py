import curses
import random


def printPrizeMoney(stdscr, stages, selected):
	for n,stage in enumerate(stages):
		if n == selected:
			stdscr.addstr(15-n, 75, stage, curses.A_STANDOUT)
		elif stage != "Rs. 0":
			stdscr.addstr(15-n, 75, stage)


def print_menu(stdscr, selected, direction=1):
    selected += direction

    curses.curs_set(0)

    if selected == 1:
        stdscr.addstr(5, 10, "Play", curses.A_STANDOUT)
    else:
        stdscr.addstr(5, 10, "Play")
    if selected == 2:
        stdscr.addstr(6, 10, "Background", curses.A_STANDOUT)
    else:
        stdscr.addstr(6, 10, "Background")
    if selected == 3:
        stdscr.addstr(7, 10, "Exit", curses.A_STANDOUT)
    else:
        stdscr.addstr(7, 10, "Exit")

    stdscr.refresh()

    return selected


def play_game(stdscr):
	quiz_data = [
		{
			"question": "Q1. What is the capital of India?",
			"options": ["Nagpur", "Delhi", "Ayodhya", "Mumbai"],
			"answer": "Delhi"
		},
		{
			"question": "Q2. What is the capital of Australia?",
			"options": ["Sydney", "Perth", "Canberra", "Auckland"],
			"answer": "Canberra"
		},
		{
			"question": "Q3. What is the capital of the United Kingdom?",
			"options": ["London", "Windsor", "Edinburgh", "Manchester"],
			"answer": "London"
		},
		{
			"question": "Q4. What is the capital of the USA?",
			"options": ["Washington DC", "New York", "Chicago", "Texas"],
			"answer": "Washington DC"
		},
		{
			"question": "Q5. What is the capital of the Russia?",
			"options": ["Saint Petersburg", "Volgograd", "Kazan", "Moscow"],
			"answer": "Moscow"
		},
		{
			"question": "Q6. Who invented the Light Bulb?",
			"options": ["Leonardo Da Vinci", "Thomas Alva Edison", "Isaac Newton", "Nikola Tesla"],
			"answer": "Thomas Alva Edison"
		},
		{
			"question": "Q7. Which planet is known as the Red Planet?",
			"options": ["Jupiter", "Earth", "Mars", "Mercury"],
			"answer": "Mars"
		},
		{
			"question": "Q8. Who invented the Printing Press?",
			"options": ["William Skeen", "Galileo Galilei", "Johannes Gutenberg", "Leonardo Da Vinci"],
			"answer": "Johannes Gutenberg"
		},
		{
			"question": "Q9.  How many continents are there?",
			"options": ["7", "6", "5", "8"],
			"answer": "7"
		},
		{
			"question": "Q10. What is the National Animal of India?",
			"options": ["Lion", "Tiger", "Elephant", "Leopard"],
			"answer": "Tiger"
		},
		{
			"question": "Q11. How many oceans are there?",
			"options": ["6", "8", "7", "5"],
			"answer": "5"
		},
	]
	# Given: List of prize money which has to be printed on the right side
	prize_money = ["Rs. 0", "Rs. 1000", "Rs. 2000", "Rs. 4000", "Rs. 8000", "Rs. 16000", "Rs. 32000", "Rs. 64000", "Rs. 1 Lakh", "Rs. 2 Lakhs", "Rs. 5 Lakhs", "Rs. 1 Crore"]
	# Given: Dictionary containing the status of lifelines used. FF = 50-50 and AP = Audience Poll
	lifeline_status = {"FF": False, "AP": False, "Quit": False}

	score = 0  # Index number of prize_money list

	for round in quiz_data:
		selected = 0
		hide_indexes = []
		while True:
			stdscr.clear()
			printPrizeMoney(stdscr, prize_money, score+1)
			if selected == -3:
				stdscr.addstr(7, 2, "50:50", curses.A_STANDOUT)
			else:
				stdscr.addstr(7, 2, "50:50")
			if selected == -2:
				stdscr.addstr(7, 12, "Audience Poll", curses.A_STANDOUT)
			else:
				stdscr.addstr(7, 12, "Audience Poll")
			if selected == -1:
				stdscr.addstr(7, 30, "Quit", curses.A_STANDOUT)
			else:
				stdscr.addstr(7, 30, "Quit")
			stdscr.addstr(10, 1, round["question"])
			for i in range(0,4):
				if i in (0,1):  # Left side
					x = 6
				else:  # Right side
					x = 30

				if i in (0,2):  # Upper row
					y = 12
				else:  # Below row
					y = 14

				if selected == i:
					if i not in hide_indexes:
						stdscr.addstr(y, x, round["options"][i], curses.A_STANDOUT)
				else:
					if i not in hide_indexes:
						stdscr.addstr(y, x, round["options"][i])

			key_pressed = stdscr.getkey()
			if key_pressed == "\n":  # if Enter clicked, then choose the option
				if selected >= 0:  # If it is one of the 4 game answer options
					if round["options"][selected] == round["answer"]:
						score += 1
						break
					else:
						if score >= 5:  # If checkpoint has been passed already
							win_money = "Rs. 32,000"
						else:
							win_money = "Rs. 0"
						print_money(stdscr, win_money)
						return

				if selected == -1:  # Exit
					print_money(stdscr, prize_money[score])
					return
				if selected == -2:  # Audience Poll
					if lifeline_status['AP'] is False:
						stdscr.clear()
						right = round["options"].index(round["answer"])  # Get the right answer
						percentage_right = random.randint(51,69)  # Randomly choose a percentage between 51 and 69 for the right answer
						remaining_percentage = 100 - percentage_right
						for i in range(0,4):
							if i == right:  # for the right answer
								stdscr.addstr(i+20, 5, round["options"][i])
								stdscr.addstr(i+20, 20, f"{percentage_right}%")
							elif i == 2 and right == 3:  # if the last option is the right option, show the remaining percentage for the third option
								stdscr.addstr(i+20, 5, round["options"][i])
								stdscr.addstr(i+20, 20, f"{remaining_percentage}%")
							elif i == 3:  # for the last option, just show the remaining percentage
								stdscr.addstr(i+20, 5, round["options"][i])
								stdscr.addstr(i+20, 20, f"{remaining_percentage}%")
							else:  # for all other options choose a random integer less than the remaining percentage and show
								percentage = random.randint(1,remaining_percentage)
								remaining_percentage -= percentage
								stdscr.addstr(i+20, 5, round["options"][i])
								stdscr.addstr(i+20, 20, f"{percentage}%")
						lifeline_status['AP'] = True
						stdscr.getkey()
						stdscr.clear()
					else:
						stdscr.clear()
						stdscr.addstr(20, 20, "You have already used this lifeline!", curses.A_STANDOUT)
						stdscr.getkey()
						stdscr.clear()
				if selected == -3:  # 50-50
					if lifeline_status['FF'] is False:
						right = round["options"].index(round["answer"])
						indexes = [0,1,2,3]
						indexes.remove(right)  # Remove right answer because we don't want to hide the right answer
						hide_indexes = random.sample(indexes, 2)  # Randomly choose 2 options to be hidden when 50-50 is used and store their indexes
						lifeline_status['FF'] = True
					else:
						stdscr.clear()
						stdscr.addstr(20, 20, "You have already used this lifeline!", curses.A_STANDOUT)
						stdscr.getkey()
						stdscr.clear()

			elif (key_pressed == "KEY_DOWN" or key_pressed == "KEY_RIGHT") and selected < 3:
				if (selected + 1) in hide_indexes and selected < 2:
					if (selected + 2) in hide_indexes:
						if (selected + 3) < 4:
							selected += 3
					else:
						selected += 2
				elif (selected + 1) in hide_indexes and selected == 2:
					pass
				else:
					selected += 1
			elif (key_pressed == "KEY_UP" or key_pressed == "KEY_LEFT") and selected > -3:
				if (selected - 1) in hide_indexes:
					if selected-2 in hide_indexes:
						selected -= 3
					else:
						selected -= 2
				else:
					selected -= 1

	print_money(stdscr, "Rs. 1 Crore")
	return


def print_money(stdscr, q_num):
	stdscr.clear()
	stdscr.addstr(18, 20, "GAME OVER!", curses.A_STANDOUT)
	stdscr.addstr(20, 20, f"Congratulations! You have won {q_num}!", curses.A_STANDOUT)
	stdscr.getkey()
	stdscr.clear()


def menu_background(stdscr):
	curses.start_color()
	curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_RED)
	curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_BLUE)
	curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_GREEN)
	curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_YELLOW)
	while True:
		for i in range(1, 5):
			stdscr.bkgd(' ', curses.color_pair(i))
			stdscr.clear()
			stdscr.addstr(5, 10, "Press any key to switch background and Enter Key to select the background", curses.A_STANDOUT)
			stdscr.refresh()
			input_char = stdscr.get_wch()

			if input_char == '\n':  # If Enter is clicked
				stdscr.clear()
				print_menu(stdscr, 1, 1)  # To set to "Background" again
				return


def main(stdscr):
    selected = print_menu(stdscr, -1)
    while True:
        key_pressed = stdscr.getkey()

        if key_pressed == 'KEY_UP' or key_pressed == 'KEY_LEFT':
            if selected > 1:
                selected = print_menu(stdscr, selected, -1)
        elif key_pressed == 'KEY_DOWN' or key_pressed == 'KEY_RIGHT':
            if selected < 3:
                selected = print_menu(stdscr, selected, 1)
        elif key_pressed == "\n":
            if selected == 1:
                play_game(stdscr)
                selected = print_menu(stdscr, -1)
            elif selected == 2:
                menu_background(stdscr)
            elif selected == 3:
                curses.endwin()
                break

        stdscr.refresh()


curses.wrapper(main)
