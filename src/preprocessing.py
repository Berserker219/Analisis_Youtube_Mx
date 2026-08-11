
# LIMPIEZA Y TRANSFORMACION DEL DATASET

import pandas as pd


data = pd.read_csv("data/raw/MXvideos.csv", encoding="latin-1")
data_copy = data.copy()

print(" ****Limpieza y transformacion del dataset.**** \n")

# LIMPIEZA DE DUPLICADOS
def limpieza_duplicados(df):
    duplicados = df.duplicated().sum()
    print(f"Numero de registros duplicados: {duplicados}")

    # muestra 8 registros duplicados
    # data_copy[data_copy.duplicated(keep=False)].sort_values(by='video_id').head(8)

    # Borrado de duplicados y muestra los duplicados actuales
    df.drop_duplicates(inplace=True)
    duplicados = df.duplicated().sum()
    print(f"Numero de registros duplicados: {duplicados}\n")
    return df


# TRANSFORMACION DE DATATIME A LA COLUMNA PUBLISH_TIME

def preprocesar_publish_time(df):
    # convertir la columna a datetime (quitando la z y la T automaticamente)
    df['publish_time'] = pd.to_datetime(df['publish_time'])
    # Quitar la informacion de zona horaria
    df['publish_time'] = df['publish_time'].dt.tz_localize(None)
    # Extaer la hora
    df['hour'] = df['publish_time'].dt.hour
    return df


# CREAR FRANJAS HORARIAS

# Crear función para clasificar franjas
def crear_franja_horaria(df):
    def clasificar_franja(hora):
        if 6 <= hora < 12:
            return 'mañana'
        elif 12 <= hora < 18:
            return 'tarde'
        else:
            return 'noche'
    df['franja_horaria'] = df['hour'].apply(clasificar_franja)
    return df




# TRANSFORMACION DE DATOS NULOS 

def limpieza_nulos(df):
    
    data_copy = df.assign(
        description=df['description'].fillna('ninguna'),
        tags=df['tags'].replace('[none]','ninguno')
        )

    
    return data_copy



# FUNCIONES

data_copy = limpieza_duplicados(data_copy)
data_copy = preprocesar_publish_time(data_copy)
data_copy = crear_franja_horaria(data_copy)
data_copy = limpieza_nulos(data_copy)

data_copy.to_csv("data/processed/MXvideos_clean.csv", index=False, encoding="utf-8")
print("Dataset limpio guardado en data/processed/MXvideos_clean.csv")

print("*" * 50)