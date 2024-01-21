import tkinter as tk
from tkinter import messagebox
import ply.lex as lex
import ply.yacc as yacc

reserved = {
    'pan': 'PAN',
    'Paraqoque': 'PARAQUE'
}

tokens = [
    'LPAREN',
    'ID',
    'ASSIGN',
    'NUMBER',
    'SEMI',
    'GREATER',
    'INCREMENT',
    'RPAREN',
    'LBRACE',
    'RBRACE'
] + list(reserved.values())

t_LPAREN = r'\('
t_ASSIGN = r'='
t_GREATER = r'>'
t_INCREMENT = r'\+\+'
t_RPAREN = r'\)'
t_LBRACE = r'{'
t_RBRACE = r'}'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')    # Check for reserved words
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_SEMI = r';'

t_ignore = ' \t\n'

def t_error(t):
    error_table.insert(tk.END, f"Illegal character '{t.value[0]}'\n")
    t.lexer.skip(1)

lexer = lex.lex()

def p_program(p):
    'program : PARAQUE LPAREN declaration SEMI condition SEMI increment SEMI RPAREN LBRACE ID RBRACE'
def p_declaration(p):
    'declaration : PAN ID ASSIGN NUMBER'

def p_condition(p):
    'condition : ID GREATER NUMBER'

def p_increment(p):
    'increment : ID INCREMENT'

def p_error(p):
    if p:
        error_table.insert(tk.END, f"Syntax error in token '{p.value}'\n")
    else:
        error_table.insert(tk.END, "Syntax error in EOF\n")

parser = yacc.yacc()

symbol_table = set()

def check_code():
    error_table.delete("1.0", tk.END)
    token_table.delete("1.0", tk.END)

    code = txt.get("1.0", tk.END).strip()
    if not code:
        messagebox.showinfo('Result', 'No code to verify.')
        return

    symbol_table.clear()

    lexer.input(code)

    for token in lexer:
        if token.type == 'DOUBLESTRING':
            value = token.value[1:-1]
        else:
            value = token.value
        token_table.insert(tk.END, f"{token.type}: {value}\n")

    result = parser.parse(code, lexer=lexer)

    if not error_table.get("1.0", tk.END).strip():
        messagebox.showinfo('Result', 'Syntax analysis is correct.')
    else:
        messagebox.showerror('Result', 'Syntax errors were found.')

root = tk.Tk()
root.title("Lexical, Syntactic, and Semantic Analyzer")

codigo = 'Paraqoque(pan i=0; i > 12; i++;){contenido}'

txt = tk.Text(root, width=55, height=10)
txt.pack()
txt.insert(tk.END, codigo)

btn = tk.Button(root, text="Analyze", command=check_code)
btn.pack()

token_table = tk.Text(root, height=10, width=40)
token_table.pack(padx=10, pady=5)

error_table = tk.Text(root, height=10, width=40)
error_table.pack(padx=10, pady=5)

root.mainloop()