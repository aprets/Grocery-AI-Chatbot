from dialogue.manager import DialogueManager

dm = DialogueManager()

print('BOT: HELLO I AM BOT?')

while True:
	user_input = input("YOU: ")
	bot_response = dm.run_state(user_input)
	print(f'BOT: {bot_response}')