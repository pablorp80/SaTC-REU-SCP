import numpy as np
import umap
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

csv_file = 'new_embeddings.csv'
embeddings_df = pd.read_csv(csv_file, header=0)
embeddings = embeddings_df.to_numpy(dtype=np.float32)

k = 20
rs = 42
nc = 32
reduced_embeddings = umap.UMAP(n_components=nc, random_state=rs).fit_transform(embeddings)

reduced_kmeans = KMeans(n_clusters=k, random_state=42).fit(reduced_embeddings)
reduced_clusters = reduced_kmeans.labels_

silhouette_avg_reduced = silhouette_score(reduced_embeddings, reduced_clusters)
print(f'Reduced Silhouette Score: {silhouette_avg_reduced}')

calinski_harabasz_avg_reduced = calinski_harabasz_score(reduced_embeddings, reduced_clusters)
print(f'Reduced Calinski-Harabasz Index: {calinski_harabasz_avg_reduced}')

davies_bouldin_avg_reduced = davies_bouldin_score(reduced_embeddings, reduced_clusters)
print(f'Reduced Davies-Bouldin Index: {davies_bouldin_avg_reduced}')

nc_for_vis = 2
vis_embeddings = umap.UMAP(n_components=nc_for_vis, random_state=rs).fit_transform(embeddings)

plt.figure(figsize=(10, 8))
plt.scatter(vis_embeddings[:, 0], vis_embeddings[:, 1], c=reduced_clusters, alpha=0.4, cmap='tab20', s=10)
plt.colorbar(ticks=range(k))
plt.clim(-0.5, k - 0.5)
plt.title('UMAP projection of Craigslist Embeddings, colored by clusters found in 128D space')
plt.xlabel('Component 1')
plt.ylabel('Component 2')
plt.savefig(fname='32reduced.pdf', format='pdf')
plt.show()
