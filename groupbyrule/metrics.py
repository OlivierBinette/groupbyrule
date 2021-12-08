import numpy as np
from scipy.special import comb

def precision(pred_labels: np.ndarray, true_labels: np.ndarray) -> tuple:
    true_cluster_sizes = np.unique((pred_labels, true_labels), axis=1, return_counts=True)[1]    
    pred_cluster_sizes = np.unique(pred_labels, return_counts=True)[1]

    TP = np.sum(comb(true_cluster_sizes, 2))
    P = np.sum(comb(pred_cluster_sizes, 2))

    return TP/P

def recall(pred_labels: np.ndarray, true_labels: np.ndarray) -> tuple:
    return precision(true_labels, pred_labels)
