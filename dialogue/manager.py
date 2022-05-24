import typing

import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

from collections import deque

from .states import STATE_DEFAULTS, DialogueState

from intent import predict_intent

from ner import ner_spacy

class DialogueManager():
    """ Dialogue Manager that handles state"""

    def __init__(self):
        self.prior_states = deque()
        self.current_state = DialogueState(
            **STATE_DEFAULTS["init"])
        self.finalised_values = {
                                    "items": [],
                                    "address": None,
                                    "timeslot": None,
                                    "payment": None
                                }

    def state_logic_wrapper(self, logic_response):
            if callable(logic_response):
                return logic_response(self)
            else:
                return logic_response

    def run_state(self, input=None):
        """ Handle the running of a state"""
        current_intent, pass_entities = self.ingest(input)
        # Handle unknown state
        if current_intent == "unknown" and not self.current_state == "lock":
            # Reset bot to start essentially
            self.current_state.turn = "unknown"
            current_intent = "init"

        if self.current_state.turn == "confirm":
            # Select next state based on intent
            if current_intent == "negative":
                next_state_name = self.current_state.name
                entities = {}
                next_turn = "confirm"

            elif current_intent == "affirmative":
                self.current_state.turn = 'confirmed'
                self.current_state.state_logic(self.current_state)(self)
                next_state_name = self.current_state.default_next_state
                entities = {}
                next_turn = "confirm"

            else: # Special case with known next state
                next_state_name = current_intent
                entities = pass_entities
                next_turn = "lock"

            # Create next state with defaults
            new_state = DialogueState(
                **STATE_DEFAULTS[next_state_name],
                entities=entities,
            )

            # Update variable values
            new_state.entities = entities
            new_state.turn = next_turn

            # Set state and broadcast message
            self.update_state(new_state)
            return self.current_state.init_message if not next_turn == "lock" else self.run_state(input)

        elif self.current_state.turn == "force_state":
            # Move to detected state
            new_state = DialogueState(
                **STATE_DEFAULTS[self.current_state.forced_next_state], 
                entities = pass_entities)
            self.update_state(new_state)

            return self.current_state.init_message

        elif self.current_state.turn == "unknown":
            # Check if intent indicates a state else reset
            if current_intent not in STATE_DEFAULTS:
                current_intent = "init"

            # Move to detected state
            new_state = DialogueState(
                **STATE_DEFAULTS[current_intent], 
                entities = pass_entities)
            self.update_state(new_state)

            return self.state_logic_wrapper(self.current_state.state_logic(self.current_state))

        
        elif self.current_state.turn == "lock":
            
            # State is locked in by previous message, 
            # ensure that it doesnt get switched and get entities
            self.current_state.state_entities = pass_entities
            self.current_state.turn = STATE_DEFAULTS[self.current_state.name]['turn']

            return self.state_logic_wrapper(self.current_state.state_logic(self.current_state))

        elif self.current_state.turn == "select" or self.current_state.turn == "selected":
                return self.current_state.state_logic(self.current_state)(self)

        else:
            # Run custom turn logic
            return self.current_state.state_logic(self.current_state)


    def ingest(self, message):
        """ Process a ingest user message"""

        for p in [",",".","-","?","!"]:
            message = message.replace(p, "")

        logging.debug(f'USER MESSAGE: {message}')
        logging.debug(f'Current State: {self.current_state.name} Turn: {self.current_state.turn} ({self.current_state.uuid})')

        turn_intent = self.get_intent(message)
        turn_entities = self.get_entities(message)
        logging.debug(f'Detected Entities: {turn_entities}')

        self.current_state.current_response = message
        self.current_state.state_entities.update(turn_entities)

        return turn_intent, turn_entities

    def get_intent(self, message):
        """ Get intent from an utterance"""

        return predict_intent(message)


    def get_entities(self, message):
        """ Get entities from an utterance"""

        ent_dict = {}
        for ent in ner_spacy(message).ents[::-1]:
            ent_dict[ent.label_] = ent.text
        return ent_dict


    def update_state(self, new_state):
        """ Save the current dialogue state to history and enter a new state."""
        logging.debug(f'Switching to State: {new_state.name} Turn: {new_state.turn} ({new_state.uuid})')

        self.prior_states.append(self.current_state)
        self.current_state = new_state