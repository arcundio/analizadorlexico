import tkinter as tk
from tkinter import ttk, messagebox

# Definición del analizador léxico
resultado_lexema = []

opAritmeticos = ["-~", "+~", "!~", "*~", "^~", "/~", "modulo~"]
opRelacionales = [":=:", ":<>:", ":<:", ":<=:", ":>:", ":>=:"]
opLogicos = ["Y", "O", "NOP", "xor", "implies", "equivalent"]
opAsignacion = ["::==", "**==", "//==", "++==", "--==", "-->>"]
simbolosAbrir = ["=(", "=[", "={", "='", '="']
simbolosCerrar = ["=)", "=]", "=}", "='", '="']
terminales = ["~:", "~;"]
separadores = [":/", r"\n"]
palabrasBucle = ["iterador", "mientras", "haga", "finhaga", "entonces"]
palabrasDecision = ["si", "sino", "endsi", "caso", "endcaso"]
palabrasClases = ["clase", "interface", "publico", "privado", "estatico"]
palabrasTipoDato = ["ent32", "ent64", "dec", "cadena", "car"]
letras = [chr(i) for i in range(97, 123)] + [chr(i) for i in range(65, 91)] + ["ñ", "Ñ"]
numeros = [str(i) for i in range(10)]
simbolos = ["$", "_", ""]

token = (
    opAritmeticos
    + opLogicos
    + opRelacionales
    + opAsignacion
    + simbolosAbrir
    + simbolosCerrar
    + terminales
    + separadores
    + palabrasBucle
    + palabrasClases
    + palabrasDecision
    + palabrasTipoDato
    + letras
    + numeros
    + simbolos
)

def analizador_lexico(data):
    resultado_lexema = []
    lineas = data.split('\n')  # Dividir el input en líneas
    for linea_num, linea in enumerate(lineas, start=1):
        palabras = linea.split()  # Convertir cada línea en palabras
        in_texto = False  # Bandera para indicar si estamos dentro de un texto
        texto = ""  # Variable para almacenar el texto si estamos dentro de uno
        for palabra in palabras:
            # Verificar si la palabra es el inicio de un texto
            if palabra.startswith('""') and not in_texto:
                in_texto = True
                texto += palabra[2:]  # Agregar el texto sin las comillas iniciales
            # Verificar si la palabra es el fin de un texto
            elif palabra.endswith('""') and in_texto:
                in_texto = False
                texto += " " + palabra[:-2]  # Agregar el texto sin las comillas finales
                resultado_lexema.append((texto, "Texto", linea_num))
                texto = ""  # Reiniciar la variable de texto
            # Si estamos dentro de un texto, agregar las palabras al texto
            elif in_texto:
                texto += " " + palabra
            else:
                # Si la palabra coincide con una función, analizarla
                if palabra.endswith("()") and palabra[:-2] in token:
                    funcion = palabra[:-2]
                    resultado_lexema.append((funcion, "Identificador", linea_num))
                    resultado_lexema.append(("=(", "Símbolo de Apertura", linea_num))
                    resultado_lexema.append((")", "Símbolo de Cierre", linea_num))
                # Si la palabra es un tipo de dato
                elif palabra in palabrasTipoDato:
                    resultado_lexema.append((palabra, "Tipo de Dato", linea_num))
                # Si la palabra es una palabra de decisión
                elif palabra in palabrasDecision:
                    resultado_lexema.append((palabra, "Palabra de Decisión", linea_num))
                # Si la palabra es una palabra de bucle
                elif palabra in palabrasBucle:
                    resultado_lexema.append((palabra, "Palabra de Bucle", linea_num))
                # Si la palabra es una palabra de clase
                elif palabra in palabrasClases:
                    resultado_lexema.append((palabra, "Palabra de Clase", linea_num))
                # Si la palabra es un operador lógico
                elif palabra in opLogicos:
                    resultado_lexema.append((palabra, "Operador Lógico", linea_num))
                # Si la palabra es un identificador
                elif palabra[0] in letras:
                    resultado_lexema.append((palabra, "Identificador", linea_num))
                # Si la palabra es un número
                elif palabra.isdigit():
                    resultado_lexema.append((palabra, "Número", linea_num))
                else:
                    # Se verifica si es un símbolo
                    if palabra in token:
                        if palabra in opAritmeticos:
                            resultado_lexema.append((palabra, "Operador Aritmético", linea_num))
                        elif palabra in opRelacionales:
                            resultado_lexema.append((palabra, "Operador Relacional", linea_num))
                        elif palabra in opAsignacion:
                            resultado_lexema.append((palabra, "Operador de Asignación", linea_num))
                        elif palabra in simbolosAbrir:
                            resultado_lexema.append((palabra, "Símbolo de Apertura", linea_num))
                        elif palabra in simbolosCerrar:
                            resultado_lexema.append((palabra, "Símbolo de Cierre", linea_num))
                        elif palabra in terminales:
                            resultado_lexema.append((palabra, "Terminal", linea_num))
                        elif palabra in separadores:
                            resultado_lexema.append((palabra, "Separador", linea_num))
                    else:
                        # Si no se reconoce, se considera un error
                        resultado_lexema.append((palabra, "Error", linea_num))
        if palabras and palabras[-1] not in terminales and linea_num == len(lineas):  # Imprime un error si no se termina con un símbolo terminal
            resultado_lexema.append(("Falta el terminal al final de la línea", "Error", linea_num))

    return resultado_lexema  # Retorna el resultado


# Creación de la interfaz gráfica usando Tkinter
class AnalizadorLexicoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador Léxico")

        # Marco para la entrada de texto
        frame_input = tk.Frame(root)
        frame_input.pack(fill=tk.BOTH, expand=True)

        self.text_input = tk.Text(frame_input, height=15, width=80)
        self.text_input.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.analyze_button = tk.Button(root, text="Analizar", command=self.analyze_code)
        self.analyze_button.pack(pady=5)

        self.clear_button = tk.Button(root, text="Limpiar", command=self.clear_text)
        self.clear_button.pack(pady=5)

        # Marco para la tabla de resultados
        frame_output = tk.Frame(root)
        frame_output.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(frame_output, columns=("Palabra", "Característica", "Línea"), show="headings", height=10)
        self.tree.heading("Palabra", text="Palabra")
        self.tree.heading("Característica", text="Característica")
        self.tree.heading("Línea", text="Línea")
        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(frame_output, orient="vertical", command=self.tree.yview)
        self.scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscroll=self.scrollbar.set)

    def analyze_code(self):
        code = self.text_input.get("1.0", tk.END).strip()
        if not code:
            messagebox.showerror("Error", "El área de texto está vacía. Por favor, ingrese el código a analizar.")
            return

        result = analizador_lexico(code)
        for i in self.tree.get_children():
            self.tree.delete(i)
        for word, feature, line in result:
            self.tree.insert("", tk.END, values=(word, feature, line))

    def clear_text(self):
        self.text_input.delete("1.0", tk.END)
        for i in self.tree.get_children():
            self.tree.delete(i)

if __name__ == "__main__":
    root = tk.Tk()
    app = AnalizadorLexicoApp(root)
    root.mainloop()
