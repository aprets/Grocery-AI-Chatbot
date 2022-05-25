# Logic for states
from asyncio.log import logger
from typing import TYPE_CHECKING, overload

from numpy import int32

from product.product_helper import menu_item

if TYPE_CHECKING:
    from dialogue.states import DialogueState
    from dialogue.manager import DialogueManager

from product import menu

CLEARER_STRING = "Please be clearer with your request."

def confirm_handler(self: "DialogueState", confirm_message="Please confirm the following") -> str:
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
        return_string = f"{confirm_message}:\n"
        for k, v in self.state_entities.items():
            return_string += f'  - For {k.title()} you entered: {v}\n'

    return return_string


def init_logic(self: "DialogueState"):
    if self.turn == "confirm":
        return "Confirm but this still shouldnt happen"

    return CLEARER_STRING

def check_availability_logic(self: "DialogueState"):
    """Logic for the check availability state"""
    if "PRODUCT" in self.state_entities:
        top = menu.get_top_n_items(self.state_entities["PRODUCT"])
        return f"For {self.state_entities['PRODUCT']} we have:\n    " + '\n    - '.join([f"{v.name}" for v in top])
    else:
        return CLEARER_STRING


def add_to_basket_logic(self: "DialogueState"):
    """Logic for the add to basket state"""
    def confirmed_callback(manager: "DialogueManager") -> str:
        manager.finalised_values["items"].append(self.temp)
        self.temp = None
        logger.debug(f'Finalised Items: [{[i.name for i in manager.finalised_values["items"]]}]')
        return f"Added {self.temp} to basket."

    def local_confirm_handler(manager: "DialogueManager") -> str:
        try:
            selection: menu_item = self.temp[int(self.current_response)]
            self.temp = selection
            self.turn = "confirm"
            return f"We think you have selected: {selection.name}, please confirm."
        except:
            self.turn = "unknown"
            return CLEARER_STRING

    def select_item_callback(manager: "DialogueManager") -> str:
        if "PRODUCT" in self.state_entities:
            top = menu.get_top_n_items(self.state_entities["PRODUCT"])
            suggest_str = "Please select an item:\n    " + '\n    '.join([f"{k}. {v.name}" for k,v in enumerate(top)])

            self.forced_next_state = self.name
            self.turn = "selected"
            self.temp = top

            return suggest_str
        else:
            self.forced_next_state = self.name
            self.turn = "force_state"
            return CLEARER_STRING

    if self.turn == "select" or self.turn == "lock":
        return select_item_callback
    elif self.turn == "selected":
        return local_confirm_handler
    elif self.turn == "confirmed":
        return confirmed_callback


def remove_from_basket_logic(self: "DialogueState"):
    """Logic for the remove from basket state"""

    def confirmed_callback(manager: "DialogueManager"):
        manager.finalised_values['items'].remove(self.temp)
        return f"Removed {self.temp} from basket."


    def local_confirm_handler(manager: "DialogueManager") -> str:
        if manager.finalised_values["items"] and "PRODUCT" in self.state_entities:
            item_to_remove = menu.select_most_likely(manager.finalised_values["items"],self.state_entities["PRODUCT"])
            self.temp = item_to_remove
            self.turn = "confirm"
            return f"Are you sure you want to remove {item_to_remove.name}?"
        else:
            self.turn = "unknown"
            return CLEARER_STRING


    if self.turn == "confirm":
        return local_confirm_handler
    elif self.turn == "confirmed":
        return confirmed_callback
    else:
        return f"{self.name}, {self.turn}"


def address_details_logic(self: "DialogueState"):
    """Logic for the address details state"""

    def confirmed_callback(manager: "DialogueManager") -> str:
        finalised_address = manager.finalised_values['address']
        finalised_address = {
            'STREET': self.state_entities['STREET'],
            'CITY': self.state_entities['CITY'],
            'POSTCODE': self.state_entities['POSTCODE'],
        }
        logger.debug(f'Finalised Values: [{", ".join([f"{v}: {finalised_address[v]}" for v in self.entity_mask])}]')
        return f"Address set as {''.join([finalised_address[v] for v in self.entity_mask])}"
        
    if self.turn == "confirm":
        return confirm_handler(self)
    elif self.turn == "confirmed":
        return confirmed_callback
    else:
        return f"{self.name}, {self.turn}"


def timeslot_details_logic(self: "DialogueState"):
    """Logic for the timeslot request state"""

    def confirmed_callback(manager: "DialogueManager"):
        manager.finalised_values['timeslot'] = self.state_entities['TIME']

        logger.debug(f'Finalised Values: [timeslot: {manager.finalised_values["timeslot"]}]')

    if self.turn == "confirm":
        return confirm_handler(self)
    elif self.turn == "confirmed":
        return confirmed_callback
    else:
        return f"{self.name}, {self.turn}"


def payment_details_logic(self: "DialogueState"):
    """Logic for the payment details state"""

    def confirmed_callback(manager: "DialogueManager"):
        finalised_payment =  manager.finalised_values['payment']
        finalised_payment = {
            'NAME': self.state_entities['NAME'],
            # TODO: Assumes they exist
            'CARD_NUMBER': self.state_entities['CARD_NUMBER'],
            'CARD_CVC': self.state_entities['CARD_CVC'],
            'CARD_EXPIRY': self.state_entities['CARD_EXPIRY'],
        }

        logger.debug(f'Finalised Values: [{", ".join([f"{v}: {finalised_payment[v]}" for v in self.entity_mask])}]')

    if self.turn == "confirm":
        return confirm_handler(self)
    elif self.turn == "confirmed":
        return confirmed_callback
    else:
        return f"{self.name}, {self.turn}"


def confirm_order_logic(self: "DialogueState"):
    """Logic for the confirm order state"""
    if self.turn == "confirm":
        return "custom confirm"
    else:
        return f"{self.name}, {self.turn}"


def exit_logic(self: "DialogueState"):
    """Logic for the exit state"""

    if self.turn == "confirm":
        return confirm_handler(self)
    else:
        return f"{self.name}, {self.turn}"
