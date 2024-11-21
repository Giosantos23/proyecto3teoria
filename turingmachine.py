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
                return "Rechazada", descriptions  # No hay transición válida
            descriptions.append(step_result)

        # Generar resultado final de la cinta
        tape_final = ''.join(self.tape).rstrip('_')  # Elimina símbolos extra de la cinta
        descriptions.append(f"Resultado final en la cinta: {tape_final}")
        
        return "Aceptada", descriptions


def cargar_mt(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)

    states = config['q_states']['q_list']
    initial_state = config['q_states']['initial']
    final_states = [config['q_states']['final']]
    tape_alphabet = config['tape_alphabet']
    transitions = {}

    for transition in config['delta']:
        params = transition['params']
        output = transition['output']
        key = (params['initial_state'], params['tape_input'])
        value = (
            output['final_state'],
            output['tape_output'],
            output['tape_displacement']
        )
        transitions[key] = value

    cadenas_simulacion = config.get('simulation_strings', [])

    return {
        "states": states,
        "initial_state": initial_state,
        "final_states": final_states,
        "tape_alphabet": tape_alphabet,
        "transitions": transitions,
        "simulation_strings": cadenas_simulacion
    }
def procesar_archivo(yaml_file):
    tm_config = cargar_mt(yaml_file)

    tm = TuringMachine(
        states=tm_config["states"],
        initial_state=tm_config["initial_state"],
        final_states=tm_config["final_states"],
        tape_alphabet=tm_config["tape_alphabet"],
        transitions=tm_config["transitions"]
    )

    print(f"\nProcesando archivo: {yaml_file}\n{'='*40}\n")

    for input_string in tm_config["simulation_strings"]:
        print(f"Cadena simulada: {input_string}")
        result, descriptions = tm.run(input_string)
        for step, desc in enumerate(descriptions):
            print(f"Step {step}:\n{desc}\n")
        print(f"Resultado: {result}\n{'-'*40}\n")


if __name__ == "__main__":
    # Archivos a procesar
    archivos_yaml = ["estructura-mt.yaml", "estructura-mt-alteradora.yaml"]

    for archivo in archivos_yaml:
        procesar_archivo(archivo)
