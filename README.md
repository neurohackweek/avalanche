## fMRI Point Process Avalanches

A Python package for doing point process analyses on fMRI data.

Built at [Neurohackweek 2017](https://github.com/neurohackweek/nhw2017) by:
- [Asier Erramuzpe](https://github.com/erramuzpe)
- [Jessica Dafflon](https://github.com/JessyD)
- [Dan Lurie](https://github.com/danlurie)
- [Brian Roach](https://github.com/br-bieegl)

(Project directory structure organization via [Shablona](https://github.com/uwescience/shablona).)

## More Info
As a first pass, we have implemented the threshold-based point process and avalanche detection methods described in the following paper:

>Tagliazucchi, E., Balenzuela, P., Fraiman, D., & Chialvo, D. R. (2012). Criticality in large-scale brain FMRI dynamics unveiled by a novel point process analysis. Frontiers in Physiology, 3, 15. [http://doi.org/10.3389/fphys.2012.00015](http://doi.org/10.3389/fphys.2012.00015)

### Summer of Code Blog Posts
Asier created an early version of this package in 2015 as a participant in the Google Summer of Code program. He documented his work in a few blog posts:
- [Integration of Measures and Point Process Developing](http://erramuzpe.github.io/C-PAC/blog/2015/08/07/integration-of-measures-and-point-process-developing/)
- [Clustering and Avalanche Detection Algorithms](http://erramuzpe.github.io/C-PAC/blog/2015/08/14/clustering-and-avalanche-detection-algorithms/)

His original code can be found [here](https://github.com/roijo/C-PAC_complexitytools/blob/master/CPAC/series_mod/criticality.py).

### Test Data
To test our code during Neurohackweek, in addition to simulated data with known avalanches, we also used openly shared preprocessed fMRI data from [OpenNeuro](https://openneuro.org/):
- Dataset (associated with [this paper](http://journals.plos.org/plosone/article?id=10.1371/journal.pone.0107145), but the acquisition is described [here](http://journals.plos.org/plosone/article?id=10.1371/journal.pone.0069224))
- [Analysis](https://openneuro.org/datasets/ds001032/versions/00001?app=FMRIPREP&version=13&job=bbfe5cc0-e49b-47fe-bd85-442c790a155c)
