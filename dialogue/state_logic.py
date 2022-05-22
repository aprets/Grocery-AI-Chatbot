# Logic for states
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dialogue.states import DialogueState

def confirm_handler(self: "DialogueState"):
    """ Logic to handle confirmation"""
    missing_details = []
    for e in self.entity_mask:
        if e not in self.state_entities:
            missing_details.append(e)
    
    if missing_details:
        return_string = "You are missing the following:\n"
        for v in missing_details:
            return_string += f'  - {v.title()}\n'
        return_string += '\n Please try again with the correct options.'
        self.turn = "unknown"

    else:
        return_string = "Please confirm the following:\n"
        for k, v in self.state_entities.items():
            return_string += f'  - For {k.title()} you entered: {v}\n'
        return_string += '\nYou can say "Yes" or "No" to confirm.'

    return return_string


def init_logic(self: "DialogueState"):
    if self.turn == "confirm":
        return "Confirm but this still shouldnt happen"

    return "Please be clearer with your request"


def check_availability_logic(self: "DialogueState"):
    """Logic for the check availability state"""
    if self.turn == "confirm":
        return confirm_handler(self)
    else:
        return f"{self.name}, {self.turn}"


def add_to_basket_logic(self: "DialogueState"):
    """Logic for the add to basket state"""
    if self.turn == "confirm":
        return confirm_handler(self)
    else:
        return f"{self.name}, {self.turn}"


def remove_from_basket_logic(self: "DialogueState"):
    """Logic for the remove from basket state"""
    if self.turn == "confirm":
        return confirm_handler(self)
    else:
        return f"{self.name}, {self.turn}"


def address_details_logic(self: "DialogueState"):
    """Logic for the address details state"""
    if self.turn == "confirm":
        return confirm_handler(self)
    else:
        return f"{self.name}, {self.turn}"


def timeslot_details_logic(self: "DialogueState"):
    """Logic for the timeslot request state"""
    if self.turn == "confirm":
        return confirm_handler(self)
    else:
        return f"{self.name}, {self.turn}"
    

def payment_details_logic(self: "DialogueState"):
    """Logic for the payment details state"""
    if self.turn == "confirm":
        return confirm_handler(self)
    else:
        return f"{self.name}, {self.turn}"


def confirm_order_logic(self: "DialogueState"):
    """Logic for the confirm order state"""
    if self.turn == "confirm":
        return confirm_handler(self)
    else:
        return f"{self.name}, {self.turn}"


def exit_logic(self: "DialogueState"):
    """Logic for the exit state"""

    if self.turn == "confirm":
        return confirm_handler(self)
    else:
        return f"{self.name}, {self.turn}"
