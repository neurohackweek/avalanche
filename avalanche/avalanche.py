"""
Function to compute Avalanche images

Expects full file path to resting state 4D nifti image
Currently, output images will be written to wd
"""

from __future__ import absolute_import, division, print_function
import numpy as np
import nibabel as nb
import os as os
from scipy.ndimage.measurements import label
from scipy.stats import zscore
from nilearn.masking import compute_epi_mask
from nilearn.masking import apply_mask
from nilearn.masking import unmask
from scipy.ndimage.morphology import generate_binary_structure

def avalanche(func_filename):
    #need to get func_filename (a nii file) as input
    img = nb.load(func_filename)
    data = img.get_data()
    
    #we need to make a mask, otherwise avalanches could happen outside the brain!
    mask_img = compute_epi_mask(func_filename)
    masked_data = apply_mask(func_filename, mask_img)
    
#    # Visualize it as an ROI - just for testing
#    from nilearn.plotting import plot_roi
#    plot_roi(mask_img)
    
    signal = zscore(masked_data, axis=0)
    signal[signal>1] = 1
    signal[signal<1]=0
    #nans are getting added to cluster 1 by label function, so set to 0
    signal[np.isnan(signal)] = 0
    
    #put the binary signal data back into 4D space:
    signal = unmask(signal, mask_img).get_data()
    
    #This is the avalanche identification step, which requires a 
    #structure to define the spatio(x-y-z)-temporal connectivity:
    struct_44 = generate_binary_structure(4,4)
    labeled_array, num_features = label(signal, struct_44)
    
    #get the size of the array:
    (n_x, n_y, n_z, n_t) = labeled_array.shape
    
    #reshape for efficiency with apply_mask:
    affine = mask_img.affine
    label_img = nb.Nifti1Image(labeled_array, affine)
    
    masked_label = apply_mask(label_img, mask_img)
    #initialize matrix to count uniques:
    uMat = np.zeros(shape=(num_features, n_t))
    
    #loop through each time point and identify cluster members:
    for i in range(n_t):
        #determine uniques at this time point:
        inds = np.unique(masked_label[i,:])
        #Note: 0 will always be a unique value, and we don't
        #actually care about zeros, so ignore them:
        uMat[(inds[1:].astype('int')-1),i] = 1
        
    #now the uMat matrix is populated with indicators for each of the "avalanches"
    #but we need to determine which are truly avalanches (i.e., occur in more than
    #one time point), and which are not
    avarray= np.zeros((uMat.shape[0], n_t+1))
    #fill this with binary data:
    avarray[:,1:]= uMat
    #and take the difference:
    avarray[:,1:] = np.diff(avarray, axis=1)
    #and then take it again to identify 1 to -1 (diff==-2) points - these are not 
    #avalanches!!!
    tmparray = np.diff(avarray, axis=1)
    
    #now we can efficiently remove all fake avalanches:
    fakes = np.asarray(np.where(np.sum(tmparray==-2,axis=1)))+1
    labeled_array[np.isin(labeled_array,fakes)]=0        
            
    #now single time point clusters should be removed
    #and we want to regenerate our labels:
    labeled_array, num_features = label(labeled_array, struct_44)
    
    img_new = nb.Nifti1Image(labeled_array, header=img.header, affine=img.affine)
    # Reconstruct the 4D volume
    ava_file = os.path.join(os.getcwd(), 'avalancheLabels.nii.gz')
    img_new.to_filename(ava_file)
        
    #make a new 4D array that is 1 time point greater than original data:
    transition_array = np.zeros((n_x, n_y, n_z, n_t+1))
    
    #the point process should come from the de-faked avalance data:
    signal = labeled_array
    signal[signal>0]=1
    #fill this transition array with binary data and leave first time point (t[0])
    #empty:
    transition_array[:,:,:,1:] = signal
    
    #take the difference between points across the 4th (time) dimension:
    onset_array = np.diff(transition_array, axis=3)
    onset_array[onset_array==-1] = 0
    #the onset array is back in the same time order and number of time points
    #as the original arrays...
    
    img_new = nb.Nifti1Image(onset_array, header=img.header, affine=img.affine
    # Reconstruct the 4D volume
    pp_file = os.path.join(os.getcwd(), 'binary_pp.nii.gz')
    img_new.to_filename(pp_file)

    Nvoxels = np.unique(labeled_array, return_counts='true')
    Nvoxels = np.asarray(Nvoxels).T
    #get rid of the 0 count (these aren't avalanches)
    Nvoxels = Nvoxels[1:]
    
    #could return num_features, Nvoxels
    