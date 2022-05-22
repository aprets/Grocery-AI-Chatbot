from dialogue.manager import DialogueManager

print('EXPECTED')
dm = DialogueManager()
print(dm.run_state("i am 67 avenue road, Guildford, GU27XE"))
print(dm.run_state("yes"))

print(dm.run_state("deliver it at 3pm"))
print(dm.run_state("yes"))

print()
print()

print('NOT CONFIRMED')
dm = DialogueManager()
print(dm.run_state("i am 67 avenue road"))
print(dm.run_state("no"))

print(dm.run_state("i would like to order chicken"))
print(dm.run_state("yes"))

print()
print()

print('USER WANTS SOMETHING ELSE')
dm = DialogueManager()
print(dm.run_state("i am 67 avenue road"))
print(dm.run_state("i would like to order chicken"))
print(dm.run_state("yes"))

print()
print()

print('USER WANTS SOMETHING ELSE NO INTENT')
dm = DialogueManager()
print(dm.run_state("i am 67 avenue road"))
print(dm.run_state("add to basket"))
print(dm.run_state("bread, milk , eggs"))
print(dm.run_state("yes"))

print()
print()

print('Food test')
dm = DialogueManager()
print(dm.run_state("get bread"))
print(dm.run_state("yes"))

# dm.run_state()