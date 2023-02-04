import argparse
from recognition import ann

parser = argparse.ArgumentParser(description='Process some arguments.')

parser.add_argument('--path_video', type=str, help='Path to the video file.')

parser.add_argument('--path_result', type=str, help='Path to the result file.')

# Parse the command line arguments
args = parser.parse_args()

# Access the --path_video argument
path_video = args.path_video

# Access the --path_result argument
path_result = args.path_result

if __name__ == "__main__":
    ann(url=path_video, path=path_result)
