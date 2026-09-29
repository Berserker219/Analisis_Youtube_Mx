import matplotlib.pyplot as plt
import seaborn as sns
import os

# Crear carpeta graficas si no existe
os.makedirs("graficas", exist_ok=True)

# 1. Gráficas de barras de métricas por categoría
def plot_metricas_por_categoria(df):
    fig, axes = plt.subplots(1, 3, figsize=(18,6))

    sns.barplot(x='category_id', y='tasa_actividad', data=df, ax=axes[0])
    axes[0].set_title('Tasa de actividad promedio por categoría')

    sns.barplot(x='category_id', y='tasa_rechazo', data=df, ax=axes[1])
    axes[1].set_title('Tasa de rechazo promedio por categoría')

    sns.barplot(x='category_id', y='ratio_comentarios', data=df, ax=axes[2])
    axes[2].set_title('Ratio de comentarios promedio por categoría')

    plt.tight_layout()
    plt.savefig("graficas/gb_metrica_categoria.png")
    

# 2. Horarios óptimos de publicación
def plot_horarios_optimos(df):
    horarios_optimos = df.groupby('hour')[['tasa_actividad']].mean().reset_index()
    plt.figure(figsize=(10,6))
    plt.bar(horarios_optimos['hour'], horarios_optimos['tasa_actividad'])
    plt.title('Promedio de Tasa de Actividad por Hora')
    plt.xlabel('Hora')
    plt.ylabel('Promedio de Tasa de Actividad')
    plt.xticks(range(0,24))
    plt.savefig("graficas/gb_horario_optimo.png")
    

# 3. Promedio de tasa de actividad por categoría
def plot_tasa_actividad_categoria(df):
    plt.figure(figsize=(10,6))
    sns.barplot(x='category_id', y='tasa_actividad', data=df)
    plt.title("Promedio de Tasa de Actividad por Categoría")
    plt.ylabel("Promedio de Tasa de Actividad")
    plt.xlabel("Categoría")
    plt.savefig("graficas/gb_tasa_activdidad_categoria.png")
    

# 4. Variación de tags entre dos años
def plot_variacion_tags(tags_variacion):
    tags_variacion['variacion'] = tags_variacion[2018] - tags_variacion[2017]
    tags_emergentes = tags_variacion.sort_values(by='variacion', ascending=False).head(10)
    tags_declive = tags_variacion.sort_values(by='variacion', ascending=True).head(10)

    fig, axes = plt.subplots(1, 2, figsize=(16,6))

    sns.barplot(x=tags_emergentes['variacion'], y=tags_emergentes.index, ax=axes[0], palette="Greens_r")
    axes[0].set_title("Tags emergentes (variación positiva)")

    sns.barplot(x=tags_declive['variacion'], y=tags_declive.index, ax=axes[1], palette="Reds")
    axes[1].set_title("Tags en declive (variación negativa)")

    plt.tight_layout()
    plt.savefig("graficas/variacion_tags.png")
    

# 5. Histogramas
def plot_histogramas(df):
    df['views'].plot.hist(title="Histograma de Views")
    plt.savefig("graficas/h_views.png")
    

    df['likes'].plot.hist(title="Histograma de Likes")
    plt.savefig("graficas/h_likes.png")
    

    df['comment_count'].plot.hist(title="Histograma de Comment Count")
    plt.savefig("graficas/h_comment_count.png")
    

# 6. Boxplots
def plot_boxplots(df):
    sns.boxplot(x=df['views'])
    plt.title('Boxplot de Views')
    plt.savefig("graficas/box_vistas.png")
    

    sns.boxplot(x=df['likes'])
    plt.title('Boxplot de Likes')
    plt.savefig("graficas/box_likes.png")
    

    sns.boxplot(x=df['comment_count'])
    plt.title('Boxplot de Comment Count')
    plt.savefig("graficas/box_comentarios.png")
    

# 7. Scatterplot con boxplots marginales
def plot_scatter_views_likes(df):
    g = sns.jointplot(
        data=df,
        x="views",
        y="likes",
        kind="scatter",
        marginal_kws=dict(bins=50, fill=True)
    )
    plt.suptitle("Boxplot bivariado: Views vs Likes", y=1.02)
    g.savefig("graficas/box_vistas_vs_likes.png")
    

# 8. Heatmap de correlación entre métricas
def plot_heatmap_metricas(df):
    corr = df[['views','likes','dislikes','comment_count']].corr()
    plt.figure(figsize=(8,6))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Matriz de correlación entre métricas')
    plt.savefig("graficas/hc_metricas.png")
    

# 9. Heatmap de correlación entre horario y tasa de actividad
def plot_heatmap_horario_tasa(df):
    corr = df[['hour','tasa_actividad']].corr()
    plt.figure(figsize=(8,6))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Matriz de correlación entre horario y tasa de actividad')
    plt.savefig("graficas/hc_horario_tasa.png")
    

# 10. Evolución de views por fecha
def plot_views_por_fecha(df):
    # Convertir publish_time a datetime si no lo es
    df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
    # Extraer solo la fecha
    df['fecha'] = df['publish_time'].dt.date
    views_por_fecha = df.groupby('fecha')['views'].mean().reset_index()

    plt.figure(figsize=(12,6))
    sns.lineplot(x='fecha', y='views', data=views_por_fecha, marker='o')
    plt.title('Promedio de Views por Fecha')
    plt.xlabel('Fecha de publicación')
    plt.ylabel('Promedio de Views')
    plt.xticks(rotation=45)
    plt.savefig("graficas/evolucion_vistas_fecha.png")
    plt.show()


# 11. Evolución de views por categoría
def plot_views_por_categoria(df):
    # Convertir publish_time a datetime si no lo es
    df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
    # Extraer solo la fecha
    df['fecha'] = df['publish_time'].dt.date
    views_categoria = (
        df.groupby(['fecha','category_id'])['views']
        .mean()
        .reset_index()
    )

    plt.figure(figsize=(12,6))
    sns.lineplot(
        data=views_categoria,
        x='fecha',
        y='views',
        hue='category_id',
        marker='o'
    )
    plt.title("Evolución de vistas por categoría")
    plt.xlabel("Fecha de publicación")
    plt.ylabel("Promedio de vistas")
    plt.xticks(rotation=45)
    plt.legend(title="Categoría")
    plt.savefig("graficas/evolucion_vistas_categoria.png")
    plt.show()



if __name__ == "__main__":
    import pandas as pd
    df = pd.read_csv("data/processed/MXvideos_metrics.csv", encoding="utf-8")

    plot_metricas_por_categoria(df)
    plot_horarios_optimos(df)
    plot_tasa_actividad_categoria(df)
    plot_histogramas(df)
    plot_boxplots(df)
    plot_scatter_views_likes(df)
    plot_heatmap_metricas(df)
    plot_heatmap_horario_tasa(df)
    plot_views_por_fecha(df)
    plot_views_por_categoria(df)
