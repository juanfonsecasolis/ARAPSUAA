ARAPSUAA: Automatic recognition of accessible pedestrian signals using an adaptive approach    
===========================================================================================
Code for master thesis [*Recognition of accessible pedestrian signals using an adaptive approach*](http://hdl.handle.net/2238/10642).

Author
-------
Juan Manuel Fonseca-Solís<sup>1,2</sup>    
<sup>1</sup> Electronics School ([IE](http://www.ie.tec.ac.cr)) at [TEC](http://www.tec.ac.cr).  
<sup>2</sup> Research Center in Information and Communication Technologies ([CITIC](http://www.citic.ucr.ac.cr/)) at [UCR](https://www.ucr.ac.cr/).  

![](./logo-tec.png)

#### Contact
[Juan Fonseca](mailto:juanma2268[at]gmail[dot]com)  
CITIC-UCR  
San Pedro de Montes de Oca  
11501-2060 San José, Costa Rica  

Abstract
---
**Context.** The automatic detection of accessible pedestrian signals (APS), a type of sound emitted by pedestrian traffic lights to enable passage at pedestrian crossings, has made easier the recognition of other audible tones, such as train horns, ambulance sirens, and police patrol alarms, among others. So far, previous authors have managed to recognize APS with partial success, since the exposed designs have presented suboptimal musical recognition kernels, fixed tone thresholds unable to adapt to the changing level of street noise and separate processing of continuous and discontinuous musical contours. The detection rates reached in the best of the previous works have been 91% precision, 90% specificity, 80% recall, and 83% F-score.

**Method**. An algorithm for the recognition of accessible pedestrian signals is presented. It consists in a three-harmonics musical recognition kernel design with a decay proportional to 1/k^2, two algorithms for the dynamic estimation of the tone threshold, that vary according to the signal-to-noise ratio (TS2Means and the leaky integrator), and the Mahalanobis distance with covariance matrices modeled according to the APS musical contours for noise robustness. 

**Results.** The best detection rates reached in this work were 93% precision, 89% specificity, 92% recall, 92% F-score, and 80% Matthew's correlation coefficients. So we found an improvement of +12% in recall while keeping almost constant precision and specificity, this means that the number of true positives increased and the number of false positives &mdash;important for user's safety&mdash; remained bounded. Also, the covariance matrices reached acceptable metrics, confirming the possibility to tolerate noise in sound patterns.

**Future work.** The score matrices (another name for the error surface) were constructed based on a fixed exponential distribution of alpha and beta parameters, it would be beneficial to apply a genetic algorithm approach to get an optimized combination of values. Also, other types of sounds, besides APS, could be processed using the covariance matrices.

Package Description
---
This repository contains all the code to reproduce the results of the thesis [*Recognition of accessible pedestrian signals using an adaptive approach*](http://hdl.handle.net/2238/10642). It contains a Python implementation of the proposed algorithm, including the elaboration of:

1. N-th harmonics prime and non-prime music kernels.
1. Pitch contour signals from real recordings in .wav format.
1. Alert signals by evaluating APS templates based on three types of distances (Euclidean, the proportion of tones, Mahalanobis) and three types of filtering techniques (fixed threshold, TS2Means, leaky integrator).
1. Covariance matrices plot for the three types of sounds (figures below)
1. Automatic evaluation against the manually annotated onsets in terms of precision, specificity, recall, F-score, and Matthew's correlation coefficients.
 
<div>
<img width="32%" src="img/cov-full-matrix-cuckoo.png">
<img width="32%" src="img/cov-full-matrix-highchirp.png">
<img width="32%" src="img/cov-full-matrix-lowchirp.png">
</div> 
 
Recreate the results
---
The algorithm implementation works by default with `python 2.7`. For data pre-processing, we have to use libraries such as `numpy`, `scipy`, `pyaudio`, `oc2python`, and `peakutils`. 

Also, make sure that the recordings folder (that can be cloned from [here](https://github.com/juanfonsecasolis/grabaciones-semaforos)) is named `grabaciones-semaforos`, and that it is placed at the same level of this repository. 

Figures 1.17, 1.18b, 1.19b, 2.1, 2.17, 3.2, 3.3, 3.13, 3.19, 3.20
    
    python2.7 Test/TestFigures.py    
   
Figures 3.6-3.12, 3.14-3.17, 4.3, 4.4
 
    python2.7 Test/TestBatchFigures.py
 
Figures 4.11, 4.14-4.21, and tables 4.4, 4.5, 4.13, 4.18, 4.23, 4.28, 4.33, 4.38, 4.43 

    python2.7 Test/TestScenarios.py   

Tables 4.7-4.12, 4.20-4.22, 4.25-4.27, 4.30-4.32, 4.35-4.37, 4.40-4.42
    
    python2.7 Test/TestBruteForce.py
    
**Disclaimer:** this particular test is fairly heavy to run in terms of memory usage. A machine with at least 12GB of RAM is recommended, and depending of the scenario, the test can take 20 to 60 min approximately.

Figures 2.2, 2.3, 2.12, 2.11, 4.5-4.10, 1.18a, 1.19a, 2.6, 2.14, 2.15
    
    python2.7 Test/TestOctave.py
    
Alternatively, you can build all figures at once executing `./run.sh`. The figures are stored in the following directories: 

* /tmp/outputDataAPS/img 
* /tmp/outputDataAPS/covarianceMatrices 
* /tmp/outputDataAPS/snr

**Note:** if you are using PyCharm to run the code as a project then remember to mark the /src folder as the source folder, to avoid dependency errors.

Data used in the paper
---
A total of 79 recordings were collected from 11 different Novax DS100 units in the Costa Rican great metropolitan area (GAM), consisting in: 

* 36 cuckoo recordings
* 30 chirp-1 recordings
* 13 chirp-2 recordings 

The recordings were acquired using three smartphones of medium-gamma (Samsung Galaxy Ace S5830, Samsung Galaxy S Duos S7562, LG G2 mini D618), employing a sampling rate of 44.1 kHz, and a quantization of 32 bits. The audio was recorded either during the morning when less traffic was present in streets, as well as after midday when roads were more populated. The weather conditions were mostly sunny and cloudly, the last one with the presence of light rain. The duration of the recordings ranged from 13 s to 35 s, depending on the activity period of the Novax units, and the signal-to-noise ratio (SNR) corresponded to 1.1 dB (Novax units were designed to maintain an SPL level of +5dB above the ambient noise, with a limit on 90 dB). The recordings were downsampled to 22.05 kHz to save disk space as no relevant information is stored above that frequency range.

**Acknowledges:** recordings taken from Samsung devices were provided by Mario Monge and Sharon Bejarano in 2013.

Dependencies
---
* A working distribution of [Python 2.7](https://www.python.org/downloads/).
* [Numpy](http://www.numpy.org/), [Scipy](http://www.scipy.org/), and [Peakutils](https://pypi.org/project/PeakUtils/) for signal processing.
* [Pyaudio](https://pypi.org/project/PyAudio/) for audio processing.
* [Matplotlib](http://matplotlib.org) for plotting the results.
* [Oct2py](https://pypi.org/project/oct2py/) and [Octave signal package](https://octave.sourceforge.io/signal/) for running TS2Means, plotting the audio filters, and visualize the score matrices.
* [TS2Means, w2means](http://www.cise.ufl.edu/~acamacho/publications) (included in the repository)
    * Camacho, A., Detection of Pitched/Unpitched Sound Using Pitch Strength Clustering, Proceedings of the Ninth International Conference on Music Information Retrieval, pp. 533-537, Philadelphia, September 2008.

The easiest way to set up a proper computing environment is first to download and install Python distributions from [Anaconda](https://store.continuum.io/cshop/anaconda/). Alternatively, run `./installDependencies.sh` 

System tested
---
### PC
| Feature | Description | 
|---------|------------------------------------------| 
| Machine | Lenovo ideapad 330S | 
| OS      | Ubuntu 18.04.1 LTS | 
| CPU     | Intel(R) Core(TM) i5-8250U CPU @ 1.60GHz | 
| RAM     | 12 GB / 665 MHz                          | 


    Python Info: 
    ------------
    Python 2.7 

    Python Packages Info (conda)
    ----------------------------
    python-numpy/bionic,now 1:1.13.3-2ubuntu1 amd64 
    python-scipy/bionic,now 0.19.1-2ubuntu1 amd64 
    python-matplotlib/bionic,now 2.1.1-2ubuntu3 amd64 
    python-matplotlib-data/bionic,bionic,now 2.1.1-2ubuntu3 all 
    python-pyaudio/bionic,now 0.2.11-1build2 amd64 

Citation
---
You can cite this work by using the following Bibtex entry:
```
@mastersthesis{FonsecaARAPSUAA2018,
  author       = {Juan M. Fonseca-Solís}, 
  title        = {Reconocimiento automático de señales peatonales accesibles usando un enfoque adaptativo},
  school       = {Escuela de Electrónica},
  year         = 2018,
  address      = {Cartago, Costa Rica},
  month        = 4,
  url          = {http://hdl.handle.net/2238/10642}
}
```

If you need DOI identifiers, you can use the following ones:
* Repository: [![DOI](https://zenodo.org/badge/189270078.svg)](https://zenodo.org/badge/latestdoi/189270078)
* Thesis document: [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3246928.svg)](https://doi.org/10.5281/zenodo.3246928)

Disclaimer
---
ARAPSUAA was developed following the abstract explanations published publicly by the project [B6146](https://vinv.ucr.ac.cr/sigpro/web/projects/B6146) (also known as RASP) of the University of Costa Rica. The code was rewritten completely from zero in a different language, adding the new findings described in the abstract, and with the purpose to serve as a scientific library. No grant, scholarship or other financial help provided by any public or private organization supported the elaboration of ARAPSUAA. I have made public the code because I believe that reproducibility is a condition for science, moreover, because I want to encourage researchers living in low-income-countries (LIC) to do independent research when working full-time in the academia is not possible.

_"In scientic work, means are virtually nothing whereas the person is almost everything."_ - Santiago Ramón y Cajal

License
---
Copyright (c) 2018, Juan M. Fonseca-Solís  
The source code is released under the [GPL](https://www.gnu.org/licenses/gpl-3.0.en.html) license.


