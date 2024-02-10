import numpy as np
import umap
import matplotlib.pyplot as plt
import pandas as pd

# Manually create a simple dataset
csv_file = 'embeddings.csv'
embeddings_df = pd.read_csv(csv_file)

umap_model = umap.UMAP(n_components=2, n_neighbors=15, min_dist=0.1, random_state=42)
embeddings_2d = umap_model.fit_transform(embeddings_df)

# Plot the result
plt.figure(figsize=(10, 8))
plt.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1], alpha=0.5)
plt.title('2D Visualization using UMAP')
plt.xlabel('Component 1')
plt.ylabel('Component 2')
plt.show()
