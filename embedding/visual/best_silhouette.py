# this script implements the Silhoutte score maximizer
# experiemnt described in section 5 of https://www.mit.edu/~vgarg/neurips2018sup.pdf

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

def main():
    csv_file = 'embeddings.csv'
    embeddings_df = pd.read_csv(csv_file, header=0)
    embeddings = embeddings_df.to_numpy(dtype=np.float32)

    best_silhouette = -1
    best_k = None
    best_random_state = None

    for random_state in range(10):
        for k in range(2, 11):
            kmeans = KMeans(n_clusters=k, random_state=random_state)
            clusters = kmeans.fit_predict(embeddings)
            silhouette_avg = silhouette_score(embeddings, clusters)
            print(f'Random state: {random_state}, k: {k}, Silhouette Score: {silhouette_avg}')

            if silhouette_avg > best_silhouette:
                best_silhouette = silhouette_avg
                best_k = k
                best_random_state = random_state

    print(f'\nBest Silhouette Score: {best_silhouette} for k = {best_k} and random state = {best_random_state}')

if __name__ == "__main__":
    main()
