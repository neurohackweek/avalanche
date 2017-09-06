def avalanche_detec(cluster_file):

    import numpy as np
    import nibabel as nb
    import os

    # Treat fMRI image
    img = nb.load(cluster_file)
    cluster_data = img.get_data()
    (n_x, n_y, n_z, n_t) = cluster_data.shape

    avalanche_id_total = np.zeros((n_x, n_y, n_z, n_t))
    avalanche_id_num = 1

    for t_ in range(n_t):

        if t_ == 0: #if first timestep, all are candidates
            time_slice = cluster_data[:,:,:,t_]
            time_slice_fut = cluster_data[:,:,:,t_+1]

            avalanche_id_now = avalanche_id_total[:,:,:,t_]
            avalanche_id_fut = avalanche_id_total[:,:,:,t_+1]

            for cluster in np.unique(cluster_data[:,:,:,t_])[1:]: #iterate over clusters
                # NEW AVALANCHE CASE
                if np.count_nonzero(time_slice_fut[(time_slice==cluster)]) >= 1 :
                    avalanche_id_now[(time_slice==cluster)] = avalanche_id_num

                    for value in np.unique(time_slice_fut[(time_slice==cluster)])[1:]:
                        avalanche_id_fut[(time_slice_fut==value)] = avalanche_id_num

                    avalanche_id_num = avalanche_id_num +1

                    avalanche_id_total[:,:,:,t_] = avalanche_id_now
                    avalanche_id_total[:,:,:,t_+1] = avalanche_id_fut


        elif t_ < (n_t-1):  #if not first timestep, check previous
            print t_
            #time_slice_past = cluster_data[:,:,:,t_-1]
            time_slice = cluster_data[:,:,:,t_]
            time_slice_fut = cluster_data[:,:,:,t_+1]

            avalanche_id_now = avalanche_id_total[:,:,:,t_]
            avalanche_id_fut = avalanche_id_total[:,:,:,t_+1]

            for cluster in np.unique(cluster_data[:,:,:,t_])[1:]:
                # PREVIOUS AVALANCHE CASE
                if np.count_nonzero(avalanche_id_now[(time_slice==cluster)]) != 0:
                    if np.count_nonzero(time_slice_fut[(time_slice==cluster)]) >= 1 :

                        this_avalanche = avalanche_id_now[(time_slice==cluster)][0]

                        for value in np.unique(time_slice_fut[(time_slice==cluster)])[1:]:
                            avalanche_id_fut[(time_slice_fut==value)] = this_avalanche

                        avalanche_id_total[:,:,:,t_+1] = avalanche_id_fut

                # NEW AVALANCHE CASE
                elif np.count_nonzero(avalanche_id_now[(time_slice==cluster)]) == 0: #and np.count_nonzero(time_slice_past[(time_slice==cluster)]) == 0:
                    if np.count_nonzero(time_slice_fut[(time_slice==cluster)]) >= 1 :

                        avalanche_id_now[(time_slice==cluster)] = avalanche_id_num

                        for value in np.unique(time_slice_fut[(time_slice==cluster)])[1:]:
                            avalanche_id_fut[(time_slice_fut==value)] = avalanche_id_num

                        avalanche_id_num = avalanche_id_num + 1

                        avalanche_id_total[:,:,:,t_] = avalanche_id_now
                        avalanche_id_total[:,:,:,t_+1] = avalanche_id_fut


    img_new = nb.Nifti1Image(avalanche_id_total, header=img.get_header(), affine=img.get_affine())
    # Reconstruct the 4D volume
    cond_rm_file = os.path.join(os.getcwd(), 'avalanche.nii.gz')
    img_new.to_filename(cond_rm_file)

    return avalanche_id_total
