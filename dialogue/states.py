from .state_logic import *

class DialogueState():
    """ Dialogue state, maintains entities and logic"""

    def __init__(self, name: str, default_next_state, state_logic, entities={}, entity_mask=[], skip_response=False):
        self.name: str = name
        self.skip_response = skip_response
        self.default_next_state = default_next_state
        self.state_logic = state_logic
        self.position = 0

        self.response_intent = None
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
                "entity_mask": ["entity_one_name", "entity_two_name"],
                "skip_response": True,
    },
    "check_availability": {
        "name": "check_availability",
                "default_next_state": "add_to_basket",
                "state_logic": check_availability_logic,
                "entity_mask": ["entity_one_name", "entity_two_name"]
    },
    "add_to_basket": {
        "name": "add_to_basket",
                "default_next_state": "address_request",
                "state_logic": add_to_basket_logic,
                "entity_mask": ["entity_one_name", "entity_two_name"]
    },
    "remove_from_basket": {
        "name": "remove_from_basket",
                "default_next_state": "address_request",
                "state_logic": remove_from_basket_logic,
                "entity_mask": ["entity_one_name", "entity_two_name"]
    },
    "address_details": {
        "name": "address_details",
                "default_next_state": "timeslot_details",
                "state_logic": address_details_logic,
                "entity_mask": ["entity_one_name", "entity_two_name"]

    },
    "timeslot_details": {
        "name": "timeslot_details",
                "default_next_state": "payment_request",
                "state_logic": timeslot_details_logic,
                "entity_mask": ["entity_one_name", "entity_two_name"]

    },
    "payment_details": {
        "name": "payment_details",
                "default_next_state": "confirm_order",
                "state_logic": payment_details_logic,
                "entity_mask": ["entity_one_name", "entity_two_name"]

    },
    "confirm_order": {
        "name": "confirm_order",
                "default_next_state": "finalise",
                "state_logic": confirm_order_logic,
                "entity_mask": ["entity_one_name", "entity_two_name"]
    },
    "exit": {
        "name": "exit",
                "default_next_state": "init",
                "state_logic": exit_logic,
                "entity_mask": ["entity_one_name", "entity_two_name"]
    },
}
