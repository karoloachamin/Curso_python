
###########Karol Dayana Loachamín Paucar: 1754679312############################

###########   VARIABLES Y POBLACIÓN OBJETIVO   #######################################
## Asignar la variable clave y la población objetivo ##
# variable_clave = "tipo_de_piso"
# poblacion_objetivo = "sexo == "Hombre"

###################################################################################################################3
# Así mismo se debe importar el paquete "pandas" el cual permite trabajar con conjuntos de datos estructurados.
import pandas as pd

# Se debe importar el paquete "numpy" para realizar las operaciones numéricas eficientes.
import numpy as np


# Desde "sklearn.model_selection" se debe importar varias funciones para poder dividir conjuntos de datos y realizar validación cruzada.
import sklearn
from sklearn.model_selection import train_test_split, KFold

# Se usará "sklearn.preprocessing" para preprocesar los datos antes de entrenar los modelos de aprendizaje automático.
from sklearn.preprocessing import StandardScaler

# El "sklearn.metrics"  proporcionará métricas para evaluar el rendimiento de los modelos.
from sklearn.metrics import accuracy_score

# El "statsmodels.api" permitirá realizar un análisis estadístico más detallado así como la estimación de modelos.
import statsmodels.api as sm

# Finalmente, se debe importar el paquete "matplotlib.pyplot" para que ayude a visualizar los datos y resultados.
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegressionCV
from sklearn.model_selection import cross_val_score
from statsmodels.discrete.discrete_model import Logit
from statsmodels.tools import add_constant
from sklearn.model_selection import KFold


##################################################################################################################
#########################################

# Cargar la base de datos originales
datos = pd.read_csv("sample_endi_model_10p.txt", sep=";")
# Eliminar filas con valores nulos en la columna "dcronica"
datos = datos[~datos["dcronica"].isna()]
variables = ['n_hijos', 'region', 'sexo', 'condicion_empleo','tipo_de_piso']

# Filtrar los datos de modo que se pueda incluir solo niños con sexo masculino y que tengan valores válidos en la columna 'tipo_de_piso'
datos_hombre_tipo_de_piso = datos[(datos['sexo'] == 'Hombre') & (datos['tipo_de_piso'].isin(['Adecuado', 'Cemento/Ladrillo', 'Tabla/Caña', 'Tierra']))]

# Calcular el conteo de niños por cada categoría de la variable 'tipo_de_piso'
conteo_tipo_de_piso = datos_hombre_tipo_de_piso['tipo_de_piso'].value_counts()
# Mostrar los resultados
print("Conteo de niños por categoría de 'tipo_de_piso':")
print(conteo_tipo_de_piso)
##################################################################################################################

# Eliminar filas con valores no finitos en las columnas especificadas
columnas_con_nulos = ['dcronica', 'region', 'n_hijos', 'tipo_de_piso', 'espacio_lavado', 'categoria_seguridad_alimentaria', 'quintil', 'categoria_cocina', 'categoria_agua', 'serv_hig']
datos_limpios = datos.dropna(subset=columnas_con_nulos)

# Comprobar si hay valores no finitos después de la eliminación
print("Número de valores no finitos después de la eliminación:")
print(datos_limpios.isna().sum())

# Convertir la variable categórica tipo_de_piso en binaria
datos_limpios['tipo_de_piso_binario'] = datos_limpios['tipo_de_piso'].apply(lambda x: 1 if x == 'Adecuado' else 0)

# Filtrar los datos para incluir solo niños con sexo masculino y que tengan valores válidos en la columna 'tipo_de_piso'
datos_hombre_tipo_de_piso = datos_limpios[(datos_limpios['sexo'] == 'Hombre') & (datos_limpios['tipo_de_piso_binario'] == 1)]

# Seleccionar las variables relevantes
variables = ['n_hijos', 'region', 'sexo', 'condicion_empleo', 'tipo_de_piso_binario']

# Filtrar los datos para las variables seleccionadas y eliminar filas con valores nulos en esas variables
for i in variables:
    datos_hombre_tipo_de_piso = datos_hombre_tipo_de_piso[~datos_hombre_tipo_de_piso[i].isna()]
# Agrupar los datos por sexo y tipo de piso que posee
# contar el número de niños en cada grupo

conteo_ninos_por_tipo_de_piso = datos_hombre_tipo_de_piso.groupby(["sexo", "tipo_de_piso_binario"]).size()

print("Conteo de niños por categoría de 'tipo_de_piso':")
print(conteo_ninos_por_tipo_de_piso)

# Definir las variables categóricas y numéricas
variables_categoricas = ['region', 'sexo', 'condicion_empleo']
variables_numericas = ['n_hijos']

#####################################################################################################################
# Crear un transformador para estandarizar las variables numéricas
transformador = StandardScaler()

# Crear una copia de los datos originales
datos_escalados = datos_limpios.copy()

# Estandarizar las variables numéricas
datos_escalados[variables_numericas] = transformador.fit_transform(datos_escalados[variables_numericas])

# Convertir las variables categóricas en variables dummy
datos_dummies = pd.get_dummies(datos_escalados, columns=variables_categoricas, drop_first=True)


# Seleccionar las variables predictoras (X) y la variable objetivo (y)
X = datos_dummies[['n_hijos', 'sexo_Mujer', 
                   'condicion_empleo_Empleada', 'condicion_empleo_Inactiva', 'condicion_empleo_Menor a 15 años']]

y = datos_dummies["tipo_de_piso_binario"]

# Definir los pesos asociados a cada observación
weights = datos_dummies['fexp_nino']

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test, weights_train, weights_test = train_test_split(X, y, weights, test_size=0.2, random_state=42)

# Asegurar que todas las variables sean numéricas
X_train = X_train.apply(pd.to_numeric, errors='coerce')
X_test = X_test.apply(pd.to_numeric, errors='coerce')
y_train = y_train.apply(pd.to_numeric, errors='coerce')

# Convertir las variables a tipo entero
variables = X_train.columns
for i in variables:
    X_train[i] = X_train[i].astype(int)
    X_test[i] = X_test[i].astype(int)

y_train = y_train.astype(int)

# Ajustar el modelo de regresión logística

modelo = sm.Logit(y_train, X_train)
result = modelo.fit(maxiter=100)  # Ajustar el número de iteraciones
print(result.summary())

result = modelo.fit()
print(result.summary())

# ¿Cuál es el valor del parámetro asociado a la variable clave si ejecutamos el modelo solo con el conjunto de entrenamiento 
#y predecimos con el mismo conjunto de entrenamiento? 

#Al ejecutar el modelo solo con el conjunto de entrenamiento y predecir con el mismo conjunto de entrenamiento, se puede examinar el coeficiente correspondiente en el resumen del modelo de regresión logística.
#INTERPRETACION
#El coeficiente estimado para la variable n_hijos es negativo (-0.8745), lo cual indica que hay una asociación negativa entre el número de hijos y la razón de probabilidad de tener un tipo de piso adecuado.
#El valor p (P>|z|) asociado a este coeficiente es menor que el nivel de significancia comúnmente utilizado de 0.05, podemos rechazar la hipótesis nula y concluir que hay evidencia estadística significativa 
#para sugerir que el coeficiente asociado a n_hijos es diferente de cero. En otras palabras, parece haber una asociación significativa entre el número de hijos y la probabilidad de tener un tipo de piso adecuado.

###########################################################################################################################
# Extraemos los coeficientes y los almacenamos en un DataFrame
coeficientes = result.params
df_coeficientes = pd.DataFrame(coeficientes).reset_index()
df_coeficientes.columns = ['Variable', 'Coeficiente']

# Creamos una tabla pivote para una mejor visualización
df_pivot = df_coeficientes.pivot_table(columns='Variable', values='Coeficiente')
df_pivot.reset_index(drop=True, inplace=True)

# Realizamos predicciones en el conjunto de prueba
predictions = result.predict(X_test)

# Convertimos las probabilidades en clases binarias
predictions_class = (predictions > 0.5).astype(int)

# Comparamos las predicciones con los valores reales
comparacion = (predictions_class == y_test)

# Definir el número de folds para la validación cruzada
kf = KFold(n_splits=100)
accuracy_scores = []  # Lista para almacenar los puntajes de precisión de cada fold
df_params = pd.DataFrame()  # DataFrame para almacenar los coeficientes estimados en cada fold

# Iterar sobre cada fold
for train_index, test_index in kf.split(X_train):
    # Dividir los datos en conjuntos de entrenamiento y prueba para este fold
    X_train_fold, X_test_fold = X_train.iloc[train_index], X_train.iloc[test_index]
    y_train_fold, y_test_fold = y_train.iloc[train_index], y_train.iloc[test_index]
    weights_train_fold, weights_test_fold = weights_train.iloc[train_index], weights_train.iloc[test_index]
    
    # Ajustar un modelo de regresión logística en el conjunto de entrenamiento de este fold
    log_reg = sm.Logit(y_train_fold, X_train_fold)
    result_reg = log_reg.fit()
    
    # Extraer los coeficientes y organizarlos en un DataFrame
    coeficientes = result_reg.params
    df_coeficientes = pd.DataFrame(coeficientes).reset_index()
    df_coeficientes.columns = ['Variable', 'Coeficiente']
    df_pivot = df_coeficientes.pivot_table(columns='Variable', values='Coeficiente')
    df_pivot.reset_index(drop=True, inplace=True)
    
    # Realizar predicciones en el conjunto de prueba de este fold
    predictions = result_reg.predict(X_test_fold)
    predictions = (predictions >= 0.5).astype(int)
    
    # Calcular la precisión del modelo en el conjunto de prueba de este fold
    accuracy = accuracy_score(y_test_fold, predictions)
    accuracy_scores.append(accuracy)
    
    # Concatenar los coeficientes estimados en este fold en el DataFrame principal
    df_params = pd.concat([df_params, df_pivot], ignore_index=True)


# Calcular la precisión promedio de la validación cruzada
mean_accuracy = np.mean(accuracy_scores)
print(f"Precisión promedio de validación cruzada: {mean_accuracy}")

# Calcular la precisión promedio
precision_promedio = np.mean(accuracy_scores)
print(precision_promedio)

##########################################################################################################################################################################################################################
#RESPUESTA FINAL: 
#Cuando se utiliza el conjunto de datos filtrado, la precisión promedio del modelo disminuye a 0.5506617647058824 en comparación con el valor anterior. Por el lado de la distribución de los coeficientes beta en comparación al ejercicio previo, 
# se necesitaría información adicional sobre los valores específicos de los coeficientes para los dos escenarios si se busca determinar si existe un aumento o disminución en cuanto a la distribución y la cantidad de este cambio.
####################################################################################################################################################

# Crear el histograma
plt.hist(accuracy_scores, bins=30, edgecolor='black')

# Añadir una línea vertical en la precisión promedio
plt.axvline(precision_promedio, color='blue', linestyle='dashed', linewidth=2)

# Añadir un texto que muestre la precisión promedio
plt.text(precision_promedio - 0.1, plt.ylim()[1] - 0.1, f'Precisión promedio: {precision_promedio:.2f}', 
         bbox=dict(facecolor='white', alpha=0.5))

# Configurar el título y etiquetas de los ejes
plt.title('Histograma de Accuracy Scores')
plt.xlabel('Accuracy Score')
plt.ylabel('Frecuencia')

# Ajustar los márgenes
plt.tight_layout()

# Mostrar el histograma
plt.show()


# Crear el histograma de los coeficientes para la variable "n_hijos"
plt.hist(df_params["n_hijos"], bins=30, edgecolor='black')

# Calcular la media de los coeficientes para la variable "n_hijos"
media_coeficientes_n_hijos = np.mean(df_params["n_hijos"])

# Añadir una línea vertical en la media de los coeficientes
plt.axvline(media_coeficientes_n_hijos, color='blue', linestyle='dashed', linewidth=2)

# Añadir un texto que muestre la media de los coeficientes
plt.text(media_coeficientes_n_hijos - 0.1, plt.ylim()[1] - 0.1, f'Media de los coeficientes: {media_coeficientes_n_hijos:.2f}', 
         bbox=dict(facecolor='white', alpha=0.5))

# Configurar título y etiquetas de los ejes
plt.title('Histograma de Beta (N Hijos)')
plt.xlabel('Valor del parámetro')
plt.ylabel('Frecuencia')

# Ajustar los márgenes
plt.tight_layout()

# Mostrar el histograma
plt.show()
