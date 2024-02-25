import numpy as np
import umap
import matplotlib.pyplot as plt
import pandas as pd

csv_file = 'embeddings.csv'
embeddings_df = pd.read_csv(csv_file, header=0)
embeddings = embeddings_df.to_numpy(dtype=np.float32)

nc = 2
nn = 15
md = 0.1
rs = 42
s = 1.5
umap_model = umap.UMAP(n_components=nc, n_neighbors=nn, min_dist=md, random_state=rs, spread=s)
embeddings_2d = umap_model.fit_transform(embeddings)

from sklearn.cluster import KMeans
k = 10
kmeans = KMeans(n_clusters=k, random_state=42)
clusters = kmeans.fit_predict(embeddings)

#from sklearn.cluster import BisectingKMeans
#k = 10
#bkmeans = BisectingKMeans(n_clusters=k, bisecting_strategy="biggest_inertia")
#clusters = bkmeans.fit_predict(embeddings)

#from sklearn.cluster import AgglomerativeClustering
#k = 10
#cluster_model = AgglomerativeClustering(n_clusters=k)
#clusters = cluster_model.fit_predict(embeddings)

#from sklearn.cluster import Birch
#k = 10
#birch = Birch(n_clusters=k, branching_factor=100, threshold=0.2)
#clusters = birch.fit_predict(embeddings)


plt.figure(figsize=(10, 8))
for cluster in range(k):
    cluster_points = embeddings_2d[clusters == cluster]
    plt.scatter(cluster_points[:, 0], cluster_points[:, 1], alpha=0.4, label=f'Cluster {cluster}')

plt.title('imagebind craigslist embeddings Birch clustering')
plt.xlabel('Component 1')
plt.ylabel('Component 2')
plt.legend()
plt.show()
