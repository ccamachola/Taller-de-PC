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

# LECTURA DATASET
def leer_dataset(nombre_archivo):
    ruta = os.path.join('Data', nombre_archivo)
    # 1. Leer archivo
    try:
        datos = np.genfromtxt(ruta, delimiter=',', skip_header=1)
    except FileNotFoundError:
        print(f'ERROR: Archivo no encontrado: {ruta}')
        return None
    except Exception as e:
        print(f'ERROR: Fallo al leer el archivo: {e}')
        return None
    # 2. Verificar que no esté vacío
    if datos.size == 0:
        print('ERROR: El archivo está vacío o no tiene datos tras el encabezado.')
        return None
    # 3. Asegurar que sea siempre 2D (protección si hay una sola fila)
    if datos.ndim == 1:
        datos = datos.reshape(1, -1)
    # 4. Verificar número de columnas
    if datos.shape[1] != 4:
        print(f'ERROR: Formato incorrecto: se esperaban 4 columnas, se encontraron {datos.shape[1]}.')
        return None
    # 5. Eliminar filas completamente corruptas
    filas_corruptas = np.all(np.isnan(datos), axis=1)
    if filas_corruptas.any():
        print(f'Se eliminaron {filas_corruptas.sum()} fila(s) completamente corruptas.')
        datos = datos[~filas_corruptas]
    # 6. Detectar y eliminar filas con NaN parciales (strings mal leídos, celdas vacías)
    filas_con_nan = np.isnan(datos).any(axis=1)
    if filas_con_nan.any():
        indices = np.where(filas_con_nan)[0] + 2  # +2 por header e índice base 0
        print(f'0Filas con valores NaN en posiciones: {indices.tolist()} → eliminadas.')
        datos = datos[~filas_con_nan]
    # 7. Verificar que queden filas válidas tras la limpieza
    if datos.shape[0] == 0:
        print('ERROR: No quedaron filas válidas después de la limpieza.')
        return None
    # 8. Verificar tipo numérico
    if not np.issubdtype(datos.dtype, np.floating):
        print(f'ERROR: El dataset contiene tipos no numéricos: {datos.dtype}')
        return None
    print(f'Dataset validado: {datos.shape[0]} filas | {datos.shape[1]} columnas.')
    return datos

#CÁLCULOS ESTADÍSTICOS
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

#FILTADO DE OUTLIERS
def filtrar_outliers(datos):
    print("\n===== FILTRO DE OUTLIERS =====\n")
    #Datos a usar
    datos_numericos = datos[:,1:]

    #Calculos estadísticos
    medias = np.mean(datos_numericos, axis=0)
    desviaciones = np.std(datos_numericos, axis=0)
    outliers = np.abs(datos_numericos - medias) > (3*desviaciones)

    #Filas con outliers
    filas_outliers = np.any(outliers, axis=1)

    #Filas a eliminar 
    cantidad_eliminadas = np.sum(filas_outliers)
    datos_filtrados = datos[~filas_outliers]

    print(f"Filas eliminadas: {cantidad_eliminadas}")
    print(f"Filas restantes: {datos_filtrados.shape[0]}")
    return datos_filtrados

#EXPORTACION DATOS
def exportar_datos_limpios(datos, nombre_archivo="datos_limpios.csv"):
    print(f"\n===== EXPORTANDO DATOS =====")
    ruta = os.path.join("Data", nombre_archivo)
    
    # Encabezados requeridos
    header = "ID,Tiempo_s,Temperatura_C,Presion_hPa"
    
    try:
        # Asegurar carpeta Data
        if not os.path.exists("Data"):
            os.makedirs("Data")
            
        # Guardar el archivo
        np.savetxt(ruta, datos, delimiter=",", header=header, comments="", fmt="%.2f")
        print(f"Éxito: Datos limpios guardados correctamente en '{ruta}'.")
        
    except Exception as e:
        print(f"Error al intentar guardar el archivo de datos limpios: {e}")

if __name__ == "__main__":
    # Generamos el archivo inicial
    generar_dataset("dataset_sintetico.csv")
    # Leemos el dataset
    datos = leer_dataset("dataset_sintetico.csv")
    # Calculamos las estadísticas
    if datos is not None:
        calcular_estadisticas(datos)
        #Filtrar Outliers
        datos_limpios = filtrar_outliers(datos)
        print("\n=====ESTADÍSTICAS DESPUÉS DEL FILTRO=====")
        calcular_estadisticas(datos_limpios)
        #Exportar datos limpios
        exportar_datos_limpios(datos_limpios, "datos_limpios.csv")
