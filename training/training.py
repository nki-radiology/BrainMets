import os
import json


class Training(object):
    @staticmethod
    def create_nnunet_directories(preprocessing_dir, training_dir):
        nnunet_raw_dir = os.path.join(training_dir, "nnUNet_raw")
        os.makedirs(nnunet_raw_dir)
        nnunet_preprocessed_dir = os.path.join(training_dir, "nnUNet_preprocessed")
        os.makedirs(nnunet_preprocessed_dir)
        nnunet_results_dir = os.path.join(training_dir, "nnUNet_results")
        os.makedirs(nnunet_results_dir)
        imagestr_dir = os.path.join(nnunet_raw_dir, "Dataset001_BrainMetastasisAI", "imagesTr")
        os.makedirs(imagestr_dir)
        labelstr_dir = os.path.join(nnunet_raw_dir, "Dataset001_BrainMetastasisAI", "labelsTr")
        os.makedirs(labelstr_dir)
        scan_names = sorted(os.listdir(preprocessing_dir))
        for i, scan_name in enumerate(scan_names):
            print(f"Generating training data folders {i + 1} / {len(scan_names)}")
            scan_dir_in = os.path.join(preprocessing_dir, scan_name)
            os.symlink(
                os.path.join(scan_dir_in, "brain_masked_mri.nii.gz"),
                os.path.join(imagestr_dir, scan_name + "_0000.nii.gz"),
            )
            os.symlink(
                os.path.join(scan_dir_in, "annotation.nii.gz"), os.path.join(labelstr_dir, scan_name + ".nii.gz")
            )

        dataset_json = {
            "channel_names": {"0": "T1Gd"},
            "file_ending": ".nii.gz",
            "labels": {"background": 0, "metastasis": 1},
            "numTraining": len(scan_names),
        }
        with open(os.path.join(nnunet_raw_dir, "Dataset001_BrainMetastasisAI", "dataset.json"), "w") as f:
            json.dump(dataset_json, f, indent=4)

    @staticmethod
    def train_nnunet(training_dir):
        os.environ["nnUNet_raw"] = os.path.join(training_dir, "nnUNet_raw")
        os.environ["nnUNet_preprocessed"] = os.path.join(training_dir, "nnUNet_preprocessed")
        os.environ["nnUNet_results"] = os.path.join(training_dir, "nnUNet_results")

        from nnunetv2.experiment_planning.plan_and_preprocess_api import (
            extract_fingerprints,
            plan_experiments,
            preprocess,
        )
        from nnunetv2.run.run_training import run_training

        print("Fingerprint extraction...")
        extract_fingerprints([1], check_dataset_integrity=True)
        print("Experiment planning...")
        plan_experiments([1])
        print("Preprocessing...")
        preprocess([1], configurations=["3d_fullres"], num_processes=[4])
        for f in range(5):
            print(f"Training fold {f + 1} / {5}...")
            run_training("1", configuration="3d_fullres", fold=f)

    @staticmethod
    def run_training(preprocessing_dir, training_dir):
        Training.create_nnunet_directories(preprocessing_dir, training_dir)
        Training.train_nnunet(training_dir)


if __name__ == "__main__":
    # argParser = argparse.ArgumentParser()
    # argParser.add_argument(
    #     "--preprocessing-dir", help="Directory in which the preprocessed Nifti files are stored.", required=True
    # )
    # argParser.add_argument(
    #     "--training-dir",
    #     help="Directory in which the training files will be stored.",
    #     required=True,
    # )
    # args = argParser.parse_args()
    # Training.run_training(args.preprocessing_dir, args.training_dir)
    Training.run_training(
        "/raid/healthcare/jbertels/testing/preprocessing_dir", "/raid/healthcare/jbertels/testing/training_dir"
    )
