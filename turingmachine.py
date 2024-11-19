import yaml

class TuringMachine:
    def __init__(self, states, initial_state, final_states, tape_alphabet, transitions):
        self.states = states
        self.initial_state = initial_state
        self.final_states = final_states
        self.tape_alphabet = tape_alphabet
        self.transitions = transitions
        self.tape = []
        self.head_position = 0
        self.current_state = initial_state

    def reiniciar(self, input_string):

        self.tape = list(input_string) + ['_']  
        self.head_position = 0
        self.current_state = self.initial_state

    def step(self):

        current_symbol = self.tape[self.head_position]
        key = (self.current_state, current_symbol)

        if key not in self.transitions:
            return False  

        siguiente_estado, write_symbol, mover_direccion = self.transitions[key]
        self.tape[self.head_position] = write_symbol
        self.current_state = siguiente_estado

        if mover_direccion == 'L':
            self.head_position = max(0, self.head_position - 1)
        elif mover_direccion == 'R':
            self.head_position += 1

        if self.head_position >= len(self.tape):
            self.tape.append('_')  

        return self.get_descripcion()

    def get_descripcion(self):
        tape_str = ''.join(self.tape)
        head_indicator = ' ' * self.head_position + '^'
        return f"Tape: {tape_str}\nHead: {head_indicator}\nState: {self.current_state}"

    def run(self, input_string):

        self.reiniciar(input_string)
        descriptions = [self.get_descripcion()]

        while self.current_state not in self.final_states:
            step_result = self.step()
            if not step_result:
                return "Rechazada", descriptions  
            descriptions.append(step_result)

        return "Aceptada", descriptions

