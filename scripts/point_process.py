# Point process analysis for a signal. Values equal to 1 when the original value 
# is higher than the threshold (1*SD)
def point_process(signal):

    import numpy as np

    pp_signal = np.zeros(signal.shape[0])
    th = np.std(signal)

    pp_signal[signal > th] = 1

    return pp_signal


# Conditional Rate Map. Given an fMRI, extract timeseries, calculate Point Process
# and then the Rate Map for each voxel given a seed   
def cond_rm(in_file, seed_location):

    import numpy as np
    import os
    import nibabel as nb

    # Treat fMRI image
    img = nb.load(in_file)
    #print img.shape
    data = img.get_data()

    (n_x, n_y, n_z, n_t) = data.shape

    K = np.zeros((n_x, n_y, n_z))
    # Extract seed and pp
    seed_data = data[seed_location[0], seed_location[1], seed_location[2],:]
    pp_seed_data = point_process(seed_data)
    r = np.count_nonzero(pp_seed_data)
    # Calculate each PP signal
    for i_ in range(n_x):
        for j_ in range(n_y):
            for k_ in range(n_z):

                target_data = data[i_,j_,k_,:]
                pp_target_data = point_process(target_data)

                # LOGIC AND (target/seed) and count(signal == 1), that will give you the X/r parameter [0,1]
                K[i_,j_,k_] = np.count_nonzero(np.logical_and(pp_seed_data,pp_target_data))/float(r)

    # Reconstruct the 3D volume
    cond_rm_file = os.path.join(os.getcwd(), 'cond_rm.nii.gz')
    img.to_filename(cond_rm_file)

    return cond_rm_file

