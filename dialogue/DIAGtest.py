from dialogue.manager import DialogueManager

print('Dialog test')
dm = DialogueManager()
print(dm.run_state("i am 67 avenue road"))
print(dm.run_state("yes"))

print(dm.run_state("deliver it at 3pm"))
print(dm.run_state("yes"))

print()
print()