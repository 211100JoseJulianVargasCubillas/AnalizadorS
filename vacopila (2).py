import re
import sys
import tkinter as tk
from tkinter import messagebox

class StdoutRedirector(object):
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, string):
        self.text_widget.config(state='normal')
        self.text_widget.insert('end', string)
        self.text_widget.see('end')
        self.text_widget.config(state='disabled')

    def flush(self):
        pass

class PDA:
    
    def __init__(self, grammar, terminals):
        self.grammar = grammar
        self.terminals = terminals
        self.stack = []
        self.history = []

    # automata de pila
    def parse(self, input_string):
        self.stack.append("S")  # Símbolo de inicio
        print("Pila:", self.stack)
        index = 0
        while self.stack and index <= len(input_string):
            index = self.skip_whitespace(
                input_string, index
            )
            if index >= len(input_string):
                break

            top = self.peek()
            remaining_input = input_string[index:]

            if top in self.grammar:
                self.process_non_terminal(top, remaining_input)
            elif self.match_terminal(top, remaining_input):
                match_length = len(
                    re.match(self.terminals[top], remaining_input).group()
                )
                index += match_length
                self.pop()
            else:
                raise Exception(f"Error de sintaxis cerca de la posición {index}")
            print("Pila:", self.stack)
        return len(self.stack) == 0

    def process_non_terminal(self, non_terminal, input_string):
        self.pop()

        if non_terminal == "S":
            self.choose_production_for_S(input_string)
        elif non_terminal == "VL":
            self.choose_production_for_VL(input_string)
        elif non_terminal == "VL2":
            self.choose_production_for_VL2(input_string)
        elif non_terminal == "ON":
            self.choose_production_for_ON(input_string)
        elif non_terminal == "CL2":
            self.push_production(self.grammar["CL2"][0])
        elif non_terminal == "CL3":
            self.push_production(self.grammar["CL3"][0])
        elif non_terminal == "CL5":
            self.push_production(self.grammar["CL5"][0])
        elif non_terminal == "CL6":
            self.push_production(self.grammar["CL6"][0])
        elif non_terminal == "CL10":
            self.push_production(self.grammar["CL10"][0])
        elif non_terminal == "IF2":
            self.push_production(self.grammar["IF2"][0])
        elif non_terminal == "V":
            self.push_production(self.grammar["V"][0])
        elif non_terminal == "P":
            self.push_production(self.grammar["P"][0])
        elif non_terminal == "F3":
            self.push_production(self.grammar["F3"][0])
        elif non_terminal == "TT":
            if non_terminal == "F":
                self.push_production(self.grammar["TT"][0])
            else:
                self.push_production(self.grammar["TT"][1])
        else:
            self.choose_production(non_terminal, input_string)

    def choose_production_for_ON(self, input_string):
        if re.match(self.terminals["ID"], input_string):
            self.push_production(self.grammar["ON"][0])
        elif re.match(self.terminals["N"], input_string):
            self.push_production(self.grammar["ON"][1])

    def choose_production_for_VL2(self, input_string):
        if re.match(self.terminals["CM"], input_string):
            self.push_production(self.grammar["VL2"][0])
        elif re.match(self.terminals["N"], input_string):
            self.push_production(self.grammar["VL2"][1])

    def choose_production_for_VL(self, input_string):
        if re.match(self.terminals["AS"], input_string):
            self.push_production(self.grammar["VL"][0])
        else:
            self.push_production(self.grammar["VL"][1])

    def choose_production_for_S(self, input_string):
        if re.match(self.terminals["AG"], input_string):
            self.push_production(self.grammar["S"][0])
        elif re.match(self.terminals["VQ"], input_string):
            self.push_production(self.grammar["S"][1])
        elif re.match(self.terminals["PQ"], input_string):
            self.push_production(self.grammar["S"][2])
        elif re.match(self.terminals["VS"], input_string):
            self.push_production(self.grammar["S"][3])
        else:
            raise Exception(
                f"No se pudo encontrar una producción adecuada para 'S' con entrada {input_string}"
            )

    def choose_production(self, non_terminal, input_string):
        for production in self.grammar[non_terminal]:
            if self.is_valid_production(production, input_string):
                self.push_production(production)
                return
        raise Exception(
            f"No se pudo encontrar una producción adecuada para {non_terminal} con entrada {input_string}"
        )

    def is_valid_production(self, production, input_string):
        symbols = production.split()
        if not symbols:
            return False
        first_symbol = symbols[0]
        if first_symbol in self.terminals:
            return re.match(self.terminals[first_symbol], input_string) is not None
        else:
            return False

    def push_production(self, production):
        for symbol in reversed(production.split()):
            self.push(symbol)

    def skip_whitespace(self, input_string, index):
        while index < len(input_string) and input_string[index].isspace():
            index += 1
        return index

    def match_terminal(self, terminal, input_string):
        pattern = self.terminals[terminal]
        return re.match(pattern, input_string)

    def push(self, symbol):
        if symbol != "ε":
            self.stack.append(symbol)

    def pop(self):
        return self.stack.pop() if self.stack else None

    def peek(self):
        return self.stack[-1] if self.stack else None


terminals = {
    "ID": r"[a-z_][a-zA-Z_]*",
    "N": r"[0-9]+",
    "VS": r"vasir",
    "NS": r"novasir",
    "SO": r"siono",
    "AG": r"agusticidad",
    "TP": r"(pan|ububue)",
    "C": r"contenido",
    "PQ": r"Paraqoque",
    "AS": r"=",
    "CM": r'"',
    "PA": r"\(",
    "PC": r"\)",
    "LA": r"\{",
    "LC": r"\}",
    "OP": r"(<|>|==|>=|<=|!=)",
    "PT": r"\;",
    "IN": r"\++",
    "VQ": r"Vuelaoque"
}

grammar = {
    "S": ["AG V", "VQ TT", "PQ CL", "VS IF"],
    "TT": ["F", "M"],
    "V": ["TP V2"],
    "V2": ["ID VL"],
    "VL": ["AS VL2", "ε"],
    "VL2": ["CM VL3", "N"],
    "VL3": ["ID CM"],
    "F": ["ID F2"],
    "F2": ["PA F3"],
    "F3": ["P F4"],
    "F4": ["PC F5"],
    "F5": ["LA F6"],
    "F6": ["C LC"],
    "P": ["TP ID"],
    "CL": ["PA CL2"],
    "CL2": ["V CL3"],
    "CL3": ["PT CL4"],
    "CL4": ["ID CL5"],
    "CL5": ["OP CL6"],
    "CL6": ["ON CL7"],
    "CL7": ["PT CL8"],
    "CL8": ["ID CL9"],
    "CL9": ["IN CL10"],
    "CL10": ["PT CL11"],
    "CL11": ["PC CL12"],
    "CL12": ["LA CL13"],
    "CL13": ["C LC"],
    "IF": ["PA IF2"],
    "IF2": ["CD IF3"],
    "IF3": ["PC IF4"],
    "IF4": ["LA IF5"],
    "IF5": ["C IF6"],
    "IF6": ["LC IF7"],
    "IF7": ["NS IF8"],
    "IF8": ["LA IF9"],
    "IF9": ["C LC"],
    "CD": ["ID CD2"],
    "CD2": ["OP ON"],
    "ON": ["ID", "N"],
    "M": ["SO M2"],
    "M2": ["PA M3"],
    "M3": ["PC M4"],
    "M4": ["LA M5"],
    "M5": ["C LC"],
}


# Define la ventana globalmente
ventana = tk.Tk()
ventana.title("Analizador de Cadena PDA")

# Campo de entrada de texto
etiqueta_entrada = tk.Label(ventana, text="Ingrese la cadena:")
etiqueta_entrada.pack()
entrada_texto = tk.Entry(ventana, width=150)
entrada_texto.pack()

# Cuadro de texto para mostrar el resultado y la pila
resultado_texto = tk.Text(ventana, height=15, width=50, state='disabled')
resultado_texto.pack()

# Redirigir stdout y stderr
sys.stdout = StdoutRedirector(resultado_texto)
sys.stderr = StdoutRedirector(resultado_texto)

# Función para analizar la cadena y actualizar resultado_texto
def analizar_cadena():
    cadena = entrada_texto.get()
    try:
        pda = PDA(grammar, terminals)
        es_valida = pda.parse(cadena)

        # No necesitas actualizar el resultado_texto aquí
        # porque ya está redirigido el stdout y stderr
        if es_valida:
            print("\nLa cadena está correctamente escrita.")
        else:
            print("\nLa cadena no está correctamente escrita.")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Botón para analizar la cadena
boton_analizar = tk.Button(ventana, text="Analizar Cadena", command=analizar_cadena)
boton_analizar.pack()

# Ejecutar la ventana
ventana.mainloop()