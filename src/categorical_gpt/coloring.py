from . import make_mds_embedding

from skimage import color
import numpy as np
from scipy.spatial import ConvexHull
from scipy.spatial.distance import cdist
import math

from .embedding import pairwise_distance, mds


# Normalize with the same scaling factor in all directions
def normalize_point(points):
    points_min_vector = np.min(points)
    points_max_vector = np.max(points)
    points_normalized = (points - points_min_vector) / (points_max_vector - points_min_vector)
    return points_normalized


# Identify most distant points
# https://stackoverflow.com/questions/31667070/max-distance-between-2-points-in-a-data-set-and-identifying-the-points
def bestpair(points):
    hull = ConvexHull(points)
    hullpoints = points[hull.vertices, :]
    # Naive way of finding the best pair in O(H^2) time if H is number of points on
    # hull
    hdist = cdist(hullpoints, hullpoints, metric='euclidean')
    # Get the farthest apart points
    bestpair = np.unravel_index(hdist.argmax(), hdist.shape)
    return hullpoints[bestpair[0]], hullpoints[bestpair[1]]


# Puts maximum distance on diagonal
def rotate_points(points):
    p1, p2 = bestpair(points)
    # Get the angle between the points and the diagonal
    vec = p2 - p1
    vec_norm = vec / np.linalg.norm(vec)
    # Rotate around vector perpendicular to the other two
    direction = np.array([1, 1, 1]) / np.sqrt(3)
    n = np.cross(vec_norm, direction)
    n = n / np.linalg.norm(n)
    rot_angle = math.acos(np.dot(vec_norm, direction))
    cosA = math.cos(rot_angle)
    sinA = math.sin(rot_angle)
    rot_mat = np.array(
        [[n[0] ** 2 * (1 - cosA) + cosA, n[0] * n[1] * (1 - cosA) - n[2] * sinA,
          n[0] * n[2] * (1 - cosA) + n[1] * sinA],
         [n[1] * n[0] * (1 - cosA) + n[2] * sinA, n[1] ** 2 * (1 - cosA) + cosA,
          n[1] * n[2] * (1 - cosA) - n[0] * sinA],
         [n[2] * n[0] * (1 - cosA) - n[1] * sinA, n[2] * n[1] * (1 - cosA) + n[0] * sinA,
          n[2] ** 2 * (1 - cosA) + cosA]]
    )
    # Rotate points:
    points_rot = np.empty(points.shape)
    for i in range(len(points)):
        points_rot[i] = np.matmul(rot_mat, points[i])
    return points_rot


# Create mds image in L*a*b* space
def points2rgb(points):
    points = rotate_points(points)
    points = normalize_point(points)
    points[..., 0] = points[..., 0] * 100
    points[..., 1] = points[..., 1] * 100 - 50
    points[..., 2] = points[..., 2] * 100 - 50
    colored_points = color.lab2rgb(points, illuminant='A')
    return colored_points


def column2color(df, column):
    df_unique = df
    vals = df_unique[column].values.tolist()
    dis = pairwise_distance([vals])
    emb = mds(dis)[0]
    cols = points2rgb(emb)
    df_color = df[column].map(lambda el: cols[vals.index(el)])
    return df_color


def color_coding(cgpt, embedding_distance_metric='euclidean', decimals=12):
    embedding, _, distance_matrix = make_mds_embedding(cgpt, distance_metric=embedding_distance_metric, n_dim=3)
    colors = points2rgb(np.array(list(embedding.values())))
    result = {}
    for i, option in enumerate(list(embedding.keys())):
        result[option] = list(np.round(colors[i], decimals))
    return result
