import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar el dataset
df = pd.read_excel('E Commerce Dataset.xlsx')

# Eliminar características no numéricas
df_numeric = df.select_dtypes(include=['int64', 'float64'])

# Normalizar los datos
scaler = StandardScaler()
df_normalized = scaler.fit_transform(df_numeric)

# Aplicar el algoritmo KMeans
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(df_normalized)

# Agregar las etiquetas de los clusters al dataframe original
df['Cluster'] = kmeans.labels_

# Analizar los clusters
for cluster in df['Cluster'].unique():
    print(f"Cluster {cluster}")
    print(df[df['Cluster'] == cluster].describe())
    print("\n")

# Visualizar los clusters
sns.pairplot(df, hue='Cluster')
plt.show()