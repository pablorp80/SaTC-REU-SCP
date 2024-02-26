import numpy as np
import pandas as pd
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans

csv_file = 'new_embeddings.csv'
embeddings_df = pd.read_csv(csv_file, header=0)
embeddings = embeddings_df.to_numpy(dtype=np.float32)

max_k = -9999
max_sil = -9999

k_values = range(2, 50)
for k in k_values:
    kmeans = KMeans(n_clusters=k, random_state=42)
    clusters = kmeans.fit_predict(embeddings)
    silhouette_avg = silhouette_score(embeddings, clusters)
    print(f'k = {k}, Silhouette Score: {silhouette_avg}')
    if silhouette_avg > max_sil:
        max_sil = silhouette_avg
        max_k = k

print('max silhoutte ' + str(max_sil) + ' with k=' + str(max_k))
