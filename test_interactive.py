from dialogue.manager import DialogueManager

dm = DialogueManager()

header = "\noooooooooo.             o8o               .oooooo..o                                                              o8o "+ \
"\n`888'   `Y8b            `\"'              d8P'    `Y8                                                              `YP "+ \
"\n 888     888  .oooo.   oooo  ooo. .oo.   Y88bo.      oooo  oooo  oooo d8b oooo d8b  .ooooo.  oooo    ooo  .oooo.o  '  "+ \
"\n 888oooo888' `P  )88b  `888  `888P\"Y88b   `\"Y8888o.  `888  `888  `888\"\"8P `888\"\"8P d88' `88b  `88.  .8'  d88(  \"8     "+ \
"\n 888    `88b  .oP\"888   888   888   888       `\"Y88b  888   888   888      888     888ooo888   `88..8'   `\"Y88b.      "+ \
"\n 888    .88P d8(  888   888   888   888  oo     .d8P  888   888   888      888     888    .o    `888'    o.  )88b     "+ \
"\no888bood8P'  `Y888\"\"8o o888o o888o o888o 8\"\"88888P'   `V88V\"V8P' d888b    d888b    `Y8bod8P'     .8'     8\"\"888P'     "+ \
"\n                                                                                            .o..P'                   "+ \
"\n                                                                                            `Y8P'                    "+ \
"\n                                                                                                                  "

print(header + "\nWelcome! How can we help you?")

while True:
	user_input = input("YOU: ")
	bot_response = dm.run_state(user_input)
	print(f'BOT: {bot_response}')