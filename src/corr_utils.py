import numpy as np

def compute_response_integral(X, stim_frames):
    """
    Compute the integrated/summed response over all stimulus frames

    Arguments:
        X (array): dF/F of size (trials, time frames, boutons)
        stim_frames (array): time frames w/ stimulus
    Returns:
        Xint (array): summed dF/F during stim frames, size (trials, boutons)
    """
    assert len(stim_frames) > 0
    assert stim_frames[0] > 0
    assert stim_frames[-1] < X.shape[1]
    return X[:,stim_frames].sum(1)


def compute_noise_corrs(X1int, X2int = None):
    """
    Compute the correlations between two responses

    Arguments:
        X1int: dF/F integral of size (trials, num_pairs_1)
        X2int: dF/F integral of size (trials, num_pairs_2)

    Returns:
        C: noise corrs of size (num_pairs_1 * num_pairs_2)
    """
    if X2int is None:
        X2int = X1int
    assert X1int.shape[0] == X2int.shape[0]
    n1, n2 = X1int.shape[1], X2int.shape[1]
    # Subtract mean
    C = np.zeros((n1, n2))
    for i1 in np.arange(n1):
        for i2 in np.arange(i1, n2): # Only need upper diag.
            C[i1, i2] = np.corrcoef(X1int[:,i1], X2int[:,i2])[0,1]
    # Select unique pairs by extracting upper diagonal of C
    if X1int.shape == X2int.shape and np.allclose(X1int, X2int):
        # Same pairs, throw away self correlations on diagonal
        k = 1
    else:
        k = 0
        # Keep correlations on diagonal
    rows, cols = np.triu_indices(n1, k, n2)
    return C[rows,cols], C
