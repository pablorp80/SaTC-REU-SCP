import numpy as np
import umap
import matplotlib.pyplot as plt
import pandas as pd

csv_file = 'embeddings.csv'
embeddings_df = pd.read_csv(csv_file, skiprows=1)
embeddings = embeddings_df.to_numpy(dtype=np.float32)

nc = 2
nn = 70
md = 0.4
rs = 42
umap_model = umap.UMAP(n_components=nc, n_neighbors=nn, min_dist=md, random_state=rs)
embeddings_2d = umap_model.fit_transform(embeddings)

plt.figure(figsize=(10, 8))
plt.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1], alpha=0.4)
plt.title('imagebind craigslist embeddings')
plt.xlabel('Component 1')
plt.ylabel('Component 2')
plt.show()
