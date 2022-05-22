{

"init": {"name":"init", "default_next_state":"add_to_basket"}, # ignore

"check_availability":{"name":"check_availability", "default_next_state":"add_to_basket"}, # chcek if you have item

"add_to_basket":{"name":"add_to_basket", "default_next_state":"address_request"}, 

"remove_from_basket":{"name":"remove_from_basket", "default_next_state":"address_request"},

"address_request":{"name":"address_request", "default_next_state":"timeslot_request"}, # change address, my address is

"timeslot_request":{"name":"timeslot_request", "default_next_state":"payment_request"}, # change delivery time, deliver at

"payment_details":{"name":"payment_request", "default_next_state":"confirm_order"}, # change card, change payment info, 

"confirm_order":{"name":"confirm_order", "default_next_state":"finalise"}, # checkout 

"exit":{"name":"finalise", "default_next_state":"init"}, # bye get me out

}