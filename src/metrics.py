import pandas as pd 
import numpy as np

df = pd.read_csv("data/processed/MXvideos_clean.csv", encoding="latin-1")


# conteo de la hora de publicacion

def conteo_horario_publicacion(df):
    hora_publicacion = df['publish_time'].dt.hour.value_counts()
    return hora_publicacion

# Agrupar por categorias y calcular metricas descriptivas
def tendencia_categoria(df):

    tendencias_categoria =(
        df.groupby('category_id')[['views','likes','dislikes','comment_count']]
        .agg(['mean','median','max','min'])
        .reset_index()
    )

    return tendencias_categoria


"""
Tasa de engagement (tasa de actividad)
La formula para calcular la tasa de engagement en Youtube, se suele medir el nivel de interaccion de los usuarios con respecto al numero de visualizaciones, por que los suscriptores no siempre ven los videos

INTERPRETACION

Menos de 2%: Bajo nivel de interaccion
Entre 2-5%: Aceptable.
Mas de 5%: Excelente, indica que tu contenido genera conversación y reacción
"""

# Metrica para calcular Tasa de engagement

def tasa_actividad(df):
    tasa_actividad = ((df['likes'] + df['comment_count']) / df['views'].replace(0,np.nan)) * 100
    return tasa_actividad


"""
Tasa de Rechazo
La tasa de rechazo = dislikes / views:

Dislikes: Señalan desaprobación o insatisfacción con el contenido.
Views : Base de referencia, por que cada vista es una oportunidad de reaccion.
INTERPRETACION

0 - 1%: Muy bajo rechazo -> tu contenido cumple expectativas, cada nadie lo desaprueba.
1- 3%: Rechazo moderado -> puede ser normal en temas polemicos o de nicho.
3 - 5%: Rechazo alto -> conviene revisar titulo, miniatura o calidad de contenido.
Más de 5%: Rechazo critico -> indica que el video genera frsutaciión, decepción o que el público siente que fue engañado
"""

# Metrica para calcular la tasa de rechazo

def tasa_rechazo(df):
    tasa_rechazo = (df['dislikes'] / df['views']) * 100
    return tasa_rechazo


"""
Ratio de comentarios
La metrica de Ratio de comentarios por 1000 vistas es muy util para medir la profuncidad del engagement en Youtube, por que los comentarios implican un esfuerzo mayor que un simple "like".

Comentarios: Reflejan conversación, debate o interés genuino.
Views: Base de referencia, cada vista es una oportunidad de comentar.
Multiplicar por 1000: normaliza la metrica para que sea mas facil comparar entre videos con distinto volumen vistas.
INTERPRETACION

0 - 2 comentarios/1000 vistas: bajo nivel de conversacion, la audiencia consume pero no participa.
3-5 comentarios/1000 vistas: nivel aceptable, hay interacción moderada.
6-10 comentarios/1000 vistas: buen engagement, tu contenido invita a opinar.
Mas de 10 comentarios/1000 vistas: excelente, tu video genera debate o fuerte conexion.
"""

# Metrica para calcular el ratio de comentarios

def ratio_comentarios(df):
    ratio_comentarios = (df['comment_count'] / df['views']) * 1000
    return ratio_comentarios


# Metrica Promedio de tasa_actividad, tasa_rechazo, ratio_comentarios por categoria

def promedio_ttr_categoria(df,ta,tr,rc):

    promedio_ttr_categoria = (
        df.groupby('category_id')[[ta,tr,rc]]
        .mean()
        .reset_index()
    )

    return promedio_ttr_categoria


# Metrica Promedio de tasa_actividad, tasa_rechazo, ratio_comentarios por franja_horaria

def promedio_ttr_franja_horaria(df,ta,tr,rc):

    promedio_ttr_franja_horaria = (
        df.groupby('franaja_horaria')[[ta,tr,rc]]
        .mean()
        .reset_index()
    )

    return promedio_ttr_franja_horaria


# Metrica Promedio de tasa_actividad, tasa_rechazo, ratio_comentarios por horario

def promedio_ttr_horario(df,ta,tr,rc):

    promedio_ttr_horario = (
        df.groupby('hour')[[ta,tr,rc]]
        .mean()
        .reset_index()
    )

    return promedio_ttr_horario


# Crear columnas de métricas en el DataFrame
df['tasa_actividad'] = tasa_actividad(df)
df['tasa_rechazo'] = tasa_rechazo(df)
df['ratio_comentarios'] = ratio_comentarios(df)

# Guardar dataset con métricas incluidas
df.to_csv("data/processed/MXvideos_metrics.csv", index=False, encoding="utf-8")
print("Dataset con métricas guardado en data/processed/MXvideos_metrics.csv")
