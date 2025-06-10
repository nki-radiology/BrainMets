import os
import dicom2nifti
import numpy as np
import nibabel as nib
from HD_BET.run import run_hd_bet


class Preprocessing(object):
    @staticmethod
    def create_dummy_annotations(preprocessing_dir):
        scan_names = sorted(os.listdir(preprocessing_dir))
        for i, scan_name in enumerate(scan_names):
            img = nib.load(os.path.join(preprocessing_dir, scan_name, "brain_masked_mri.nii.gz"))
            anno = nib.Nifti1Image((np.asarray(img.dataobj) > 0).astype(np.uint8), img.affine)
            nib.save(anno, os.path.join(preprocessing_dir, scan_name, "annotation.nii.gz"))
    
    @staticmethod
    def series_to_nifti(dicom_series_directory, nifti_file_path):
        dicom2nifti.dicom_series_to_nifti(dicom_series_directory, nifti_file_path, reorient_nifti=False)

    @staticmethod
    def apply_brain_mask(nifti_file_path, masked_nifti_file_path):
        run_hd_bet(nifti_file_path, masked_nifti_file_path, bet=True, keep_mask=False)

    @staticmethod
    def run_preprocessing(data_dir, preprocessing_dir):
        scan_names = sorted(os.listdir(data_dir))
        for i, scan_name in enumerate(scan_names):
            print(f"Preprocessing {i + 1} / {len(scan_names)}")
            scan_dir_in = os.path.join(data_dir, scan_name)
            scan_dir_out = os.path.join(preprocessing_dir, scan_name)
            os.makedirs(scan_dir_out, exist_ok=True)
            scan_nii_path = os.path.join(scan_dir_out, "mri.nii.gz")
            Preprocessing.series_to_nifti(scan_dir_in, scan_nii_path)
            masked_scan_nii_path = os.path.join(scan_dir_out, "brain_masked_mri.nii.gz")
            Preprocessing.apply_brain_mask(scan_nii_path, masked_scan_nii_path)


if __name__ == "__main__":
    import argparse

    argParser = argparse.ArgumentParser()
    argParser.add_argument(
        "--data-dir",
        help="Directory in which the raw DICOM data is stored in the correct folder structure.",
        required=True,
    )
    argParser.add_argument(
        "--preprocessing-dir", help="Directory in which the preprocessed Nifti files will be stored.", required=True
    )
    args = argParser.parse_args()
    Preprocessing.run_preprocessing(args.data_dir, args.preprocessing_dir)
