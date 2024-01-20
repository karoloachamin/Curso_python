######################################################################################################
#######################ACTIVIDAD 2 ###################################################################

mi_variable_01 = "Hola, que tal, soy Karol :)"
print(mi_variable_01)

##Lista de numeros
quintil_01 = [1, 2, 3, 4, 5]
print(quintil_01)

##Diccionario
mi_diccionario = { "clave_1" : "valor1", "clave_2" : "valor2", "clave_3" : "valor3" }
print(mi_diccionario)

#####################################################################################################
vector_de_enteros = [10]*4
print(vector_de_enteros)

vector_flotantes = [24.5]*2
print(vector_flotantes)

diccionario={ "n_enteros" : vector_de_enteros, "n_flotantes" : vector_flotantes}
print(diccionario)

vector_complejo = [(3 + 7j)] * 9
print(vector_complejo)

#Creación de cadenas 
cadena_simple = 'Hola mundo!'
print(cadena_simple)
cadena_doble = "Este es un curso muy interesante, Me gusta aprender"
print(cadena_doble)
############################################################################################################
# Uso de pandas para la lectura de una tabla Excel 

#con "pd" llamamos a la librería pandas
import pandas as pd

# Crear un DataFrame con los datos de rendimiento en participaciones en juegos

datos = {
    'Participante': ['Richard', 'Nicolas', 'Nathaly', 'Shirley'],
    'Juego 1 (puntos)': [150, 180, 130, 200],
    'Juego 2 (puntos)': [120, 90, 110, 150],
    'Juego 3 (puntos)': [200, 160, 180, 190]
}

df = pd.DataFrame(datos)

# Mostrar el DataFrame
print(df)




