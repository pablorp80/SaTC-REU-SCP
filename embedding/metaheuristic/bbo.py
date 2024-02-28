import numpy as np
import pandas as pd
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from mealpy import FloatVar, BBO


csv_file = '../new_embeddings.csv'  # Make sure this points to the correct file path
embeddings_df = pd.read_csv(csv_file, header=0)
X = embeddings_df.to_numpy(dtype=np.float32)
X = StandardScaler().fit_transform(X)

num_clusters = 10

data_min, data_max = X.min(axis=0), X.max(axis=0)
num_features = X.shape[1]
float_bounds = FloatVar(lb=data_min, ub=data_max, name="centroids")

bounds = []
for _ in range(num_clusters):
    cluster_bounds = [FloatVar(lb=data_min[i], ub=data_max[i], name=f"dim_{i}") for i in range(num_features)]
    bounds.extend(cluster_bounds)

def clustering_objective(solution):
    centroids = solution.reshape(num_clusters, -1)
    labels = np.argmin(np.linalg.norm(X[:, None] - centroids, axis=2), axis=1)
    score = silhouette_score(X, labels)
    return -score

problem = {
    "obj_func": clustering_objective,
    "bounds": bounds,
    "minmax": "min",
    "verbose": True,
}

model = BBO.DevBBO(epoch=1000, pop_size=71, p_m=0.01, n_elites=2)
g_best = model.solve(problem)
print(f"Solution: {g_best.solution}, Fitness: {g_best.target.fitness}")
print(f"Solution: {model.g_best.solution}, Fitness: {model.g_best.target.fitness}")

optimized_centroids = g_best.solution.reshape(num_clusters, -1)
centroids_df = pd.DataFrame(optimized_centroids)
centroids_df.to_csv('optimized_centroids.csv', index=False)
