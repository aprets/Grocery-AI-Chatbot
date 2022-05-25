import logging
from dialogue.manager import DialogueManager



def run_test(*msgs, name):
	dm = DialogueManager()
	print()
	print()
	print()
	print('-' * 50, f'START TEST {name}', '-' * 50)
	for msg in msgs:
		response = dm.run_state(msg)
		print()
		print(response)
		print()
	print('-' * 50, f'END TEST {name}', '-' * 50)





run_test("i am central avenue, Guildford, GU27XE", "yes", "deliver it at 3pm", "yes", name='BASIC')

run_test("Bread, i am central avenue, Guildford, GU27XE, at 4pm", "yes", "deliver it at 3pm", "yes", name='ODD')

run_test("i am 67 avenue road", "no", "i would like to order chicken", "yes", name='NOT CONFIRMED')

run_test("i am 67 avenue road", "i would like to order chicken", "yes", name='USER WANTS SOMETHING ELSE')

run_test("i am 67 avenue road", "add to basket", "bread, milk , eggs", "yes", name='USER WANTS SOMETHING ELSE NO INTENT')

run_test("get bread", "yes", name='Food test')

run_test("no", "Salmon plz", name='Start with no end with salmon')

run_test("deliver to 25 central avenue, Guildford, GU27XE", name='NER test')

run_test("deliver at 16:00", "yes", "My address is 15 Waltham Avenue Guildford GU27XE", name='Mike test')

run_test("add to bread to basket", "0", "yes","add to bread to basket", "0", "yes", name='Correct select for add_to_basket')

run_test("add to bread to basket", "0", "no", name='Correct select for add_to_basket no')

run_test("add to bread to basket", "0", "yes", "remove bread from basket", "yes", name='Correct select for add_to_basket no')

run_test("remove bread from basket", "yes", name='Correct select for add_to_basket')
