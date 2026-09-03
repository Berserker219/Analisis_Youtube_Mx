import matplotlib.pyplot as plt
import seaborn as sns

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
    plt.show()

# 2. Horarios óptimos de publicación
def plot_horarios_optimos(df):
    horarios_optimos = df.groupby('hour')[['tasa_actividad']].mean().reset_index()
    plt.figure(figsize=(10,6))
    plt.bar(horarios_optimos['hour'], horarios_optimos['tasa_actividad'])
    plt.title('Promedio de Tasa de Actividad por Hora')
    plt.xlabel('Hora')
    plt.ylabel('Promedio de Tasa de Actividad')
    plt.xticks(range(0,24))
    plt.show()

# 3. Promedio de tasa de actividad por categoría
def plot_tasa_actividad_categoria(df):
    plt.figure(figsize=(10,6))
    sns.barplot(x='category_id', y='tasa_actividad', data=df)
    plt.title("Promedio de Tasa de Actividad por Categoría")
    plt.ylabel("Promedio de Tasa de Actividad")
    plt.xlabel("Categoría")
    plt.show()

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
    plt.show()

# 5. Histogramas
def plot_histogramas(df):
    df['views'].plot.hist(title="Histograma de Views")
    plt.show()
    df['likes'].plot.hist(title="Histograma de Likes")
    plt.show()
    df['comment_count'].plot.hist(title="Histograma de Comment Count")
    plt.show()

# 6. Boxplots
def plot_boxplots(df):
    sns.boxplot(x=df['views'])
    plt.title('Boxplot de Views')
    plt.show()

    sns.boxplot(x=df['likes'])
    plt.title('Boxplot de Likes')
    plt.show()

    sns.boxplot(x=df['comment_count'])
    plt.title('Boxplot de Comment Count')
    plt.show()

    sns.boxplot(data=df[['views','likes']])
    plt.title('Boxplot comparativo de Views y Likes')
    plt.show()

# 7. Scatterplot con boxplots marginales
def plot_scatter_views_likes(df):
    sns.jointplot(
        data=df,
        x="views",
        y="likes",
        kind="scatter",
        marginal_kws=dict(bins=50, fill=True)
    )
    plt.suptitle("Boxplot bivariado: Views vs Likes", y=1.02)
    plt.show()

# 8. Heatmap de correlación entre métricas
def plot_heatmap_metricas(df):
    corr = df[['views','likes','dislikes','comment_count']].corr()
    plt.figure(figsize=(8,6))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Matriz de correlación entre métricas')
    plt.show()

# 9. Heatmap de correlación entre horario y tasa de actividad
def plot_heatmap_horario_tasa(df):
    corr = df[['hour','tasa_actividad']].corr()
    plt.figure(figsize=(8,6))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Matriz de correlación entre horario y tasa de actividad')
    plt.show()

# 10. Evolución de views por fecha
def plot_views_por_fecha(df):
    views_por_fecha = df.groupby('publish_time')['views'].mean().reset_index()
    plt.figure(figsize=(12,6))
    sns.lineplot(x='publish_time', y='views', data=views_por_fecha, marker='o')
    plt.title('Promedio de Views por Fecha')
    plt.xlabel('Fecha de publicación')
    plt.ylabel('Promedio de Views')
    plt.xticks(rotation=45)
    plt.show()

# 11. Evolución de views por categoría
def plot_views_por_categoria(df):
    views_categoria = (
        df.groupby(['publish_time','category_id'])['views']
        .mean()
        .reset_index()
    )
    plt.figure(figsize=(12,6))
    sns.lineplot(
        data=views_categoria,
        x='publish_time',
        y='views',
        hue='category_id',
        marker='o'
    )
    plt.title("Evolución de vistas por categoría")
    plt.xlabel("Fecha de publicación")
    plt.ylabel("Promedio de vistas")
    plt.xticks(rotation=45)
    plt.legend(title="Categoría")
    plt.show()
