class Evaluation(object):
    @staticmethod
    def run_evaluation(inference_dir, evaluation_dir):
        return


if __name__ == "__main__":
    import argparse

    argParser = argparse.ArgumentParser()
    argParser.add_argument("--inference-dir", help="Directory in which the predictions are stored.", required=True)
    argParser.add_argument(
        "--evaluation-dir", help="Directory in which the evaluation files will be stored.", required=True
    )
    args = argParser.parse_args()
    Evaluation.run_evaluation(args.inference_dir, args.evaluation_dir)
