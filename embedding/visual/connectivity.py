import numpy as np
import umap
import umap.plot
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from sklearn.preprocessing import StandardScaler

csv_file = 'new_embeddings.csv'
embeddings_df = pd.read_csv(csv_file, header=0)
embeddings = embeddings_df.to_numpy(dtype=np.float32)

mapper = umap.UMAP().fit(embeddings)
umap.plot.connectivity(mapper, show_points=True, edge_bundling='hammer')

# Using standard Matplotlib to plot instead of umap.plot for better compatibility
plt.scatter(
    mapper.embedding_[:, 0],
    mapper.embedding_[:, 1],
    s=5  # Adjust the size of the points if necessary
)
plt.title("UMAP projection")
plt.savefig('connectivity.pdf', format='pdf')
plt.show()
