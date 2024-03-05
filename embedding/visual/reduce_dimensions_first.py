import numpy as np
import umap
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

csv_file = 'new_embeddings.csv'
embeddings_df = pd.read_csv(csv_file, header=0)
embeddings = embeddings_df.to_numpy(dtype=np.float32)

reduced_dim = 128
pca = PCA(n_components=reduced_dim)
embeddings_reduced = pca.fit_transform(embeddings)

k = 20
rs = 3
kmeans_reduced = KMeans(n_clusters=k, init='k-means++', random_state=rs, max_iter=750)
clusters_reduced = kmeans_reduced.fit_predict(embeddings_reduced)

initial_centroids = np.array([embeddings[clusters_reduced == i].mean(axis=0) for i in range(k)])
kmeans = KMeans(n_clusters=k, init='k-means++', n_init=1, max_iter=750)
clusters = kmeans.fit_predict(embeddings)

nc = 2
umap_model = umap.UMAP(n_components=nc, random_state=42)
embeddings_2d = umap_model.fit_transform(embeddings)

silhouette_avg = silhouette_score(embeddings, clusters)
davies_bouldin_avg = davies_bouldin_score(embeddings, clusters)
calinski_harabasz_avg = calinski_harabasz_score(embeddings, clusters)

print(silhouette_avg)
print(davies_bouldin_avg)
print(calinski_harabasz_avg)

plt.figure(figsize=(10, 8))
for cluster in range(k):
    cluster_points = embeddings_2d[clusters == cluster]
    plt.scatter(cluster_points[:, 0], cluster_points[:, 1], alpha=0.4, s=10, label=f'Cluster {cluster}')

plt.title('K-Means Clusters with Preprocessing')
plt.xlabel('Component 1')
plt.ylabel('Component 2')
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.tight_layout()
plt.savefig(fname="k_means_with_preprocessing.pdf", format='pdf')
