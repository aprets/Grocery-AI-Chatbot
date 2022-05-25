from .state_logic import *

import uuid

class DialogueState():
    """ Dialogue state, maintains entities and logic"""

    def __init__(self, name: str, init_message, default_next_state, state_logic = None, entities={},current_response=None, entity_mask=[], turn="confirm"):
        self.name: str = name
        self.uuid = uuid.uuid4()
        self.default_next_state = default_next_state
        self.forced_next_state = None
        self.state_logic = state_logic
        self.init_message = init_message
        self.turn = turn

        self.current_response = None
        self.state_entities = entities
        self.entity_mask = entity_mask


    def update_entities(self, entities):
        self.state_entities.update(entities)
        return

STATE_FUNCTIONS = {
    "init": init_logic,
    "check_availability":check_availability_logic,
    "add_to_basket": add_to_basket_logic,
    "remove_from_basket": remove_from_basket_logic,
    "address_details": address_details_logic,
    "timeslot_details":  timeslot_details_logic,
    "payment_details": payment_details_logic,
    "confirm_order": confirm_order_logic,
    "exit": exit_logic
}
