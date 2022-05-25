STATE_DEFAULTS = {
    "init": {
        "name": "init",
        "default_next_state": "add_to_basket",
        "entity_mask": [],
        "init_message": "Welcome to Bainsurreys' - oops!",
        "turn": "unknown"

    },
    "check_availability": {
        "name": "check_availability",
        "default_next_state": "add_to_basket",
        "entity_mask": ["PRODUCT"],
        "init_message": "What product would you like to check availability for?",
        "turn": "confirm"
    },
    "add_to_basket": {
        "name": "add_to_basket",
        "default_next_state": "address_details",
        "entity_mask": ["PRODUCT"],
        "init_message": "What product would you like to add to basket?",
        "turn": "select"
    },
    "remove_from_basket": {
        "name": "remove_from_basket",
        "default_next_state": "address_details",
        "entity_mask": ["PRODUCT"],
        "init_message": "What product would you like to remove from basket?",
        "turn": "confirm"
    },
    "address_details": {
        "name": "address_details",
        "default_next_state": "timeslot_details",
        "entity_mask": ["STREET", "CITY", "POSTCODE"],
        "init_message": "What address would you like the order to be delivered to?",
        "turn": "confirm"
    },
    "timeslot_details": {
        "name": "timeslot_details",
        "default_next_state": "payment_details",
        "entity_mask": ["TIME"],
        "init_message": "What time tomorrow would you like the order delivered?",
        "turn": "confirm"
    },
    "payment_details": {
        "name": "payment_details",
        "default_next_state": "confirm_order",
        "entity_mask": ["NAME", "CARD_NUMBER", "CARD_CVC", "CARD_EXPIRY"],
        "init_message": "Please enter your Credit Card Number, CVC, Expiry Date and the Cardholder Name.",
        "turn": "confirm"
    },
    "confirm_order": {
        "name": "confirm_order",
        "default_next_state": "exit",
        "entity_mask": [],
        "init_message": "????????????",
        "turn": "confirm"
    },
    "exit": {
        "name": "exit",
        "default_next_state": "init",
        "entity_mask": [],
        "init_message": "Restarting conversation...",
        "turn": "confirm"
    },
}
