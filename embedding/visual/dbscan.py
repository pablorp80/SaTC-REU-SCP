import numpy as np
import umap
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import DBSCAN

csv_file = 'embeddings.csv'
embeddings_df = pd.read_csv(csv_file, header=0)
embeddings = embeddings_df.to_numpy(dtype=np.float32)

nc_for_vis = 2
rs = 42
vis_embeddings = umap.UMAP(n_components=nc_for_vis, random_state=rs).fit_transform(embeddings)

eps = 0.5
min_samples = 5
metric = 'euclidean'
dbscan = DBSCAN(eps=eps, min_samples=min_samples, metric=metric)
clusters = dbscan.fit_predict(vis_embeddings)

plt.figure(figsize=(10, 8))
scatter = plt.scatter(vis_embeddings[:, 0], vis_embeddings[:, 1], c=clusters, alpha=0.4, cmap='tab20', s=10)

n_clusters = len(set(clusters)) - (1 if -1 in clusters else 0)
plt.colorbar(scatter, ticks=range(n_clusters))

plt.title('imagebind embeddings DBSCAN clustering')
plt.xlabel('Component 1')
plt.ylabel('Component 2')

plt.tight_layout()
plt.savefig(fname='dbscan_clusters.pdf', format='pdf')
plt.show()
