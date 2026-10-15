# GRAFICAS DEL ANALISIS
# Entrada : data/processed/MXvideos_metrics.csv
# Salida  : graficas/*.png

import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

AZUL = "#1F4E79"
os.makedirs("graficas", exist_ok=True)


# 1. Distribucion de vistas (escala logaritmica, porque la distribucion es muy asimetrica)
def plot_histogramas(df):
    plt.figure(figsize=(8, 5))
    plt.hist(np.log10(df["views"]), bins=40, color=AZUL)
    plt.axvline(np.log10(df["views"].median()), color="#C55A11", ls="--", label="Mediana")
    plt.title("Distribución de vistas")
    plt.xlabel("Vistas (escala log10)")
    plt.ylabel("Videos")
    plt.legend()
    plt.tight_layout()
    plt.savefig("graficas/h_views.png", dpi=150)
    plt.close()


# 2. Tasa de actividad mediana por categoria
def plot_tasa_actividad_categoria(df, min_videos=10):
    # Se excluyen categorias con muy pocos videos (p. ej. "Shows" tiene 3)
    conteo = df["categoria"].value_counts()
    df = df[df["categoria"].isin(conteo[conteo >= min_videos].index)]
    plt.figure(figsize=(10, 7))
    orden = df.groupby("categoria")["tasa_actividad"].median().sort_values(ascending=False).index
    sns.barplot(y="categoria", x="tasa_actividad", data=df, order=orden,
                estimator="median", errorbar=None, color=AZUL)
    plt.axvline(2, color="gray", ls=":")
    plt.axvline(5, color="gray", ls=":")
    plt.title("Tasa de Actividad Mediana por Categoría")
    plt.xlabel("Mediana de Tasa de Actividad (%)")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig("graficas/gb_tasa_actividad_categoria.png", dpi=150)
    plt.close()


# 3. Horarios optimos de publicacion (hora local de la Ciudad de Mexico)
def plot_horarios_optimos(df):
    por_hora = df.groupby("hour")["tasa_actividad"].median().reset_index()
    plt.figure(figsize=(10, 6))
    plt.bar(por_hora["hour"], por_hora["tasa_actividad"], color=AZUL)
    plt.axhline(2, color="gray", ls=":")
    plt.axhline(5, color="gray", ls=":")
    plt.title("Mediana de Tasa de Actividad por Hora de Publicación (hora de la Ciudad de México)")
    plt.xlabel("Hora")
    plt.ylabel("Mediana de Tasa de Actividad (%)")
    plt.xticks(range(0, 24))
    plt.tight_layout()
    plt.savefig("graficas/gb_horario_optimo.png", dpi=150)
    plt.close()


# 4. Correlacion entre vistas, likes, dislikes y comentarios
#    Spearman es mas confiable aqui porque los valores extremos distorsionan Pearson.
def plot_heatmap_metricas(df):
    columnas = ["views", "likes", "dislikes", "comment_count"]
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    for ax, metodo in zip(axes, ["pearson", "spearman"]):
        sns.heatmap(df[columnas].corr(metodo), annot=True, cmap="Blues", fmt=".2f",
                    vmin=0.3, vmax=1, cbar=False, ax=ax)
        ax.set_title(f"Correlación de {metodo.capitalize()}")
    plt.tight_layout()
    plt.savefig("graficas/hc_metricas.png", dpi=150)
    plt.close()


if __name__ == "__main__":
    df = pd.read_csv("data/processed/MXvideos_metrics.csv", encoding="utf-8")

    plot_histogramas(df)
    plot_tasa_actividad_categoria(df)
    plot_horarios_optimos(df)
    plot_heatmap_metricas(df)
    print("Gráficas guardadas en graficas/")