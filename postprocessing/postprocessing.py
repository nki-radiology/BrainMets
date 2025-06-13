class Postprocessing(object):
    @staticmethod
    def run_postprocessing(inference_dir):
        return


if __name__ == "__main__":
    import argparse

    argParser = argparse.ArgumentParser()
    argParser.add_argument("--inference-dir", help="Directory in which the predictions are stored.", required=True)
    args = argParser.parse_args()
    Postprocessing.run_postprocessing(args.inference_dir)
