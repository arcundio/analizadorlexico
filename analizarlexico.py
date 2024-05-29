import tkinter as tk  # Importa el módulo Tkinter para crear la interfaz gráfica
from tkinter import ttk, messagebox  # Importa los submódulos ttk (para estilos) y messagebox
from graphviz import Digraph  # Importa la clase Digraph de GraphViz para dibujar autómatas
import tempfile  # Importa el módulo para manejar archivos temporales
import os  # Importa el módulo para interactuar con el sistema operativo
import re  # Importa el módulo para trabajar con expresiones regulares

# Definición del analizador léxico
resultado_lexema = []  # Lista para almacenar los tokens encontrados

# Definición de las listas de tokens
opAritmeticos = ["-kiss", "+kiss", "%kiss", "arribakiss", "ctrkiss", "modulo~"]
opComparacion = ["igual", "menorque", "mayorque", "menoroigualque", "mayoroigualque", "diferentede"]
opIncrementoDecremento = ["++incremento", "--decremento"]
opLogicos = ["Y", "O", "NOP", "xor", "implies", "equivalent"]
opAsignacion = ["==", "&==", "%==", "++==", "--==", "--&&"]
simbolosAbrir = ["abre(", "abre[", "abre{", "='", '="']
simbolosCerrar = ["cierra)", "cierra]", "cierra}", "='", '="']
terminales = ["kiss:", "kiss;"]
separadores = ["sep1", "esp2", ","]
palabrasBucle = ["gato", "mientras", "haga", "finhaga", "entonces", "para"]
palabrasDecision = ["si", "sino", "endsi", "caso", "endcaso"]
palabrasClases = ["clase", "interface", "publico", "privado", "estatico"]
palabrasTipoDato = ["ent32", "ent64", "dec", "cadena", "car"]
letras = [chr(i) for i in range(97, 123)] + [chr(i) for i in range(65, 91)] + ["ñ", "Ñ"]
numeros = [str(i) for i in range(10)]
simbolos = ["$", "_", ""]
palabrasClases = ["clase", "interface", "publico", "privado", "estatico"]
palabrasTipoDato = ["ent32", "ent64", "dec", "cadena", "car"]
letras = [chr(i) for i in range(97, 123)] + [chr(i) for i in range(65, 91)] + ["ñ", "Ñ"]
numeros = [str(i) for i in range(10)]
simbolos = ["$", "_", ""]

token = (
    opAritmeticos
    + opLogicos
    + opComparacion
    + opIncrementoDecremento
    + opAsignacion
    + simbolosAbrir
    + simbolosCerrar
    + terminales
    + separadores
    + palabrasBucle
    + palabrasClases
    + palabrasDecision
    + palabrasTipoDato
    + palabrasTipoDato
    + letras
    + numeros
    + simbolos
)

def analizador_lexico(data):
    """
    Función que analiza el código fuente y genera una lista de tokens.

    Args:
        data (str): El código fuente a analizar.

    Returns:
        list: Una lista de tuplas (token, tipo_token, num_linea).
    """
    resultado_lexema = []
    lineas = data.split('\n')
    in_block_comment = False
    for linea_num, linea in enumerate(lineas, start=1):
        if linea.startswith("¡¡!!"):  # Manejo de comentarios de línea
            resultado_lexema.append((linea, "Comentario", linea_num))
            continue

        if linea.startswith("¡¡&!"):  # Inicio de comentario de bloque
            in_block_comment = True
            linea = linea[5:]  # Eliminar los caracteres "¡¡&!"

        if linea.endswith("!&!!"):  # Final de comentario de bloque
            in_block_comment = False
            linea = linea[:-5]  # Eliminar los caracteres "!&!!"

        if in_block_comment:
            resultado_lexema.append((linea, "Comentario", linea_num))
            continue

        palabras = linea.split()
        in_texto = False
        texto = ""
        for palabra in palabras:
            if palabra.startswith('""') and not in_texto:  # Manejo de cadenas de texto
                in_texto = True
                texto += palabra[2:]
            elif palabra.endswith('""') and in_texto:
                in_texto = False
                texto += " " + palabra[:-2]
                resultado_lexema.append((texto, "Texto", linea_num))
                texto = ""
            elif in_texto:
                texto += " " + palabra
            else:  # Análisis de tokens
                if re.match(r"^\d+\.\d+$", palabra):
                    resultado_lexema.append((palabra, "Número Real", linea_num))
                elif re.match(r"^\d+$", palabra):
                    resultado_lexema.append((palabra, "Número Entero", linea_num))
                elif palabra in palabrasTipoDato:
                    resultado_lexema.append((palabra, "Tipo de Dato", linea_num))
                elif palabra in opLogicos:
                    resultado_lexema.append((palabra, "Operador Logico", linea_num))
                elif palabra in palabrasDecision:
                    resultado_lexema.append((palabra, "Palabra de Decisión", linea_num))
                elif palabra in palabrasBucle:
                    resultado_lexema.append((palabra, "Palabra de Bucle", linea_num))
                elif palabra in palabrasClases:
                    resultado_lexema.append((palabra, "Palabra de Clase", linea_num))
                elif palabra in opAritmeticos:
                    resultado_lexema.append((palabra, "Operador Aritmético", linea_num))
                elif palabra in opComparacion:
                    resultado_lexema.append((palabra, "Operador de Comparación", linea_num))
                elif palabra in opIncrementoDecremento:
                    resultado_lexema.append((palabra, "Operador de Incremento/Decremento", linea_num))
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
                elif palabra[0] in letras:  # Identificadores
                    if len(palabra) > 10:
                        resultado_lexema.append((f"{palabra} (Error: Identificador demasiado largo)", "Error", linea_num))
                    else:
                        resultado_lexema.append((palabra, "Identificador", linea_num))
                else:  # Token no reconocido
                    resultado_lexema.append((f"{palabra} (Error: Token no reconocido)", "Error", linea_num))

    return resultado_lexema

def draw_automata(states, transitions, filename="automata"):
    """
    Función que crea un autómata a partir de una lista de estados y transiciones.

    Args:
        states (list): Lista de tuplas (nombre_estado, es_estado_final).
        transitions (list): Lista de tuplas (estado_origen, estado_destino, símbolo).
        filename (str, optional): Nombre del archivo de imagen del autómata. Por defecto es "automata".

    Returns:
        str: Ruta del archivo de imagen del autómata.
    """
    dot = Digraph()  # Crea un nuevo objeto Digraph

    for state in states:
        if state[1]:  # Si es un estado final
            dot.node(state[0], state[0], shape="doublecircle")  # Se dibuja con un círculo doble
        else:
            dot.node(state[0], state[0])  # Se dibuja con un círculo simple

    for transition in transitions:
        dot.edge(transition[0], transition[1], label=transition[2])  # Se dibuja la transición

    filepath = os.path.join(tempfile.gettempdir(), filename)  # Ruta del archivo temporal
    dot.render(filepath, format='png')  # Genera la imagen del autómata en formato PNG
    return filepath + ".png"  # Retorna la ruta de la imagen

def generate_token_automata(token):
    """
    Función que genera los estados y transiciones para un token dado.

    Args:
        token (str): El token a partir del cual se generará el autómata.

    Returns:
        tuple: Una tupla con dos listas:
            - states (list): Lista de tuplas (nombre_estado, es_estado_final).
            - transitions (list): Lista de tuplas (estado_origen, estado_destino, símbolo).
    """
    # Define los estados y transiciones para el token dado
    states = [("q0", False)]  # Inicializa la lista de estados con el estado inicial
    transitions = []  # Lista vacía para almacenar las transiciones

    # Agrega las transiciones basadas en el token
    for i in range(len(token)):
        current_state = f"q{i}"  # Nombre del estado actual
        next_state = f"q{i+1}"  # Nombre del siguiente estado
        transitions.append((current_state, next_state, token[i]))  # Agrega la transición
        states.append((next_state, True if i == len(token) - 1 else False))  # Agrega el siguiente estado

    return states, transitions  # Retorna las listas de estados y transiciones

def generate_automata_from_lexemes(lexemes):
    """
    Función que genera las imágenes de los autómatas para cada token encontrado.

    Args:
        lexemes (list): Lista de tuplas (token, tipo_token, num_linea).

    Returns:
        list: Lista de rutas de las imágenes de los autómatas generados.
    """
    automata_images = []  # Lista para almacenar las rutas de las imágenes

    for lexeme, type_, line in lexemes:
        if type_ == "Error":  # Omite los tokens de error
            continue

        # Definición de la expresión regular para caracteres no especiales
        # Se incluyen letras (mayúsculas y minúsculas), números, guión bajo, llaves, corchetes, doble punto, doble igual, guión, y símbolos de puntuación comunes
        valid_lexeme = re.sub(r'[^a-zA-Z0-9_{}[\]==\-.,;?!@#$%^&*()\'\" ]', '_', lexeme)

        # Genera el autómata para el token actual
        states, transitions = generate_token_automata(valid_lexeme)
        automata_image_path = draw_automata(states, transitions, filename=f"automata_{valid_lexeme}")
        automata_images.append(automata_image_path)  # Agrega la ruta de la imagen a la lista

    return automata_images  # Retorna la lista de rutas de las imágenes

class TextLineNumbers(tk.Canvas):
    """
    Clase que crea un lienzo para mostrar los números de línea en un widget de texto.
    """
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.textwidget = None  # Widget de texto al que estará asociado

    def attach(self, text_widget):
        """
        Asocia un widget de texto a este lienzo de números de línea.

        Args:
            text_widget (tk.Text): El widget de texto al que se asociará.
        """
        self.textwidget = text_widget

    def redraw(self, *args):
        """
        Función que se ejecuta cuando se actualiza el widget de texto.
        Dibuja los números de línea en el lienzo.
        """
        self.delete("all")  # Borra todo el contenido del lienzo

        i = self.textwidget.index("@0,0")  # Obtiene el índice de la primera línea
        while True:
            dline = self.textwidget.dlineinfo(i)  # Obtiene información de la línea actual
            if dline is None:
                break
            y = dline[1]  # Coordenada y de la línea
            linenum = str(i).split(".")[0]  # Número de línea
            self.create_text(2, y, anchor="nw", text=linenum, fill="gray")  # Dibuja el número de línea
            i = self.textwidget.index(f"{i}+1line")  # Avanza a la siguiente línea

class AnalizadorLexicoApp:
    """
    Clase principal de la aplicación de analizador léxico con interfaz gráfica.
    """
    def __init__(self, root):
        self.init(root)  # Inicializa la aplicación

    def init(self, root):
        """
        Función que inicializa la aplicación y crea la interfaz gráfica.

        Args:
            root (tk.Tk): La ventana principal de la aplicación.
        """
        self.root = root
        self.root.title("Analizador Léxico")  # Título de la ventana

        frame_input = tk.Frame(root)  # Frame para el área de entrada de texto
        frame_input.pack(fill=tk.BOTH, expand=True)

        self.text_input = tk.Text(frame_input, height=15, width=80)  # Widget de texto para la entrada
        self.text_input.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.linenumbers = TextLineNumbers(frame_input, width=30)  # Lienzo para los números de línea
        self.linenumbers.attach(self.text_input)  # Asocia el lienzo al widget de texto
        self.linenumbers.pack(side=tk.LEFT, fill=tk.Y)

        self.text_input.bind("<KeyRelease>", self.on_key_release)  # Evento para actualizar los números de línea

        self.analyze_button = tk.Button(root, text="Analizar", command=self.analyze_code)  # Botón para analizar el código
        self.analyze_button.pack(pady=5)

        self.clear_button = tk.Button(root, text="Limpiar", command=self.clear_text)  # Botón para limpiar el texto
        self.clear_button.pack(pady=5)

        self.automata_button = tk.Button(root, text="Generar Autómatas", command=self.generate_automata)  # Botón para generar autómatas
        self.automata_button.pack(pady=5)

        frame_output = tk.Frame(root)  # Frame para el área de salida
        frame_output.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(frame_output, columns=("Palabra", "Característica", "Línea"), show="headings", height=10)  # Tabla de resultados
        self.tree.heading("Palabra", text="Palabra")
        self.tree.heading("Característica", text="Característica")
        self.tree.heading("Línea", text="Línea")
        self.tree.column("Palabra", width=200)
        self.tree.column("Característica", width=200)
        self.tree.column("Línea", width=100)
        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def on_key_release(self, event):
        """
        Función que se ejecuta cuando se suelta una tecla en el widget de texto.
        Actualiza los números de línea.
        """
        self.linenumbers.redraw()

    def analyze_code(self):
        """
        Función que analiza el código fuente ingresado y muestra los resultados en la tabla.
        """
        data = self.text_input.get("1.0", tk.END)  # Obtiene el código fuente del widget de texto
        resultado_lexema = analizador_lexico(data)  # Analiza el código

        # Limpiar la vista del árbol
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Agregar los resultados al árbol
        for palabra, caracteristica, linea in resultado_lexema:
            self.tree.insert("", tk.END, values=(palabra, caracteristica, linea))

    def clear_text(self):
        """
        Función que limpia el texto del widget de entrada y la tabla de resultados.
        """
        self.text_input.delete("1.0", tk.END)  # Limpia el texto del widget de entrada
        # Limpiar la vista del árbol
        for item in self.tree.get_children():
            self.tree.delete(item)

    def generate_automata(self):
        """
        Función que genera y muestra los autómatas para los tokens encontrados.
        """
        data = self.text_input.get("1.0", tk.END)  # Obtiene el código fuente del widget de texto
        resultado_lexema = analizador_lexico(data)  # Analiza el código

        automata_image_paths = generate_automata_from_lexemes(resultado_lexema)  # Genera las imágenes de los autómatas

        if not automata_image_paths:
            messagebox.showerror("Error", "No se pudieron generar los autómatas.")  # Muestra un mensaje de error si no se generaron autómatas
            return

        # Mostrar las imágenes de los autómatas
        automata_windows = []
        for i, image_path in enumerate(automata_image_paths, start=1):
            automata_window = tk.Toplevel(self.root)  # Crea una nueva ventana para el autómata
            automata_window.title(f"Autómata {i}")  # Título de la ventana
            automata_window.geometry("800x600")  # Tamaño de la ventana

            scrollbar = tk.Scrollbar(automata_window, orient="vertical")  # Barra de desplazamiento vertical
            canvas = tk.Canvas(automata_window, yscrollcommand=scrollbar.set)  # Lienzo para mostrar la imagen
            scrollbar.config(command=canvas.yview)  # Configura la barra de desplazamiento
            scrollbar.pack(side="right", fill="y")
            canvas.pack(side="left", fill="both", expand=True)

            try:
                image = tk.PhotoImage(file=image_path)  # Carga la imagen del autómata
            except tk.TclError:
                messagebox.showerror("Error", f"No se pudo cargar la imagen del autómata {i}.")  # Muestra un mensaje de error si no se puede cargar la imagen
                automata_window.destroy()  # Cierra la ventana del autómata
                continue

            canvas.create_image(0, 0, anchor="nw", image=image)  # Dibuja la imagen en el lienzo
            canvas.config(scrollregion=canvas.bbox("all"))  # Configura la región de desplazamiento
            canvas.image = image  # Mantiene una referencia a la imagen para evitar que se elimine

            automata_windows.append(automata_window)  # Agrega la ventana del autómata a la lista

        # Mantener una referencia a las ventanas para evitar que se cierren prematuramente
        self.automata_windows = automata_windows

if __name__ == "__main__":
    root = tk.Tk()  # Crea la ventana principal de la aplicación
    app = AnalizadorLexicoApp(root)  # Crea una instancia de la aplicación
    root.mainloop()  # Inicia el bucle principal de la aplicación