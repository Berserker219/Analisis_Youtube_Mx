import matplotlib.pyplot as plt
import seaborn as sns

# Gráfico de distribución de vistas
def plot_distribucion_vistas(df):
    plt.figure(figsize=(8,5))
    sns.histplot(df['views'], bins=50, log_scale=True)
    plt.title("Distribución de vistas")
    plt.xlabel("Vistas")
    plt.ylabel("Frecuencia")
    plt.show()

# Gráfico de videos por franja horaria
def plot_videos_por_franja(df):
    plt.figure(figsize=(6,4))
    sns.countplot(x="franja_horaria", data=df, palette="Set2")
    plt.title("Cantidad de videos por franja horaria")
    plt.xlabel("Franja horaria")
    plt.ylabel("Número de videos")
    plt.show()

# Gráfico de promedio de vistas por franja horaria
def plot_vistas_por_franja(df):
    promedio = df.groupby("franja_horaria")["views"].mean().reset_index()
    plt.figure(figsize=(6,4))
    sns.barplot(x="franja_horaria", y="views", data=promedio, palette="Set1")
    plt.title("Promedio de vistas por franja horaria")
    plt.xlabel("Franja horaria")
    plt.ylabel("Promedio de vistas")
    plt.show()

# Gráfico de correlación entre métricas
def plot_correlacion_metricas(df):
    plt.figure(figsize=(8,6))
    corr = df[['views','likes','dislikes','comment_count']].corr()
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlación entre métricas")
    plt.show()
