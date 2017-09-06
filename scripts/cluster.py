# Detects clusters after Point Processing a Brain 
def cluster_detection(in_file):

    import numpy as np
    import os
    import nibabel as nb
    from CPAC.criticallity import point_process

    # Treat fMRI image
    img = nb.load(in_file)
    data = img.get_data()
    (n_x, n_y, n_z, n_t) = data.shape

    # Get the PP data
    pp_data = np.zeros((n_x, n_y, n_z, n_t))
    for i_ in range(n_x):
        for j_ in range(n_y):
            for k_ in range(n_z):
                voxel_data = data[i_,j_,k_,:]
                pp_data[i_,j_,k_,:] = point_process(voxel_data)

    cluster_graph_data_total = np.zeros((n_x, n_y, n_z, n_t))
    for t_ in range(n_t):
        time_slice = pp_data[:,:,:,t_]
        cluster_graph_data = np.zeros((n_x, n_y, n_z))
        cluster_number = 1

        for i_ in range(n_x):
            for j_ in range(n_y):
                for k_ in range(n_z):

                    if time_slice[i_,j_,k_] == 1: # is active, check if it has active neighboours
                        if time_slice[i_-1,j_,k_] or time_slice[i_+1,j_,k_] \
                        or time_slice[i_,j_-1,k_] or time_slice[i_,j_+1,k_] \
                        or time_slice[i_,j_,k_-1] or time_slice[i_,j_,k_+1]:

                            if cluster_graph_data[i_,j_,k_] == 0: # if is not in any previous cluster
                                this_cluster = (cluster_graph_data[i_-1,j_,k_] or cluster_graph_data[i_+1,j_,k_] \
                                or cluster_graph_data[i_,j_-1,k_] or cluster_graph_data[i_,j_+1,k_] \
                                or cluster_graph_data[i_,j_,k_-1] or cluster_graph_data[i_,j_,k_+1])

                                if this_cluster == 0: #no neighbours in any previous cluster neither
                                    this_cluster = cluster_number
                                    cluster_graph_data[i_,j_,k_] = this_cluster
                                    cluster_number = cluster_number + 1
                                else:
                                    #check cluster union
                                    merge_clusters = np.unique([cluster_graph_data[i_-1,j_,k_], cluster_graph_data[i_+1,j_,k_] \
                                , cluster_graph_data[i_,j_-1,k_], cluster_graph_data[i_,j_+1,k_] \
                                , cluster_graph_data[i_,j_,k_-1], cluster_graph_data[i_,j_,k_+1]])
                                    merge_clusters = merge_clusters[1:] #quit first value = 0

                                    this_cluster = merge_clusters[0]
                                    cluster_graph_data[i_,j_,k_] = this_cluster
                                    for cluster_to_merge in merge_clusters[1:]:
                                        cluster_graph_data[cluster_graph_data == cluster_to_merge] = this_cluster


                            else:
                                this_cluster = cluster_graph_data[i_,j_,k_]

                            #find neighbours and give cluster_number
                            if time_slice[i_-1,j_,k_] == 1:
                                cluster_graph_data[i_-1,j_,k_] = this_cluster
                            elif time_slice[i_+1,j_,k_] == 1:
                                cluster_graph_data[i_+1,j_,k_] = this_cluster
                            elif time_slice[i_,j_-1,k_] == 1:
                                cluster_graph_data[i_,j_-1,k_] = this_cluster
                            elif time_slice[i_,j_+1,k_] == 1:
                                cluster_graph_data[i_,j_+1,k_] = this_cluster
                            elif time_slice[i_,j_,k_-1] == 1:
                                cluster_graph_data[i_,j_,k_-1] = this_cluster
                            elif time_slice[i_,j_,k_+1] == 1:

                    # if not == 1¡, keep the search 
                        # if not neighbours, keep the search

        cluster_graph_data_total[:,:,:,t_] = cluster_graph_data

    return cluster_graph_data_total
