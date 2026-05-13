import numpy as np
import os

def generar_dataset(nombre_archivo, num_muestras=100):
    # Definir la ruta dentro de la carpeta Data
    ruta = os.path.join("Data", nombre_archivo)
    
    # 1. Crear datos base (distribución normal)
    ids = np.arange(1, num_muestras + 1)
    
    # Tiempo en segundos (0 a 1000)
    tiempo = np.linspace(0, 1000, num_muestras)
    
    # Temperatura: promedio 25°C con desviación de 2
    temperatura = np.random.normal(25, 2, num_muestras)
    
    # Presión: promedio 1013 hPa con desviación de 10
    presion = np.random.normal(1013, 10, num_muestras)
    
    # 2. Insertar OUTLIERS (Valores extremos para que el equipo los filtre)
    # Esto son 5 índices al azar para meter ruido
    indices_outliers = np.random.choice(num_muestras, 5, replace=False)
    
    temperatura[indices_outliers[0:2]] = 85.0  # Temperaturas muy altas
    presion[indices_outliers[2:5]] = 500.0     # Presiones muy bajas
    
    # 3. Combinar todo en una matriz
    # Lo puse horizontal para unir columnas
    dataset = np.column_stack((ids, tiempo, temperatura, presion))
    
    # 4. Guardar como CSV usando NumPy
    header = "ID,Tiempo_s,Temperatura_C,Presion_hPa"
    
    try:
        # Asegurarse de que la carpeta Data existe
        if not os.path.exists("Data"):
            os.makedirs("Data")
            
        np.savetxt(ruta, dataset, delimiter=",", header=header, comments="", fmt="%.2f")
        print(f" Dataset generado con éxito en: {ruta}")
        
    except Exception as e:
        print(f" Error al guardar el archivo: {e}")

# CÁLCULOS ESTADÍSTICOS
def leer_dataset(nombre_archivo):
    ruta = os.path.join("Data", nombre_archivo)
    
    try:
        datos = np.genfromtxt(ruta, delimiter=",", skip_header=1)
        return datos
    
    except FileNotFoundError:
        print("Error: El archivo no fue encontrado.")
        return None
    
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return None

def calcular_estadisticas(datos):
    # Excluir la columna ID
    datos_numericos = datos[:, 1:]
    nombres_columnas = [
        "Tiempo_s",
        "Temperatura_C",
        "Presion_hPa"
    ]
    print("\n===== ESTADÍSTICAS DEL DATASET =====\n")

    for i, nombre in enumerate(nombres_columnas):
        columna = datos_numericos[:, i]

        media = np.mean(columna)
        desviacion = np.std(columna)

        print(f"{nombre}")
        print(f"Media: {media:.2f}")
        print(f"Desviación estándar: {desviacion:.2f}")
        print()


if __name__ == "__main__":
    # Generamos el archivo inicial
    generar_dataset("dataset_sintetico.csv")
    # Leemos el dataset
    datos = leer_dataset("dataset_sintetico.csv")
    # Calculamos las estadísticas
    if datos is not None:
        calcular_estadisticas(datos)
