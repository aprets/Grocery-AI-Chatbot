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
        return_string = "Missing: " + ", ".join([detail.capitalize() for detail in missing_details])
    else:
        return_string = "Please confirm the following:\n\n"
        for k, v in self.state_entities.items():
            return_string += f'The {k.lower()} you chose is {v}'
            return_string += '\n'
        return_string += '\n\nYou can say "Yes" or "No" to confirm.'

    
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
        return "confirmed"

def add_to_basket_logic(self: "DialogueState"):
    """Logic for the add to basket state"""
    if self.turn == "confirm":
        return confirm_handler(self)
    else:
        return "confirmed"
def remove_from_basket_logic(self: "DialogueState"):
    """Logic for the remove from basket state"""
    return 'Removing from basket'


def address_details_logic(self: "DialogueState"):
    """Logic for the address details state"""
    if self.turn == "confirm":
        return confirm_handler(self)
    else:
        return "confirmed"



def timeslot_details_logic(self: "DialogueState"):
    """Logic for the timeslot request state"""
    if self.turn == "confirm":
        return confirm_handler(self)
    else:
        return "confirmed"    
    
def payment_details_logic(self: "DialogueState"):
    """Logic for the payment details state"""
    if self.turn == "confirm":
        return confirm_handler(self)
    else:
        return "confirmed"

def confirm_order_logic(self: "DialogueState"):
    """Logic for the confirm order state"""
    if self.turn == "confirm":
        return confirm_handler(self)
    else:
        return "confirmed"

def exit_logic(self: "DialogueState"):
    """Logic for the exit state"""

    if self.turn == "confirm":
        return confirm_handler(self)
    else:
        return "confirmed"