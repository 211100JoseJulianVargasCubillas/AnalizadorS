import ply.lex as lex
import tkinter as tk
from tkinter import scrolledtext

result_lexema = []

reservadas = (
    'PAN',
    'PARAQUE',
    'AGUSTICIDAD',
    'UBUBUE',
    'VASIR',
    'NOVASIR',
    'VUELAOQUE',
    'SIONO'
)

tokens = reservadas + (
    'IDENTIFICADOR',
    'ENTERO',
    'LPAREN',
    'ID',
    'ASSIGN',
    'NUMBER',
    'SEMI',
    'GREATER',
    'INCREMENT',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'STRING',
    'MENOS',
    'MAS',
    'MULTI',
    'DIV',
    'IGUALMA',
    'IGUALMENO',
    'DOBLEIGUAL',
    'PUNTCOM',
    'MENOR',
)

t_LPAREN = r'\('
t_ASSIGN = r'='
t_GREATER = r'>'
t_INCREMENT = r'\+\+'
t_RPAREN = r'\)'
t_LBRACE = r'{'
t_RBRACE = r'}'
t_MAS = r'\+'
t_MENOS = r'-'
t_MULTI = r'\*'
t_DIV = r'\\'
t_IGUALMA = r'=>'
t_IGUALMENO = r'=<'
t_DOBLEIGUAL = r'=='
t_PUNTCOM = r';'
t_MENOR = r'<'

def t_PAN(t):
    r'pan'
    return t

def t_PARAQUE(t):
    r'paraque'
    return t

def t_AGUSTICIDAD(t):
    r'agusticidad'
    return t

def t_UBUBUE(t):
    r'ububue'
    return t

def t_VASIR(t):
    r'vasir'
    return t

def t_NOVASIR(t):
    r'novasir'
    return t

def t_VUELAOQUE(t):
    r'vuelaoque'
    return t

def t_SIONO(t):
    r'siono'
    return t

def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'"(?:\\"|[^"])*"'
    return t

t_SEMI = r';'
t_ignore = ' \t\n'

def reset_results():
    result_lexema.clear()
    text_widget.delete(1.0, tk.END)

def t_error(t):
    global result_lexema
    estado = "** Token no válido en la zona {:4} valor {:16} Posición {:4}".format(str(t.lineno), str(t.value),
                                                                                    str(t.lexpos))
    result_lexema.append(estado)
    text_widget.insert(tk.END, estado + "\n")
    t.lexer.skip(1)

def prueba(data):
    reset_results()
    analizador = lex.lex()
    analizador.input(data)

    while True:
        tok = analizador.token()
        if not tok:
            break
        estado = "Linea {:4} Tipo {:16} Valor {:16} Posición {:4}".format(str(tok.lineno), str(tok.type),
                                                                           str(tok.value), str(tok.lexpos))
        result_lexema.append(estado)
        text_widget.insert(tk.END, estado + "\n")

def on_submit(entry):
    data = entry.get()
    prueba(data)

# Crear la interfaz gráfica
window = tk.Tk()
window.title("Analizador Léxico")

frame = tk.Frame(window)
frame.pack(padx=10, pady=10)

entry = tk.Entry(frame, width=50)
entry.pack(side=tk.LEFT)

submit_button = tk.Button(frame, text="Analizar", command=lambda: on_submit(entry))
submit_button.pack(side=tk.LEFT)

reset_button = tk.Button(frame, text="Reiniciar", command=reset_results)
reset_button.pack(side=tk.LEFT)

text_widget = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=80, height=20)
text_widget.pack(padx=10, pady=10)

result_lexema = []

window.mainloop()