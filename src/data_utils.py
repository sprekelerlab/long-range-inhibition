# Helper functions for loading data
import numpy as np
from scipy.io import loadmat
import os


def load_data(file, phase = 'rec', data_dir = '../AFC'):
    """ phase: hab / acq / rec """
    assert phase in ('hab', 'acq', 'rec')
    d = loadmat(f"{data_dir}/{file}")
    X = d[f'DeltaFF_{phase}']
    if  "AFC" in data_dir:
        y = d[f'CSp_tr_{phase}'].flatten()
    else: 
        if phase == "acq": # Take care of shock trials
            y = np.ones((45, )) * -1 # Init 
            y[np.where(d['CS2_tr_acq']==1)[0]] = 1
            y[np.where(d['CS2_tr_acq']==0)[0]] = 0
            # Delete remaining -1 (shock) entries
            y = y[y>=0]
        else:
            y = np.zeros((30, )) # Init 
            y[np.where(d[f'CS2_tr_{phase}']==1)[0]] = 1
    return X, y


def get_all_boutons(phase, data_dir = "../../data/AFC/", num_pcs = 200, subsample = False):
    """
    Group data from all mice and reduce its dimensionality

    Arguments: 
        phase: 'hab'/'acq'/'rec'
        data_dir: directory with the data for individual mice
        subsample: randomly select # of boutons equal to # from pseudo-experiment?

    Returns:
        Xs: all calcium data, of size (num_trials, num_frames, num_rois)
        Xred: dimensionality reduced data, (num_trials, num_frames, num_pcs)
        pca: fitted PCA object
        ys: binary trial identity, (num_trials, )
    """
    from sklearn.decomposition import PCA
    assert phase in ('hab', 'acq', 'rec')
    assert subsample in (True, False)
    files = os.listdir(data_dir)
    Xs = []
    ys = []
    alternate_idx = np.array([[i, 15+i] for i in range(15)]).flatten()

    for m, file in enumerate(files):
        X, y = load_data(file, phase,  data_dir)
        # Sort by label, then mix them
        idx_sort = np.argsort(y) 
        y = y[idx_sort] #[0,0,..., 0, 1,1, ..., 1]
        X = X[idx_sort]
        y = y[alternate_idx]
        X = X[alternate_idx]
        if m == 0:   # Start. Now y labels are all the same
            Xs = X
            ys = y 
        else:
            Xs = np.concatenate((Xs, X), -1)
            
    
    num_trials, num_frames, num_rois = Xs.shape
    if subsample:
        n_select = 535
        idx_select = np.random.choice(np.arange(num_rois), n_select, replace=False)
        Xs = Xs[:,:,idx_select]
        num_rois = n_select
    # Fit PCA
    Xs /= np.linalg.norm(Xs, axis=(0,1))
    pca = PCA(num_pcs)
    Xred = pca.fit_transform(Xs.reshape((-1, num_rois))).reshape((num_trials, num_frames, num_pcs))
    
    return Xs, Xred, pca, ys


def get_per_mouse_boutons(phase, data_dir):
    """
    Load the boutons from all mice 

    Arguments: 
        phase: 'hab', 'ac', 'rec'
        data_dir: directory from where to load the files

    Returns:
        Xs: dF/F of size (trials, time frames, boutons)
        ys: stimulus (1=CS+, 0=CS-) of size (trials, )
    """
    assert phase in ('hab', 'acq', 'rec')
    Xs = {}
    ys = {}
    files = os.listdir(data_dir) # individual mice 
    files.sort()
    for m, file in enumerate(files):
        mouse_id = file.split(".")[0]
        Xs[mouse_id], ys[mouse_id] = load_data(file, phase, data_dir)
    return Xs, ys



