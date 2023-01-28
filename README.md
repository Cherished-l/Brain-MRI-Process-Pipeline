# Overview
With the development of deep learning, a large number of works use brain MRI images for diagnostic prediction.
However, many novices do not know much about MRI. Most natural image vision researchers often directly train the original MRI, and often cannot get good training results and explanations, which will waste a lot of time.
Therefore, this work will describe how to preprocess the mri, and then directly align it for training.
It has been compiled by UKB and ADNI Database.
# Requerements
The following work is to explain the **linux** platform, windows and mac can also be referred to, just need to pay less attention
There are many preprocessing tools, such as Freesurfer, FSL, ANTs, SPM and so on. Here I will explain the combination of FSL and ANTs.

1. install FSL from [https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FslInstallation](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FslInstallation)
   1. It is recommended to use fsinstaller.py for installation
   2. Offline installation can also be used, but pay attention to using miniconda(or conda) to create a virtual environment named **fslpython**, and modify the FSL address in bashrc.
2. install ANTs from [https://github.com/ANTsX/ANTs/wiki/Compiling-ANTs-on-Linux-and-Mac-OS](https://github.com/ANTsX/ANTs/wiki/Compiling-ANTs-on-Linux-and-Mac-OS)
   1. follow "Installing developer tools"
3. install nipype, nibabel
# Pipelines
## For Structural MRI
### Process overview

- Orientation correction

Different shooting machines, doctors, patients and other factors lead to different directions of images. This step rotates all images to the same orientation. (The direction here refers to the head facing)

- Crop the image (remove the neck)

Part of the neck area is automatically cut. This step is for better stripping of the skull. **This step is not necessary but recommended**, since the direct removal of the skull will leave most of the neck area.

- Stripping the skull

Remove useless information about the skull. Laying the basis for white matter and gray matter segmentation

- Registration

Register each image to the standard brain space to facilitate subsequent roi feature extraction, neural network training, etc.

- bias correction

Correction for bias field effects
### Note

- Crop the image (remove the neck)** is not necessary but recommended. **TThe picture below will show the schematic diagram of directly stripping the skull without cutting. Please select according to the specific image situation

![image.png](https://cdn.nlark.com/yuque/0/2023/png/25509636/1674889428763-5df41811-fe92-4676-a1c3-a221ca3d4e28.png#averageHue=%23181818&clientId=ud776d918-3dab-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=325&id=u29b594df&margin=%5Bobject%20Object%5D&name=image.png&originHeight=1300&originWidth=1696&originalType=binary&ratio=1&rotation=0&showTitle=false&size=470448&status=done&style=none&taskId=ub79c0699-3357-43e5-ade1-46089379b27&title=&width=424)

- The scalping and registration order can be reversed. If registering first, please use the MNI152_T1_1mm.nii.gz template for registration, if you peel off the scalp first and then register, please use MNI152_T1_1mm_brain.nii.gz. However, **it is more recommended to peel off the scalp first and then perform registration.**
### Code
This work uses a multi-threaded batch processing mechanism, you can choose to perform all processes on each image or perform each process on all images in turn.
Either one will take a long time, it is recommended to use nohup to observe the running status.
#### perform all processes on each image
```
python all_in_one/Process_all.py
```
#### perform each process on all images in turn
```
python one_by_one/orient.py
python one_by_one/remove_neck.py
python one_by_one/skull.py
python one_by_one/registration.py
python one_by_one/bias_correction.py
```
## For functional MRI
## For DTI
# References
[https://github.com/junyuchen245/TransMorph_Transformer_for_Medical_Image_Registration/blob/main/PreprocessingMRI.md](https://github.com/junyuchen245/TransMorph_Transformer_for_Medical_Image_Registration/blob/main/PreprocessingMRI.md)
[https://github.com/quqixun/BrainPrep](https://github.com/quqixun/BrainPrep)

