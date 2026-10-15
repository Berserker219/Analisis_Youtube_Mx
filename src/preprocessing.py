# LIMPIEZA Y TRANSFORMACION DEL DATASET
# Entrada : data/raw/MXvideos.csv
# Salida  : data/processed/MXvideos_clean.csv

import os
import pandas as pd

ZONA = "America/Mexico_City"


#Clasificacion estandar de YouTube (el CSV solo trae el id numerico)
CATEGORIAS = {
    1: "Cine y animación",
    2: "Autos y vehículos",
    10: "Música",
    15: "Mascotas y animales",
    17: "Deportes",
    19: "Viajes y eventos",
    20: "Videojuegos",
    22: "Gente y blogs",
    23: "Comedia",
    24: "Entretenimiento",
    25: "Noticias y política",
    26: "Consejos y estilo",
    27: "Educación",
    28: "Ciencia y tecnología",
    29: "ONG y activismo",
    43: "Shows",
}


COLUMNAS_UTILES = [
    "video_id",
    "category_id",
    "categoria",
    "title",          # opcional: no entra en las metricas, sirve para revisar casos sueltos
    "publish_time",
    "hour",
    "franja_horaria",
    "views",
    "likes",
    "dislikes",
    "comment_count",
]


# LIMPIEZA DE DUPLICADOS
def limpieza_duplicados(df):
    print(f"Registros duplicados antes: {df.duplicated().sum()}")
    df = df.drop_duplicates().copy()
    print(f"Registros duplicados despues: {df.duplicated().sum()}\n")
    return df
 
 
# FECHA Y HORA DE PUBLICACION (en hora de la Ciudad de Mexico)
def preprocesar_publish_time(df):
    # La 'Z' del texto indica UTC
    df["publish_time"] = pd.to_datetime(df["publish_time"], utc=True)
    # CONVERTIR (no borrar) a hora local; maneja el horario de verano
    df["publish_time"] = df["publish_time"].dt.tz_convert(ZONA)
    # Extraer la hora ya en hora local
    df["hour"] = df["publish_time"].dt.hour
    # Quitar la zona solo al final, para guardar en CSV
    df["publish_time"] = df["publish_time"].dt.tz_localize(None)
    return df
 
 
# FRANJAS HORARIAS (hora local)
def crear_franja_horaria(df):
    def clasificar_franja(hora):
        if 0 <= hora < 6:
            return "madrugada"
        elif 6 <= hora < 12:
            return "mañana"
        elif 12 <= hora < 18:
            return "tarde"
        return "noche"
 
    df["franja_horaria"] = df["hour"].apply(clasificar_franja)
    return df
 
 
# NOMBRE DE LA CATEGORIA
def asignar_nombre_categoria(df):
    df["categoria"] = df["category_id"].map(CATEGORIAS)
    sin_nombre = df.loc[df["categoria"].isna(), "category_id"].unique()
    if len(sin_nombre) > 0:
        print(f"Aviso: category_id sin nombre asignado: {sin_nombre}")
        df["categoria"] = df["categoria"].fillna("Otra")
    return df
 
 
# SOLO LAS COLUMNAS NECESARIAS
def eliminar_columnas_innecesarias(df, columnas_a_conservar):
    return df[columnas_a_conservar].copy()
 
 
if __name__ == "__main__":
    print(" ****Limpieza y transformacion del dataset.**** \n")
 
    # El archivo original esta en UTF-8 (con latin-1 los acentos salen dañados).
    # Hay 3 celdas de texto cortadas (tags/description), por eso errors="replace".
    data = pd.read_csv("data/raw/MXvideos.csv", encoding="utf-8", encoding_errors="replace")
 
    data = limpieza_duplicados(data)
    data = preprocesar_publish_time(data)
    data = crear_franja_horaria(data)
    data = asignar_nombre_categoria(data)
    data = eliminar_columnas_innecesarias(data, COLUMNAS_UTILES)
 
    os.makedirs("data/processed", exist_ok=True)
    data.to_csv("data/processed/MXvideos_clean.csv", index=False, encoding="utf-8")
    print("Dataset limpio guardado en data/processed/MXvideos_clean.csv")
 