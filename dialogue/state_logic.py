# Logic for states
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dialogue.states import DialogueState

def init_logic(self: "DialogueState"):
    if self.turn == "confirm":
        return "Confirm but this still shouldnt happen"

    return "Please be clearer with your request"


def check_availability_logic(self: "DialogueState"):
    """Logic for the check availability state"""
    return 'Checking availability'


def add_to_basket_logic(self: "DialogueState"):
    """Logic for the add to basket state"""
    return 'Adding to basket'

def remove_from_basket_logic(self: "DialogueState"):
    """Logic for the remove from basket state"""
    return 'Removing from basket'


def address_details_logic(self: "DialogueState"):
    """Logic for the address details state"""
    out_string = ""

    if self.turn == "confirm":
        incorrect = False

        for e in self.entity_mask:
            if e in self.state_entities:     
                out_string += f'    Found Entity "{e}": {self.state_entities[e]}\n'
            else:
                out_string += f'    Did not find entity {e}\n'
                incorrect = True
        
        if incorrect:
            None#self.
    else:
        out_string += f'Is your address {self.state_entities["STREET"]}?\n'

    return out_string.strip("\n")


def timeslot_details_logic(self: "DialogueState"):
    """Logic for the timeslot request state"""
    if self.turn == "confirm":
        return f'Setting timeslot {self.state_entities["TIME"]}'

    return f'Would you like this timeslot:'# {self.state_entities["TIME"]}?'
    
    
def payment_details_logic(self: "DialogueState"):
    """Logic for the payment details state"""
    if self.turn == "confirm":
        self.state_entities["CARD_NUMBER"]

    return 'Setting payment details'


def confirm_order_logic(self: "DialogueState"):
    """Logic for the confirm order state"""

    return 'Order confirmed'


def exit_logic(self: "DialogueState"):
    """Logic for the exit state"""

    return 'Bye!'
