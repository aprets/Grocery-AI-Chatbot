# Logic for states
def init_logic(self):
    if self.confirm:
        return "Confirm but this still shouldnt happen"

    return "This shouldn't happen"

def check_availability_logic(self):
    """Logic for the check availability state"""
    return 'Checking availability'


def add_to_basket_logic(self):
    """Logic for the add to basket state"""
    return 'Adding to basket'

def remove_from_basket_logic(self):
    """Logic for the remove from basket state"""
    return 'Removing from basket'


def address_details_logic(self):
    """Logic for the address details state"""
    if self.confirm:
        for e in self.entity_mask:
            self.state_entities[e]
        return f'Setting address {self.state_entities["STREET"]}'

    return f'Is your address {self.state_entities["STREET"]}?'


def timeslot_details_logic(self):
    """Logic for the timeslot request state"""
    if self.confirm:
        return f'Setting timeslot {self.state_entities["TIME"]}'

    return f'Would you like this timeslot: {self.state_entities["TIME"]}?'
    
    
def payment_details_logic(self):
    """Logic for the payment details state"""

    return 'Setting payment details'


def confirm_order_logic(self):
    """Logic for the confirm order state"""

    return 'Order confirmed'


def exit_logic(self, start):
    """Logic for the exit state"""

    return 'Bye!'
