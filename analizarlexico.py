# Resultado del análisis
resultado_lexema = []
# aqui declarar todas las normas

opAritmeticos = ["-~", "+~", "!~", "*~", "^~", "/~", "modulo~"]
opRelacionales = [":=:", ":<>:", ":<:", ":<=:", ":>:", ":>=:"]
opLogicos = ["Y", "O", "NOP", "xor", "implies", "equivalent"]
opAsignacion = ["::==", "**==", "//==", "++==", "--==", "-->>"]
simbolosAbrir = ["=(", "=[", "={", "='", '="']
simbolosCerrar = ["=)", "=]", "=}", "='", '="']
terminales = ["~:", "~;"]
separadores = [":/" r"\n"]
palabrasBucle = ["iterador", "mientras", "haga", "finhaga", ""]
palabrasDecision = ["si", "sino", "endsi", "caso", "endcaso"]
palabrasClases = ["clase", "interface", "publico", "privao", "estatico"]
identificadoresVariable = ["rav", ""]
identificadoresMetodo = ["tionfun"]
palabrasTipoDato = ["ent32", "ent64", "dec", "cadena", "car"] 
letras = [
    "a",
    "A",
    "b",
    "B",
    "c",
    "C",
    "d",
    "D",
    "e",
    "E",
    "f",
    "F",
    "g",
    "G",
    "h",
    "H",
    "i",
    "I",
    "j",
    "J",
    "k",
    "K",
    "l",
    "L",
    "m",
    "M",
    "n",
    "N",
    "ñ",
    "Ñ",
    "o",
    "O",
    "p",
    "P",
    "q",
    "Q",
    "r",
    "R",
    "s",
    "S",
    "t",
    "T",
    "u",
    "U",
    "v",
    "V",
    "w",
    "W",
    "x",
    "X",
    "y",
    "Y",
    "z",
    "Z",
]
numeros = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
simbolos = ["$", "_"]

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
    + letras
    + numeros
    + simbolos
)


# Funcion para analizar el input
def analizador_lexico(data):
    palabras = data.split() # Convierte el input (data) en palabras
    cont = 1
    for palabra in palabras:
        # Se valida que la palabra este en el diccionario de tokens
        if palabra in token:
            # Se comienza a validar en que diccionario está la palabra y se agrega a la lista resultado_lexema
            if palabra in opAritmeticos:
                resultado_lexema.append(f"Operador Aritmetico: {palabra}")
            elif palabra in opLogicos:
                resultado_lexema.append(f"Operador Logico: {palabra}")
            elif palabra in opRelacionales:
                resultado_lexema.append(f"Operador Relacional: {palabra}")
            elif palabra in opAsignacion:
                resultado_lexema.append(f"Operador de Asignacion: {palabra}")
            elif palabra in simbolosAbrir:
                resultado_lexema.append(f"Simbolo de Apertura: {palabra}")
            elif palabra in simbolosCerrar:
                resultado_lexema.append(f"Simbolo de Cierre: {palabra}")
            elif palabra in terminales:
                resultado_lexema.append(f"Terminal: {palabra}")
            elif palabra in separadores:
                resultado_lexema.append(f"Separador: {palabra}")
            elif palabra in palabrasBucle:
                resultado_lexema.append(f"Palabra de Bucle: {palabra}")
            elif palabra in palabrasDecision:
                resultado_lexema.append(f"Palabra de Decision: {palabra}")
            elif palabra in palabrasClases:
                resultado_lexema.append(f"Palabra de Clase: {palabra}")
            elif palabra in numeros:
                resultado_lexema.append(f"Numero: {palabra}")
            elif palabra in simbolos:
                resultado_lexema.append(f"Simbolo: {palabra}")
            else:
                resultado_lexema.append(f"Identificador: {palabra}")
        else:
            flagError = False
            if palabra[0] in letras:# Se valida que el primer caracter de la palabra sea una letra, para comenzar a validar si es un identificador
                for caracter in palabra:
                    # De ser el primer caracter una letra, se valida con este for los demás caracteres para verificar que cumpla con los token
                    if (
                        caracter not in numeros
                        and caracter not in letras
                        and caracter not in simbolos
                    ):
                        flagError = True # Si encuentra un caracter que no pertenece a los token, marca la flag como true
                        break
            else:
                flagError = True # Si el primer caracter no es una letra marca la flag como true
            if flagError:
                resultado_lexema.append(f"Error: {palabra}") # Agrega el error al resultado_lexema
            else:
                resultado_lexema.append(f"Identificador: {palabra}") # Agrega la palabra como un identificador si todos sus caracteres son token validos
        if cont < len(palabras):
            resultado_lexema.append(f" => ") # Imprime un separador luego de validar que el contador sea menor a la longitud del input
        cont += 1
    if palabras[-1] not in terminales: # Imprime un error si no se termina con un simbolo terminal
        resultado_lexema.append(f" => Error: Falta el terminal al final de la línea ")

    return resultado_lexema # Retorna el resultado 


if __name__ == "__main__":
    while True:
        data = input("Ingrese el código: ") # Pide el input
        resultado_lexema = []  # Reiniciar la lista en cada iteración
        analizador_lexico(data)
        print("".join(resultado_lexema)) # Imprime la lista resultado_lexema como un String