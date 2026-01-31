import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

df = pd.read_excel('Coffee2.xlsx', engine='openpyxl')

print(df.head())

# Limpiamos un poco el dataset
# Datos faltantes en el dataset
datos_faltantes = df.isnull().sum()
print("\nCantidad de datos faltantes en cada columna:")
print(datos_faltantes)

#Categoria 'En un día normal, ¿Cuántas veces tomas café?' fixing 
Opciones = df['En un día normal, ¿Cuántas veces tomas café?'].unique()
print(f"Las opciones de la columna 'En un día normal, ¿Cuántas veces tomas café?' son: {Opciones}")
# Diccionario de Mapeo de categorías
mapeo_categorias = {
    'Ninguna taza': 0,
    'Menos de una taza': 1/2,
    '1 a 3 tazas': 2,
    '4 a 6 tazas': 5,
    '6 o más tazas': 6 
}
# Verificación de que diccionario existe
print("Diccionario de mapeo:", mapeo_categorias)
# Creo una nueva columna con los valores numéricos
df['¿Cuántas veces tomas café?'] = df['En un día normal, ¿Cuántas veces tomas café?'].map(mapeo_categorias)
# Mostrar el DataFrame resultante
print(df)

# VALIDACIÓN LIMPIEZA Preferencia de tamaños de café 1
valores_Tamaños_de_café_1 = df['Tamaños de café 1'].unique()
print(f"\nValores únicos en la columna 'Tamaños de café 1': {valores_Tamaños_de_café_1}")
mapeo_nombres_simplificados_1 = {
    'C) Pequeño (0.35 litros)': 'Pequeño(0.35)',
    'B) Mediano (0.47 litros)': 'Mediano(0.47)',
    'A) Grande (0.59 litros)': 'Grande(0.59)'
}

print("Diccionario de mapeo tamaños:", mapeo_nombres_simplificados_1)

df['Tamaño_Café_1'] = df['Tamaños de café 1'].map(mapeo_nombres_simplificados_1)

# Mostrar el DataFrame resultante
print(df)

# VALIDACIÓN LIMPIEZA Preferencia de tamaños de café 2
valores_Tamaños_de_café_2 = df['Tamaños de café 2'].unique()
print(f"\nValores únicos en la columna 'Tamaños de café 2': {valores_Tamaños_de_café_2}")

mapeo_nombres_simplificados_2 = {
    'D) Pequeño (0.24 litros)': 'Pequeño(0.24)',
    'C) Mediano (0.35 litros)': 'Mediano(0.35)',
    'B) Grande (0.47 litros)': 'Grande(0.47)'
}
print("Diccionario de mapeo tamaños:", mapeo_nombres_simplificados_2)
df['Tamaño_Café_2'] = df['Tamaños de café 2'].map(mapeo_nombres_simplificados_2)
print(df)

# Columna 'Fecha Nacimiento' fixing
# Convertir la columna "Fecha Nacimiento" a tipo datetime
df['Fecha Nacimiento'] = pd.to_datetime(df['Fecha Nacimiento'])
# Eliminar la hora y dejar solo la fecha
df['Fecha Nacimiento'] = df['Fecha Nacimiento'].dt.date
# Mostrar el DataFrame resultante
print(df)

#Columna Nueva 'Edad'
def calcular_edad(Fecha_Nacimiento):
    hoy = datetime.today()
    edad = hoy.year - Fecha_Nacimiento.year
    if (hoy.month, hoy.day) < (Fecha_Nacimiento.month, Fecha_Nacimiento.day):
        edad -= 1
    return edad

df['Edad'] = df['Fecha Nacimiento'].apply(calcular_edad)
print(df)

# Columna 'Género' fixing
# Check if the column name exists in the DataFrame
if 'Género .1' not in df.columns:
    # If not found, try variations of the column name (e.g., different casing)
    possible_names = ['genero', 'GENERO', 'Genero']
    for name in possible_names:
        if name in df.columns:
            print(f"Found column with name '{name}'. Renaming to 'Género .1 '...")
            df = df.rename(columns={name: 'Género .1 '})
            break
    else:
        # If no variations are found, raise an exception or handle the error appropriately
        raise KeyError(f"Column 'Género' or its variations not found in the DataFrame.")
print(df)


#PREGUNTAS
#PREGUNTA 1. Cuanto suelen consumir las personas?
df['En un día normal, ¿Cuántas veces tomas café?'].value_counts()
print(df['En un día normal, ¿Cuántas veces tomas café?'].value_counts())
sns.countplot(x='En un día normal, ¿Cuántas veces tomas café?', data=df)

#PREGUNTA 2. ¿Cuántas personas respondieron "Sí" a "¿Te gusta el café?
Personas_Gusta_Cafe = df[df['¿Te gusta el café?\n'] == 'Si'].shape[0]
print(f"Personas a las que les gusta el café: {Personas_Gusta_Cafe}")

#PREGUNTA 3. ¿Qué porcentaje de personas que dijeron "Sí" a "¿Te gusta el café?" también respondieron "Sí" a "¿Tú tomas café?
Personas_que_toman_cafe = df[(df['¿Te gusta el café?\n'] == 'Si') & (df['¿Tú tomas café?'] == 'Si')].shape[0]
porcentaje = (Personas_que_toman_cafe / Personas_Gusta_Cafe) * 100
print(f"Porcentaje de personas que gustan y toman café: {porcentaje:.2f}%")

#PREGUNTA 4. ¿Cuál es la frecuencia promedio de consumo de café entre las personas que respondieron "Sí" a "¿Tú tomas café?
frecuencia_promedio = df[df['¿Tú tomas café?'] == 'Si']['¿Cuántas veces tomas café?'].mean()
print(f"Frecuencia promedio de consumo: {frecuencia_promedio:.2f} veces por día")

#PREGUNTA 5. ¿Qué proporción de personas que toman café lo hacen más de una vez al día?
proporcion = df[df['¿Cuántas veces tomas café?'] > 1].shape[0] / df.shape[0]
print(f"Proporción de personas que toman café más de una vez al día: {proporcion:.2f}")

#PREGUNTA 6. ¿Cuál es la cantidad de café más común entre las personas que respondieron "Sí" a "¿Tú tomas café?
cantidad_comun = df[df['¿Tú tomas café?'] == 'Si']['¿Cuántas veces tomas café?'].mode()
print(f"Cantidad de café más común: {cantidad_comun.values[0]} veces al día")

#PREGUNTA 7. ¿Existe una relación entre la edad y la frecuencia de consumo de café?
Relacion_Edad_Consumo = df.groupby('Edad')['¿Cuántas veces tomas café?'].mean()
print(Relacion_Edad_Consumo)

#PREGUNTA 8. ¿Qué carrera tiene la mayor proporción de personas que consumen café?
consumo_por_carrera = df[df['¿Tú tomas café?'] == 'Si']['¿Qué carrera estudias?'].value_counts(normalize=True)
print(consumo_por_carrera)

#PREGUNTA 9. ¿Las personas que trabajan consumen más café que las que no trabajan?
personas_trabajadoras_toman_cafe = df[df['¿Trabajas?'] == 'Si']['¿Tú tomas café?'].value_counts()
print(personas_trabajadoras_toman_cafe)

#PREGUNTA 10. ¿Existe alguna relación entre el sexo de la persona y su preferencia por el tamaño de café 1?
relacion_sexo_tamaño = df.groupby(['Género .1', 'Tamaños de café 1']).size().unstack()
print(relacion_sexo_tamaño)

#PREGUNTA 11. ¿Existe alguna relación entre el sexo de la persona y su preferencia por el tamaño de café 2?
relacion_sexo_tamaño_2 = df.groupby(['Género .1', 'Tamaños de café 2']).size().unstack()
print(relacion_sexo_tamaño_2)

#PREGUNTA 12. ¿Cuál es la edad promedio de las personas que prefieren el tamaño de café 1 "Pequeño (0.35 litros)"?
edad_promedio_pequeño = df[df['Tamaño_Café_1'] == 'Pequeño(0.35)']['Edad'].mean()
print(f"Edad promedio de personas que prefieren el tamaño 'Pequeño(0.35)': {edad_promedio_pequeño:.2f}")

#PREGUNTA 14. ¿Cuál es la edad promedio de las personas que prefieren el tamaño de café 1 "Mediano (0.47 litros)"?
edad_promedio_mediano = df[df['Tamaño_Café_1'] == 'Mediano(0.47)']['Edad'].mean()
print(f"Edad promedio de personas que prefieren el tamaño 'Mediano(0.47)': {edad_promedio_mediano:.2f}")

#PREGUNTA 15. ¿Cuál es la edad promedio de las personas que prefieren el tamaño de café 1 "Grande (0.59 litros)"?
edad_promedio_grande = df[df['Tamaño_Café_1'] == 'Grande(0.59)']['Edad'].mean()
print(f"Edad promedio de personas que prefieren el tamaño 'Grande(0.59)': {edad_promedio_grande:.2f}")

#PREGUNTA 16. ¿Cuál es la edad promedio de las personas que prefieren el tamaño de café 2 "Pequeño (0.24)"?
edad_promedio_pequeño_2 = df[df['Tamaño_Café_2'] == 'Pequeño(0.24)']['Edad'].mean()
print(f"Edad promedio de personas que prefieren el tamaño 'Pequeño(0.24)': {edad_promedio_pequeño_2:.2f}")

#PREGUNTA 17. ¿Cuál es la edad promedio de las personas que prefieren el tamaño de café 2 "Mediano(0.35)"?
edad_promedio_mediano_2 = df[df['Tamaño_Café_2'] == 'Mediano(0.35)']['Edad'].mean()
print(f"Edad promedio de personas que prefieren el tamaño 'Mediano(0.35)': {edad_promedio_mediano_2:.2f}")

#PREGUNTA 18. ¿Cuál es la edad promedio de las personas que prefieren el tamaño de café 2 "Grande(0.47)"?
edad_promedio_grande_2 = df[df['Tamaño_Café_2'] == 'Grande(0.47)']['Edad'].mean()
print(f"Edad promedio de personas que prefieren el tamaño 'Grande(0.47)': {edad_promedio_grande_2:.2f}")

#PREGUNTA 19. Cual es el tamaño de cafe preferido 1? 
Tamaños_preferidos = df['Tamaños de café 1'].value_counts()
print(Tamaños_preferidos)

#PREGUNTA 20. Cual es el tamaño de cafe preferido 2?
Tamaños_preferidos_2 = df['Tamaños de café 2'].value_counts()
print(Tamaños_preferidos_2)

#PREGUNTA 21. ¿La proporción de hombres y mujeres que toman café es similar?
consumo_por_sexo = df[df['¿Tú tomas café?'] == 'Si']['Género .1'].value_counts(normalize=True)
print(consumo_por_sexo)

#PREGUNTA 22. ¿Las personas de ciertas carreras universitarias tienen una mayor propensión a consumir café?
consumo_por_carrera = df[df['¿Tú tomas café?'] == 'Si']['¿Qué carrera estudias?'].value_counts(normalize=True)
print(consumo_por_carrera)
Mayor_carrera = consumo_por_carrera.idxmax()
print(f"La carrera con la mayor proporción de personas que toman café es: {Mayor_carrera}")


#PERFIL IDEAL
# Filtrar solo a los consumidores frecuentes (más de 4 veces por día)
consumidores_frecuentes = df[df['¿Cuántas veces tomas café?'].notna()]

# Análisis del perfil general de consumidores frecuentes
print("Perfil general de consumidores frecuentes:")

# Sexo más común
sexo_mas_comun = consumidores_frecuentes['Género .1'].mode()[0]
print(f"- Sexo: {sexo_mas_comun}")

# Edad promedio
edad_promedio = consumidores_frecuentes['Edad'].mean()
print(f"- Edad promedio: {edad_promedio:.1f} años")

# Carrera más común
carrera_mas_comun = consumidores_frecuentes['¿Qué carrera estudias?'].mode()[0]
print(f"- Carrera más común: {carrera_mas_comun}")

# Proporción de personas que trabajan
proporcion_trabajadores = consumidores_frecuentes['¿Trabajas?'].value_counts(normalize=True).get('Si', 0) * 100
print(f"- Porcentaje de personas que trabajan: {proporcion_trabajadores:.1f}%")

# Frecuencia promedio de consumo
frecuencia_promedio = consumidores_frecuentes['¿Cuántas veces tomas café?'].mean()
print(f"- Frecuencia promedio de consumo: {frecuencia_promedio:.1f} veces por día")

# Contar la frecuencia de una variable por género
relacion_genero_consumo = df.groupby(['Género .1', '¿Tú tomas café?'])['¿Tú tomas café?'].count().unstack()
print(relacion_genero_consumo)

# Tabla cruzada para analizar relaciones
tabla_cruzada = pd.crosstab(df['Género .1'], df['¿Tú tomas café?'])
print(tabla_cruzada)



#GRAFICOS
#GRAFICO 1. Relación entre el sexo y el tamaño de café preferido
sns.countplot(data=consumidores_frecuentes, x='Tamaños de café 1')
plt.title("Distribución de Tamaño de Café 1 entre Consumidores Frecuentes")
plt.show()
sns.countplot(data=consumidores_frecuentes, x='Tamaños de café 2')
plt.title("Distribución de Tamaño de Café 2 entre Consumidores Frecuentes")
plt.show()

#GRAFICO 2.   Relación entre la edad y la frecuencia de consumo de café
sns.scatterplot(data=consumidores_frecuentes, x='Edad', y='¿Cuántas veces tomas café?')
plt.title("Relación entre Edad y Frecuencia de Consumo de Café")
plt.show()

#GRAFICO 3. Relación entre la edad y el tamaño de café preferido
sns.boxplot(data=consumidores_frecuentes, x='Tamaños de café 1', y='Edad')
plt.title("Relación entre Edad y Tamaño de Café 1")
plt.show()
sns.boxplot(data=consumidores_frecuentes, x='Tamaños de café 2', y='Edad')
plt.title("Relación entre Edad y Tamaño de Café 2")
plt.show()

#GRAFICO 4. Distribución género entre consumidores frecuentes
sns.countplot(data=consumidores_frecuentes, x='Género .1')
plt.title("Distribución de género entre Consumidores Frecuentes")
plt.show()

#GRAFICO 5. Distribución de carreras entre consumidores frecuentes
sns.countplot(data=consumidores_frecuentes, y='¿Qué carrera estudias?')
plt.title("Distribución de Carreras entre Consumidores Frecuentes")
plt.show()

#GRAFICO 6. Distribución de personas que trabajan entre consumidores frecuentes
sns.countplot(data=consumidores_frecuentes, x='¿Trabajas?')
plt.title("Distribución de Personas que Trabajan entre Consumidores Frecuentes")
plt.show()

#GRAFICO 7. Distribución de frecuencia de consumo de café entre consumidores frecuentes
sns.histplot(data=consumidores_frecuentes, x='¿Cuántas veces tomas café?')
plt.title("Distribución de Frecuencia de Consumo de Café entre Consumidores Frecuentes")
plt.show()

#GRAFICO 8. Distribución de edad entre consumidores frecuentes
sns.histplot(consumidores_frecuentes['Edad'], bins=5, kde=True)
plt.title("Distribución de Edad entre Consumidores Frecuentes")
plt.show()
