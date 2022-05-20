# Logic for states
def init_logic(self, start):
    if start:
        return 'start'
    else:
        return 'end'


def check_availability_logic(self, start):
    """Logic for the check availability state"""

    if start:
        print("start")
    else:
        print("end")


def add_to_basket_logic(self, start):
    """Logic for the add to basket state"""

    if start:
        print("start")
    else:
        print("end")


def remove_from_basket_logic(self, start):
    """Logic for the remove from basket state"""

    if start:
        print("start")
    else:
        print("end")


def address_details_logic(self, start):
    """Logic for the address details state"""

    if start:
        print("start")
    else:
        print("end")


def timeslot_details_logic(self, start):
    """Logic for the timeslot request state"""

    if start:
        print("start")
    else:
        print("end")

    
def payment_details_logic(self, start):
    """Logic for the payment details state"""

    if start:
        print("start")
    else:
        print("end")


def confirm_order_logic(self, start):
    """Logic for the confirm order state"""

    if start:
        print("start")
    else:
        print("end")


def exit_logic(self, start):
    """Logic for the exit state"""

    if start:
        print("start")
    else:
        print("end")
