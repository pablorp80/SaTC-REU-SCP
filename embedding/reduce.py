import numpy as np
import umap
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# load data
csv_file = 'file_name_here.csv'
embeddings_df = pd.read_csv(csv_file, header=0)
embeddings = embeddings_df.to_numpy(dtype=np.float32)

# reduce to 32D
n_components = 32
pca = PCA(n_components=n_components)
reduced_embeddings = pca.fit_transform(embeddings)

# k-means on reduced embeddings
k = 20
rs=3
reduced_kmeans = KMeans(n_clusters=k, random_state=rs).fit(reduced_embeddings)
reduced_clusters = reduced_kmeans.labels_

# print scores
silhouette_avg_reduced = silhouette_score(embeddings, reduced_clusters)
print(f'Reduced Silhouette Score: {silhouette_avg_reduced}')
calinski_harabasz_avg_reduced = calinski_harabasz_score(embeddings, reduced_clusters)
print(f'Reduced Calinski-Harabasz Index: {calinski_harabasz_avg_reduced}')
davies_bouldin_avg_reduced = davies_bouldin_score(embeddings, reduced_clusters)
print(f'Reduced Davies-Bouldin Index: {davies_bouldin_avg_reduced}')

# umap
nc_for_vis = 2
vis_embeddings = umap.UMAP(n_components=nc_for_vis, random_state=rs).fit_transform(embeddings)

# visual
plt.figure(figsize=(10, 8))
plt.scatter(vis_embeddings[:, 0], vis_embeddings[:, 1], c=reduced_clusters, alpha=0.4, cmap='tab20', s=10)
plt.colorbar(ticks=range(k))
plt.clim(-0.5, k - 0.5)
plt.savefig(fname='32reduced.pdf', format='pdf')
plt.show()
