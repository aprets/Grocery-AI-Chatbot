import typing
from collections import deque

from states import STATE_DEFAULTS, DialogueState


class DialogueManager():
    """ Dialogue Manager that handles state"""

    def __init__(self):
        self.state_defaults = STATE_DEFAULTS

        self.prior_states = deque()
        self.current_state = DialogueState(
            **self.state_defaults["add_to_basket"])

    def start_dialogue(self):
        """ Start the dialogue"""

        self.run_state()
        return

    def run_state(self, input=None):
        """ Handle the running of a state"""
        self.current_state.position = (self.current_state.position + 1) % 5

        print(
            f'Intent {self.current_state.name}, Position {self.current_state.position}')

        if self.current_state.position == 1:
            return self.bot_turn(start=True)

        elif self.current_state.position == 2:
            self.user_turn(start=True, message=input)
            return self.run_state()

        elif self.current_state.position == 3:
            return self.bot_turn(start=False)

        elif self.current_state.position == 4:
            if not self.current_state.skip_response:
                self.user_turn(start=False, message=input)
                return self.run_state()

    def bot_turn(self, start):
        """ Run a bot turn"""

        return self.current_state.state_logic(self.current_state, start=start)

    def user_turn(self, start, message):
        """ Process a user turn"""

        turn_intent = self.get_intent(message)
        turn_entities = self.get_entities(message)

        if start:
            # Update state variables
            self.current_state.response_intent = turn_intent
            self.current_state.state_entities.update(turn_entities)
        else:
            if turn_intent == "negative":
                new_state = DialogueState(
                    self.state_defaults[self.current_state.name],
                    entities=turn_entities,
                )
                self.update_state(new_state)
            else:
                if turn_intent == "affirmative":
                    next_state_name = self.current_state.default_next_state
                else:
                    next_state_name = turn_intent

                new_state = DialogueState(
                    self.state_defaults[next_state_name],
                    entities=turn_entities,
                )
                self.update_state(new_state)

        return

    def get_intent(self, message):
        """ Get intent from an utterance"""

        return "intent"

    def get_entities(self, message):
        """ Get entities from an utterance"""

        return {"entity_one": "one"}

    def update_state(self, new_state):
        """ Save the current dialogue state to history and enter a new state."""

        self.prior_states.append(self.current_state)
        self.current_state = new_state
        return


if __name__ == "__main__":
    dm = DialogueManager()

    dm.start_dialogue()

    print(dm.run_state("input"))
    print(dm.run_state("input"))
    print(dm.run_state("input"))
    print(dm.run_state("input"))
    print(dm.run_state("input"))
    # dm.run_state()
