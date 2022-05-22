from .state_logic import *

import uuid

class DialogueState():
    """ Dialogue state, maintains entities and logic"""

    def __init__(self, name: str, init_message, default_next_state, state_logic, lock_state=False, entities={}, entity_mask=[], turn="confirm"):
        self.name: str = name
        self.uuid = uuid.uuid4()
        self.default_next_state = default_next_state
        self.state_logic = state_logic
        self.init_message = init_message
        self.turn = turn
        self.lock_state = lock_state

        self.current_response = None
        self.state_entities = entities
        self.entity_mask = entity_mask


    def update_entities(self, entities):
        self.state_entities.update(entities)
        return


STATE_DEFAULTS = {
    "init": {
        "name": "init",
        "default_next_state": "add_to_basket",
        "state_logic": init_logic,
        "entity_mask": [],
        "init_message": "Welcome to Bainsurreys' - oops!",
        "turn": "unknown"

    },
    "check_availability": {
        "name": "check_availability",
        "default_next_state": "add_to_basket",
        "state_logic": check_availability_logic,
        "entity_mask": ["PRODUCT"],
        "init_message": "Checking availablility",

    },
    "add_to_basket": {
        "name": "add_to_basket",
        "default_next_state": "address_details",
        "state_logic": add_to_basket_logic,
        "entity_mask": ["PRODUCT"],
        "init_message": "add to basket init msg",
    },
    "remove_from_basket": {
        "name": "remove_from_basket",
        "default_next_state": "address_details",
        "state_logic": remove_from_basket_logic,
        "entity_mask": ["PRODUCT"],
        "init_message": "remove from basket msg"

    },
    "address_details": {
        "name": "address_details",
        "default_next_state": "timeslot_details",
        "state_logic": address_details_logic,
        "entity_mask": ["STREET", "CITY", "POSTCODE"],
        "init_message": "address init message"

    },
    "timeslot_details": {
        "name": "timeslot_details",
        "default_next_state": "payment_details",
        "state_logic": timeslot_details_logic,
        "entity_mask": ["TIME"],
        "init_message": "Timeslot init message"

    },
    "payment_details": {
        "name": "payment_details",
        "default_next_state": "confirm_order",
        "state_logic": payment_details_logic,
        "entity_mask": [],
        "init_message": "payment init message"

    },
    "confirm_order": {
        "name": "confirm_order",
        "default_next_state": "finalise",
        "state_logic": confirm_order_logic,
        "entity_mask": [],
        "init_message": "payment init message"
    },
    "exit": {
        "name": "exit",
        "default_next_state": "init",
        "state_logic": exit_logic,
        "entity_mask": [],
        "init_message": "payment init message"
    },
}
