class Evaluation(object):
    @staticmethod
    def run_evaluation(postprocessing_dir):
        return


if __name__ == "__main__":
    import argparse

    argParser = argparse.ArgumentParser()
    argParser.add_argument(
        "--postprocessing-dir", help="Directory in which the postprocessing files will be stored.", required=True
    )
    args = argParser.parse_args()
    Evaluation.run_evaluation(args.postprocessing_dir)
