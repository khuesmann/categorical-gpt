import numpy as np


def mds(d, dimensions=3):
    (n, n) = d.shape
    E = (-0.5 * d ** 2)

    Er = np.mat(np.mean(E, 1))
    Es = np.mat(np.mean(E, 0))

    F = np.array(E - np.transpose(Er) - Es + np.mean(E))

    [U, S, V] = np.linalg.svd(F)

    Y = U * np.sqrt(S)

    return [Y[:, 0:dimensions], S]


def pairwise_distance(feature_tensor, distance='euclidean', normalization='minmax'):
    dists = []
    for f in feature_tensor:
        f = np.array(f)
        if distance == 'euclidean':
            d = np.sqrt(np.sum((f[:, np.newaxis, :] - f[np.newaxis, :, :]) ** 2, axis=-1))
            dists.append(d)
        elif distance == 'cosine':
            norm_f = f / np.linalg.norm(f, axis=-1, keepdims=True)
            cosine_similarity = np.dot(norm_f, norm_f.T)
            cosine_distance = 1 - cosine_similarity
            dists.append(cosine_distance)
        elif distance == 'pearson':
            dists.append(np.corrcoef(f))

    dists = np.array(dists)

    if normalization == 'minmax':
        mini = np.min(dists, axis=(1, 2), keepdims=True)
        maxi = np.max(dists, axis=(1, 2), keepdims=True)
        dists = (dists - mini) / (maxi - mini)
    elif normalization == 'meanstd':
        mean = np.mean(dists, axis=(1, 2), keepdims=True)
        std = np.std(dists, axis=(1, 2), keepdims=True)
        dists = (dists - mean) / std
    elif 'custom' in normalization:
        mini, maxi = normalization.split(':')[1].split(',')
        mini = float(mini)
        maxi = float(maxi)
        dists = (dists - mini) / (maxi - mini)

    dists = np.sum(dists, axis=0)

    return dists


def make_mds_embedding(cgpt, distance_metric='euclidean', n_dim=3, tolist=False):
    distance_matrix = pairwise_distance([list(cgpt.feature_vectors.values())], distance=distance_metric)
    emb = mds(distance_matrix, dimensions=n_dim)
    if tolist:
        emb[0] = emb[0].tolist()
    embedding = dict(zip(list(cgpt.feature_vectors.keys()), emb[0]))
    embedding_eigens = emb[1]
    return embedding, embedding_eigens, distance_matrix
