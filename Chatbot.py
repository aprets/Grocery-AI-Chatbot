import typing
from collections import deque

class DialogueState():
    """ Dialogue state, maintains entities and logic"""
    def __init__(self, name: str, default_next_state, state_logic, entities = {}):
        self.name: str = name
        self.default_next_state = default_next_state
        self.state_logic = state_logic
        self.turn = 0

        self.response_intent = None
        self.state_entities = entities


    def update_entities(self, entities):
        self.state_entities.update(entities)
        return


# Logic for states
def init_logic(self, start):
    if start:
        print("start")
    else:
        print("hello")

    return False


def check_availablity_logic(self, start):
    """Logic for the check availability state"""

    if start:
        print("start")
    else:
        print("end")
    return True


def add_to_basket_logic(self, start):
    """Logic for the add to basket state"""

    if start:
        print("start")
    else:
        print("end")
    return True


def remove_from_basket_logic(self, start):
    """Logic for the remove from basket state"""

    if start:
        print("start")
    else:
        print("end")
    return True


def address_details_logic(self, start):
    """Logic for the address details state"""

    if start:
        print("start")
    else:
        print("end")
    return True


def timeslot_request_logic(self, start):
    """Logic for the timeslot request state"""

    if start:
        print("start")
    else:
        print("end")
    return True

    
def payment_details_logic(self, start):
    """Logic for the payment details state"""

    if start:
        print("start")
    else:
        print("end")
    return True


def confirm_order_logic(self, start):
    """Logic for the confirm order state"""

    if start:
        print("start")
    else:
        print("end")
    return True


def exit_logic(self, start):
    """Logic for the exit state"""

    if start:
        print("start")
    else:
        print("end")
    return True


class DialogueManager():
    """ Dialogue Manager that handles state"""
    def __init__(self):
        self.state_defaults = {
            "init": {
                "name": "init",
                "default_next_state": "add_to_basket",
                "state_logic": init_logic, 
                "entities": ["entity_one_name", "entity_two_name"]
            },
            "check_availability": {
                "name": "check_availability",
                "default_next_state": "add_to_basket",
                "state_logic": check_availablity_logic, 
                "entities": ["entity_one_name", "entity_two_name"]
            },
            "add_to_basket": {
                "name": "add_to_basket",
                "default_next_state":"address_request",
                "state_logic": add_to_basket_logic, 
                "entities": ["entity_one_name", "entity_two_name"]
            },
            "remove_from_basket": {
                "name": "remove_from_basket",
                "default_next_state": "address_request",
                "state_logic": remove_from_basket_logic, 
                "entities": ["entity_one_name", "entity_two_name"]
            },
            "address_details": {
                "name": "address_details",
                "default_next_state": "timeslot_request",
                "state_logic": address_details_logic, 
                "entities": ["entity_one_name", "entity_two_name"]

            },
            "timeslot_request": {
                "name": "timeslot_request",
                "default_next_state": "payment_request",
                "state_logic": timeslot_request_logic, 
                "entities": ["entity_one_name", "entity_two_name"]

            },
            "payment_details": {
                "name": "payment_details",
                "default_next_state": "confirm_order",
                "state_logic": payment_details_logic, 
                "entities": ["entity_one_name", "entity_two_name"]

            },
            "confirm_order": {
                "name": "confirm_order",
                "default_next_state": "finalise",
                "state_logic": confirm_order_logic, 
                "entities": ["entity_one_name", "entity_two_name"]
            },
            "exit": {
                "name": "exit",
                "default_next_state": "init",
                "state_logic": exit_logic, 
                "entities": ["entity_one_name", "entity_two_name"]
            },
        }

        self.prior_states = deque()
        self.current_state = DialogueState(**self.state_defaults["init"])


    def start_dialogue(self):
        """ Start the dialogue"""

        self.run_state()
        return


    def run_state(self, input):
        """ Handle the running of a state"""
        if self.current_state.turn == 0:
            self.bot_turn(start = True)

        elif self.current_state.position == 1:
            self.user_turn(start = True)
            self.run_state()

        elif self.current_state.position == 2:
            requires_response = self.bot_turn(start = False)
            
        elif self.current_state.position == 3:
            if requires_response:

                self.user_turn(start = False)
                self.run_state()
 
        self.current_state.turn += 1
        return


    def bot_turn(self, start):
        """ Run a bot turn"""

        requires_response = self.current_state.state_logic(self.current_state, start=start)
        return requires_response


    def user_turn(self, start):
        """ Process a user turn"""

        turn_intent = self.get_intent()
        turn_entities = self.get_entities()

        if start:
            # Update state variables
            self.current_state.response_intent = turn_intent
            self.current_state.state_entities.update(turn_entities)
        else:
            if turn_intent == "negative":
                new_state = DialogueState(self.state_defaults(self.current_state.name), entities = turn_entities)
                self.update_state(new_state)
            else:
                if turn_intent == "affirmative":
                    next_state_name = self.current_state.default_next_state
                else:
                    next_state_name = turn_intent

                new_state = DialogueState(self.state_defaults(next_state_name), entities = turn_entities)
                self.update_state(new_state)           

        return


    def get_intent(self):
        """ Get intent from an utterance"""

        return "intent"


    def get_entities(self):
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

    dm.run_state("input")
    dm.run_state()

