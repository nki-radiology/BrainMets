import os
# import shutil


class Inference(object):
    @staticmethod
    def predict_nnunet(training_dir, input_dir, output_dir):
        os.environ["nnUNet_raw"] = os.path.join(training_dir, "nnUNet_raw")
        os.environ["nnUNet_preprocessed"] = os.path.join(training_dir, "nnUNet_preprocessed")
        os.environ["nnUNet_results"] = os.path.join(training_dir, "nnUNet_results")

        from nnunetv2.utilities.file_path_utilities import get_output_folder
        from nnunetv2.inference.predict_from_raw_data import nnUNetPredictor

        predictor = nnUNetPredictor(tile_step_size=1, use_gaussian=False, use_mirroring=False, allow_tqdm=False)
        model_folder = get_output_folder("Dataset001_BrainMetastasisAI")
        predictor.initialize_from_trained_model_folder(model_folder, user_folds=[0, 1, 2, 3, 4])
        predictor.predict_from_files(input_dir, output_dir, save_probabilities=True, overwrite=False)

    @staticmethod
    def run_inference(preprocessing_dir, training_dir, inference_dir):
        temp_input_dir = os.path.join(inference_dir, "temp_input_dir")
        os.makedirs(temp_input_dir)
        temp_output_dir = os.path.join(inference_dir, "temp_output_dir")
        os.makedirs(temp_output_dir)
        scan_names = sorted(os.listdir(preprocessing_dir))
        for i, scan_name in enumerate(scan_names):
            scan_dir_in = os.path.join(preprocessing_dir, scan_name)
            os.symlink(
                os.path.join(scan_dir_in, "brain_masked_mri.nii.gz"),
                os.path.join(temp_input_dir, scan_name + "_0000.nii.gz"),
            )

        Inference.predict_nnunet(training_dir, temp_input_dir, temp_output_dir)
        # for i, scan_name in enumerate(scan_names):
        #     scan_dir_in = os.path.join(preprocessing_dir, scan_name)
        #     os.symlink(os.path.join(scan_dir_in, "brain_masked_mri.nii.gz"), os.path.join(temp_input_dir, scan_name + "_0000.nii.gz"))

        # shutil.rmtree(temp_input_dir)
        # shutil.rmtree(temp_output_dir)


if __name__ == "__main__":
    import argparse

    argParser = argparse.ArgumentParser()
    argParser.add_argument(
        "--preprocessing-dir", help="Directory in which the preprocessed Nifti files are stored.", required=True
    )
    argParser.add_argument("--training-dir", help="Directory in which the training files are stored.", required=True)
    argParser.add_argument("--inference-dir", help="Directory in which the predictions will be stored.", required=True)
    args = argParser.parse_args()
    Inference.run_inference(args.preprocessing_data_dir, args.training_dir, args.inference_data_dir)
