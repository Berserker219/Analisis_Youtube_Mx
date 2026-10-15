# METRICAS DE ENGAGEMENT
# Entrada : data/processed/MXvideos_clean.csv
# Salidas : data/processed/MXvideos_metrics.csv
#           data/processed/resumen_categoria.csv
#           data/processed/resumen_franja_horaria.csv
#           data/processed/resumen_hora.csv

import numpy as np
import pandas as pd

METRICAS = ["tasa_actividad", "tasa_rechazo", "ratio_comentarios"]


"""
Tasa de engagement (tasa de actividad)
Mide la interaccion de los usuarios con respecto al numero de visualizaciones,
porque los suscriptores no siempre ven los videos.

INTERPRETACION

Menos de 2%: Bajo nivel de interaccion
Entre 2-5%: Aceptable.
Mas de 5%: Excelente, indica que tu contenido genera conversacion y reaccion
"""

def tasa_actividad(df):
    return ((df["likes"] + df["comment_count"]) / df["views"].replace(0, np.nan)) * 100


"""
Tasa de Rechazo = dislikes / views

Dislikes: señalan desaprobacion o insatisfaccion con el contenido.
Views: base de referencia, cada vista es una oportunidad de reaccion.

INTERPRETACION

0 - 1%: Muy bajo rechazo -> el contenido cumple expectativas.
1 - 3%: Rechazo moderado -> puede ser normal en temas polemicos o de nicho.
3 - 5%: Rechazo alto -> conviene revisar titulo, miniatura o calidad de contenido.
Mas de 5%: Rechazo critico -> el video genera frustracion o decepcion.
"""

def tasa_rechazo(df):
    return (df["dislikes"] / df["views"].replace(0, np.nan)) * 100


"""
Ratio de comentarios por 1000 vistas
Mide la profundidad del engagement, porque comentar implica mas esfuerzo que un "like".
Multiplicar por 1000 normaliza la metrica para comparar videos con distinto volumen de vistas.

INTERPRETACION

0 - 2 comentarios/1000 vistas: bajo nivel de conversacion.
3 - 5 comentarios/1000 vistas: nivel aceptable.
6 - 10 comentarios/1000 vistas: buen engagement.
Mas de 10 comentarios/1000 vistas: excelente, el video genera debate.
"""

def ratio_comentarios(df):
    return (df["comment_count"] / df["views"].replace(0, np.nan)) * 1000


# Conteo de videos publicados por hora (hora local)
def conteo_horario_publicacion(df):
    return df["hour"].value_counts().sort_index()


# Resumen de las tres metricas por grupo. Usa la MEDIANA porque las
# distribuciones tienen colas muy largas (la media esta distorsionada por videos virales).
def resumen_metricas(df, por):
    return (
        df.groupby(por)
        .agg(
            videos=("video_id", "size"),
            vistas_mediana=("views", "median"),
            tasa_actividad=("tasa_actividad", "median"),
            tasa_rechazo=("tasa_rechazo", "median"),
            ratio_comentarios=("ratio_comentarios", "median"),
        )
        .round(2)
        .reset_index()
    )


# Descriptivos de likes, dislikes, comentarios y vistas por categoria
def tendencia_categoria(df):
    return (
        df.groupby("categoria")[["views", "likes", "dislikes", "comment_count"]]
        .agg(["mean", "median", "max", "min"])
        .reset_index()
    )


if __name__ == "__main__":
    # Lee en UTF-8 (asi se guardo) y vuelve a convertir publish_time a fecha
    df = pd.read_csv(
        "data/processed/MXvideos_clean.csv",
        encoding="utf-8",
        parse_dates=["publish_time"],
    )

    df["tasa_actividad"] = tasa_actividad(df)
    df["tasa_rechazo"] = tasa_rechazo(df)
    df["ratio_comentarios"] = ratio_comentarios(df)

    df.to_csv("data/processed/MXvideos_metrics.csv", index=False, encoding="utf-8")
    print("Dataset con métricas guardado en data/processed/MXvideos_metrics.csv")

    resumen_metricas(df, "categoria").sort_values("tasa_actividad", ascending=False).to_csv(
        "data/processed/resumen_categoria.csv", index=False, encoding="utf-8"
    )
    resumen_metricas(df, "franja_horaria").to_csv(
        "data/processed/resumen_franja_horaria.csv", index=False, encoding="utf-8"
    )
    resumen_metricas(df, "hour").to_csv(
        "data/processed/resumen_hora.csv", index=False, encoding="utf-8"
    )
    print("Resúmenes por categoría, franja horaria y hora guardados en data/processed/")

    print("\nVideos publicados por hora:")
    print(conteo_horario_publicacion(df).to_string())