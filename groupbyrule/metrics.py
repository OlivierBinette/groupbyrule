import numpy as np
from scipy.special import comb
import math
import sklearn.metrics as metrics

# TODO: add graph (link-based) metrics


def precision(pred_labels, true_labels) -> float:
    TP_cluster_sizes = np.unique(
        (pred_labels, true_labels), axis=1, return_counts=True)[1]
    P_cluster_sizes = np.unique(pred_labels, return_counts=True)[1]

    TP = np.sum(comb(TP_cluster_sizes, 2))
    P = np.sum(comb(P_cluster_sizes, 2))

    return TP / P


def recall(pred_labels, true_labels) -> float:
    return precision(true_labels, pred_labels)


def precision_recall(pred_labels, true_labels) -> tuple:
    return (precision(pred_labels, true_labels), recall(pred_labels, true_labels))


def fscore(pred_labels, true_labels, beta=1.0) -> float:
    P = precision(pred_labels, true_labels)
    R = recall(pred_labels, true_labels)

    return (1 + beta**2) * P * R / (beta**2 * P + R)


# TODO: test validity
# Note: this should be much more efficient than sklearn's pair_confusion_matrix
def pairs_ct(pred_labels, true_labels) -> float:
    TP_cluster_sizes = np.unique(
        (pred_labels, true_labels), axis=1, return_counts=True)[1]
    P_cluster_sizes = np.unique(pred_labels, return_counts=True)[1]
    T_cluster_sizes = np.unique(true_labels, return_counts=True)[1]

    TP = np.sum(comb(TP_cluster_sizes, 2))
    P = np.sum(comb(P_cluster_sizes, 2))
    T = np.sum(comb(T_cluster_sizes, 2))
    FP = P - TP
    FN = T - TP
    TN = comb(len(pred_labels), 2) - P - FN

    return ((TP, FP), (FN, TN))


def fowlkes_mallows(pred_labels, true_labels) -> float:
    P = precision(pred_labels, true_labels)
    R = recall(pred_labels, true_labels)

    return math.sqrt(P*R)


def homogeneity(pred_labels, true_labels) -> float:
    return metrics.cluster.homogeneity_score(true_labels, pred_labels)


def completeness(pred_labels, true_labels) -> float:
    return metrics.cluster.completeness_score(true_labels, pred_labels)


def v_measure(pred_labels, true_labels, beta=1.0) -> float:
    H = homogeneity(pred_labels, true_labels)
    C = completeness(pred_labels, true_labels)
    return (1 + beta) * H * C / (beta * H + C)
