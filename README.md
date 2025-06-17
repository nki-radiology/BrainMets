<div align="center">

# BrainMets AI

</div>

<div align="center">
    <img src=".pictures/nki_logo_2.png" alt="NKI" width="200" height="auto" />
    <img src=".pictures/robovision_logo_3.png" alt="Robovision" width="200" height="auto" />
</div>

<div align="center">

## A Data-centric Approach to Deep Learning for Brain Metastasis Analysis at MRI 

</div>

BrainMets AI is the result of a collaboration between the [Netherlands Cancer Institute](https://www.nki.nl) (NKI) and [Robovision Healthcare](https://www.brainmets.ai). This repository gives further insights in how the underlying AI model was trained and the evaluation was performed. For more details we would like to refer to the article *"Topff L, et al. A Data-centric Approach to Deep Learning for Brain Metastasis Analysis at MRI. Radiology, 2025. DOI: 10.1148/radiol.242416"*.

You can try out the BrainMets AI model on our [Test Page](https://testflight.healthcare.robovision.ai/#/ZmyJVF1RCupHEwCZ1WTO), for research purposes only, not for clinical use.

---

## Table of Contents
1. [Overview](#overview)  
2. [Installation](#installation)  
3. [Data](#data)  
4. [Preprocessing](#preprocessing)  
5. [Training](#training)  
6. [Inference](#inference)
7. [Postprocessing](#postprocessing)  
8. [Evaluation](#evaluation)  
9. [Citation](#citation)  

---

## Overview

The BrainMets AI pipeline is built upon a modified nnU-Net framework to detect and segment brain metastases of all sizes on contrast-enhanced 3D T1-weighted MRI. The repository provides:

- **Preprocessing**: DICOM to Nifti conversion,  brain extraction and some basic checks.  
- **Training**: Five-fold cross-validation on the preprocessed dataset.  
- **Inference**: Use the trained model to generate predictions on another dataset.
- **Postprocessing**: Generate probability maps, thresholding, connected‐component analysis and lesion confidence scoring.  
- **Evaluation**: Scripts to compute lesion‐wise sensitivity, Dice Similarity Coefficient (DSC), Normalized Surface Distance (NSD), and Free-response Receiver Operating Characteristic (FROC) curves.

---

## Installation

### Requirements

- **Operating System**: Ubuntu 20.04+  
- **Python**: 3.11
- **CUDA**: 11.8
- **Disk Space**: ≥ 100 GB (depending on dataset size) 
- **RAM**: ≥ 32 GB 
- **GPU**: ~ NVIDIA A100 80 GB

### Python

Make sure to first create a virtual environment and install the correct Pytorch version. Then, all other required Python dependencies can be installed using the `requirements.txt` file. 

1. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate
```

2. **Install Pytorch**
```bash
pip install torch==2.6.0 --index-url https://download.pytorch.org/whl/cu118
```

3. **Install other dependencies**
```bash
pip install -r requirements.txt
```

4. **Verify installation**
```bash
python -c "import torch, nnunetv2, HD_BET; print('OK')"
```

---

## Data

Place all input MRIs (in DICOM format) under a DATA_DIR in the expected directory structure:
```bash
DATA_DIR/
    scan_001/
        dicom_file_001.dcm
        ...
    scan_002/
        dicom_file_001.dcm
        ...
    ...
```

Each scan folder must contain all the DICOM files of only a single DICOM series.

---

## Preprocessing

```bash
python preprocessing/preprocessing.py --data-dir DATA_DIR --preprocessing-dir PREPROCESSING_DIR
```

This will generate:

```bash
PREPROCESSING_DIR/
    scan_001/
        brain_masked_mri.nii.gz
    scan_002/
        brain_masked_mri.nii.gz
    ...
```

---

## Training

Using the preprocessed data files, you can use any labeling platform that accepts Nifti files to generate binary segmentation masks. When you created these masks, put them in the PREPROCESSING_DIR:

```bash
PREPROCESSING_DIR/
    scan_001/
        brain_masked_mri.nii.gz
        annotation.nii.gz
    scan_002/
        brain_masked_mri.nii.gz
        annotation.nii.gz
    ...
```

```bash
python training/training.py --preprocessing-dir PREPROCESSING_DIR --training-dir TRAINING_DIR
```

This will check if the data is consistent across the PREPROCESSING_DIR. If all goes well, the TRAINING_DIR will be populated and the training starts.

```bash
TRAINING_DIR/
    nnUNet_raw/
        Dataset001_BrainMetastasisAI/
            imagesTr/
                scan_001_0000.nii.gz
                scan_002_0000.nii.gz
                ...
            labelsTr/
                scan_001.nii.gz
                scan_002.nii.gz
                ...
    nnUNet_preprocessed/
        Dataset001_BrainMetastasisAI/
            ...
    nnUNet_results/
        Dataset001_BrainMetastasisAI/
            ...
```

---

## Inference

Once there is a trained model available in the TRAINING_DIR, you can also do inference for any PREPROCESSING_DIR and have the result outputted in the INFERENCE_DIR:

```bash
python inference/inference.py --preprocessing-dir PREPROCESSING_DIR --training-dir TRAINING_DIR --inference_dir INFERENCE_DIR
```

The INFERENCE_DIR will look like this:

```bash
INFERENCE_DIR/
    scan_001/
        brain_masked_mri.nii.gz (symlink)
        annotation.nii.gz (symlink - optional)
        prediction.nii.gz
    scan_002/
        brain_masked_mri.nii.gz (symlink)
        annotation.nii.gz (symlink - optional)
        prediction.nii.gz
    ...
```

---

## Postprocessing

To postprocess an INFERENCE_DIR, make sure you started from a PREPROCESSING_DIR where you added ground truth annotations:

```bash
python postprocessing/postprocessing.py --inference_dir INFERENCE_DIR
```

This will inject some result.csv files into the INFERENCE_DIR.

```bash
INFERENCE_DIR/
    scan_001/
        brain_masked_mri.nii.gz (symlink)
        annotation.nii.gz (symlink)
        prediction.nii.gz
        result.csv
    scan_002/
        brain_masked_mri.nii.gz (symlink)
        annotation.nii.gz (symlink)
        prediction.nii.gz
        result.csv
    ...
```

---

## Evaluation

To run the evaluation, do:

```bash
python evaluation/evaluation.py --inference-dir INFERENCE_DIR --evaluation-dir EVALUATION_DIR
```

This will generate the tables and figures like in the paper:

```bash
EVALUATION_DIR/
    figure_1.png
    table_1.csv
    ...
```

---

## Citation
When making use of BrainMets AI, please also acknowledge this by referencing to or citing our work:

Topff L, et al. A Data-centric Approach to Deep Learning for Brain Metastasis Analysis at MRI. Radiology, 2025. DOI: 10.1148/radiol.242416.

```bibtex
@article{Topff2025BrainMets,
  title   = {A Data-centric Approach to Deep Learning for Brain Metastasis Analysis at MRI},
  author  = {Topff, Laurens et al.},
  journal = {Radiology},
  year    = {2025},
  doi     = {10.1148/radiol.242416},
}
```

---

## Contact
For questions, bug reports, or feature requests, please open an issue on GitHub or contact:

Laurens Topff, MD, PhD (Corresponding author) — l.topff@nki.nl

Thank you for using our BrainMets AI!
