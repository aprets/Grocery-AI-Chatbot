# Logic for states
from asyncio.log import logger
from typing import TYPE_CHECKING, overload

from numpy import int32
from dialogue.state_defaults import STATE_DEFAULTS

from product.product_helper import menu_item

if TYPE_CHECKING:
    from dialogue.states import DialogueState
    from dialogue.manager import DialogueManager

from product import menu

CLEARER_STRING = "Please be clearer with your request."
PRODUCT_MISSING = "We didn't identify any products matching that request, please try again."
END_ERROR = "This shouldn't have happened, please contact support"

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
    else:
        return CLEARER_STRING


def check_availability_logic(self: "DialogueState"):
    """Logic for the check availability state"""
    if "PRODUCT" in self.state_entities:
        top = menu.get_top_n_items(self.state_entities["PRODUCT"])
        return f"For {self.state_entities['PRODUCT']} we have:\n    " + '\n    - '.join([f"{v.name}" for v in top])
    else:
        return PRODUCT_MISSING


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

            if top:
                return suggest_str
            else:
                return PRODUCT_MISSING
       
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
    else:
        logger.error(f"Fatal error: \n    State: {self.name}, Turn: {self.turn}, Message: {self.current_response}")
        return END_ERROR


def remove_from_basket_logic(self: "DialogueState"):
    """Logic for the remove from basket state"""

    def confirmed_callback(manager: "DialogueManager"):
        manager.finalised_values['items'].remove(self.temp)
        logger.debug(f'Finalised Items: {[i.name for i in manager.finalised_values["items"]]}')
        return f"Removed {self.temp} from basket."


    def local_confirm_handler(manager: "DialogueManager") -> str:
        if manager.finalised_values["items"]:
            if "PRODUCT" in self.state_entities:
                item_to_remove = menu.select_most_likely(manager.finalised_values["items"],self.state_entities["PRODUCT"])
                self.temp = item_to_remove
                self.turn = "confirm"
                return f"Are you sure you want to remove {item_to_remove.name}?"
            else:
                self.turn = "unknown"
                return PRODUCT_MISSING          
        else:
            self.turn = "unknown"
            return CLEARER_STRING


    if self.turn == "confirm":
        return local_confirm_handler
    elif self.turn == "confirmed":
        return confirmed_callback
    else:
        logger.error(f"Fatal error: \n    State: {self.name}, Turn: {self.turn}, Message: {self.current_response}")
        return END_ERROR


def address_details_logic(self: "DialogueState"):
    """Logic for the address details state"""

    def confirmed_callback(manager: "DialogueManager") -> str:
        finalised_address = manager.finalised_values['address']
        finalised_address = {
            'STREET': self.state_entities['STREET'],
            'CITY': self.state_entities['CITY'],
            'POSTCODE': self.state_entities['POSTCODE'],
        }
        logger.debug(f'Finalised Values: {", ".join([f"{v}: {finalised_address[v]}" for v in self.entity_mask])}')
        return f"Address set as {''.join([finalised_address[v] for v in self.entity_mask])}"
        
    if self.turn == "confirm":
        return confirm_handler(self)
    elif self.turn == "confirmed":
        return confirmed_callback
    else:
        logger.error(f"Fatal error: \n    State: {self.name}, Turn: {self.turn}, Message: {self.current_response}")
        return END_ERROR


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
        logger.error(f"Fatal error: \n    State: {self.name}, Turn: {self.turn}, Message: {self.current_response}")
        return END_ERROR


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
        logger.error(f"Fatal error: \n    State: {self.name}, Turn: {self.turn}, Message: {self.current_response}")
        return END_ERROR


def confirm_order_logic(self: "DialogueState"):
    """Logic for the confirm order state"""

    def order_confirm_callback(manager: "DialogueManager"):
        if not manager.finalised_values["items"] == []:

            if not manager.finalised_values["address"]== None and \
            not manager.finalised_values["address"]["STREET"] and\
            not manager.finalised_values["address"]["CITY"] and\
            not manager.finalised_values["address"]["POSTCODE"]:

                if manager.finalised_values["timeslot"] == None:

                    if not manager.finalised_values["payment"]== None and \
                    not manager.finalised_values["payment"]["CARD_NUMBER"] and\
                    not manager.finalised_values["payment"]["CARD_CVC"] and\
                    not manager.finalised_values["payment"]["CARD_EXPIRY"]:
                        self.forced_next_state = "exit"
                        self.turn = "force_state"
                        return "Order processed succesfully!"
                    else:
                        self.forced_next_state = "payment_details"
                        self.turn = "force_state_no_init"
                        return STATE_DEFAULTS["payment_details"]["init_message"]

                else:
                    self.forced_next_state = "timeslot_details"
                    self.turn = "force_state_no_init"
                    return STATE_DEFAULTS["payment_details"]["timeslot_details"]

            else:
                self.forced_next_state = "address_details"
                self.turn = "force_state_no_init"
                return STATE_DEFAULTS["payment_details"]["address_details"]

        else:
            self.forced_next_state = "add_to_basket"
            self.turn = "force_state_no_init"
            return STATE_DEFAULTS["payment_details"]["add_to_basket"]

    if self.turn == "confirm":
        return order_confirm_callback(self)
    else:
        logger.error(f"Fatal error: \n    State: {self.name}, Turn: {self.turn}, Message: {self.current_response}")
        return END_ERROR


def exit_logic(self: "DialogueState"):
    """Logic for the exit state"""
    header = "\noooooooooo.             o8o               .oooooo..o                                                              o8o "+ \
    "\n`888'   `Y8b            `\"'              d8P'    `Y8                                                              `YP "+ \
    "\n 888     888  .oooo.   oooo  ooo. .oo.   Y88bo.      oooo  oooo  oooo d8b oooo d8b  .ooooo.  oooo    ooo  .oooo.o  '  "+ \
    "\n 888oooo888' `P  )88b  `888  `888P\"Y88b   `\"Y8888o.  `888  `888  `888\"\"8P `888\"\"8P d88' `88b  `88.  .8'  d88(  \"8     "+ \
    "\n 888    `88b  .oP\"888   888   888   888       `\"Y88b  888   888   888      888     888ooo888   `88..8'   `\"Y88b.      "+ \
    "\n 888    .88P d8(  888   888   888   888  oo     .d8P  888   888   888      888     888    .o    `888'    o.  )88b     "+ \
    "\no888bood8P'  `Y888\"\"8o o888o o888o o888o 8\"\"88888P'   `V88V\"V8P' d888b    d888b    `Y8bod8P'     .8'     8\"\"888P'     "+ \
    "\n                                                                                            .o..P'                   "+ \
    "\n                                                                                            `Y8P'                    "+ \
    "\n                                                                                                                  "

    return "\n" + header + "\nWelcome! How can we help you?"