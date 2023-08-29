import numpy as np

from . import make_mds_embedding


def ordered_options(cgpt, ordering_method='mds', embedding_distance_metric='euclidean'):
    embedding, _, distance_matrix = make_mds_embedding(cgpt, distance_metric=embedding_distance_metric, n_dim=1)
    emb = np.array(list(embedding.values()))[:, 0]
    if 'tsp' in ordering_method:
        import networkx as nx
        G = nx.convert_matrix.from_numpy_array(distance_matrix)
        initial_i_sorted = np.argmax(np.unravel_index(np.argmax(distance_matrix), distance_matrix.shape)[1])
        if 'mds' in ordering_method:
            initial_i_sorted = np.argsort(emb, axis=0)[0]
        indices_sorted = nx.approximation.greedy_tsp(G, source=initial_i_sorted)[:-1]
    elif ordering_method == 'umap':
        import umap
        u = umap.UMAP(n_components=1, random_state=42).fit_transform(list(cgpt.feature_vectors.values()))
        indices_sorted = np.argsort(u[:, 0], axis=0)
    elif ordering_method == 'lexicographic':
        return sorted(cgpt.options)
    else:
        indices_sorted = np.argsort(emb, axis=0)

    options_sorted = []
    for i in indices_sorted:
        v = cgpt.options[i]
        options_sorted.append(v)

    return options_sorted
