import logging
from dialogue.manager import DialogueManager



def run_test(*msgs, name):
	dm = DialogueManager()
	print()
	print()
	print()
	print()
	logging.debug(f'START TEST - {name}')
	for msg in msgs:
		print(dm.run_state(msg))
	logging.debug(f'EMD TEST - {name}')




run_test("i am central avenue, Guildford, GU27XE", "yes", "deliver it at 3pm", "yes", name='BASIC')

run_test("Bread, i am central avenue, Guildford, GU27XE, at 4pm", "yes", "deliver it at 3pm", "yes", name='ODD')

run_test("i am 67 avenue road", "no", "i would like to order chicken", "yes", name='NOT CONFIRMED')

run_test("i am 67 avenue road", "i would like to order chicken", "yes", name='USER WANTS SOMETHING ELSE')

run_test("i am 67 avenue road", "add to basket", "bread, milk , eggs", "yes", name='USER WANTS SOMETHING ELSE NO INTENT')

run_test("get bread", "yes", name='Food test')

run_test("no", "Salmon plz", name='Start with no end with salmon')

run_test("deliver to 25 central avenue, Guildford, GU27XE", name='NER test')

run_test("deliver at 16:00", "yes", "My address is 15 Waltham Avenue Guildford GU27XE", name='Mike test')