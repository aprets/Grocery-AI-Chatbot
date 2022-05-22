from dialogue.manager import DialogueManager
print()
print()

print('EXPECTED')
dm = DialogueManager()
print(dm.run_state("i am central avenue, Guildford, GU27XE"))
print(dm.run_state("yes"))

print(dm.run_state("deliver it at 3pm"))
print(dm.run_state("yes"))

print()
print()
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
print()
print()

print('USER WANTS SOMETHING ELSE')
dm = DialogueManager()
print(dm.run_state("i am 67 avenue road"))
print(dm.run_state("i would like to order chicken"))
print(dm.run_state("yes"))

print()
print()
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
print()
print()

print('Food test')
dm = DialogueManager()
print(dm.run_state("get bread"))
print(dm.run_state("yes"))

print()
print()
print()
print()

print('No')
dm = DialogueManager()
print(dm.run_state("no"))
print(dm.run_state("Salmon plz"))

print()
print()
print()
print()

print('No')
dm = DialogueManager()
print(dm.run_state("deliver to 25 central avenue, Guildford, GU27XE "))
# dm.run_state()