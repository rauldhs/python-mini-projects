import os
import re
import argparse

extensions = (".srt", ".ass", ".sub", ".vtt")

# Function to rename SRT files in a directory
def rename_all_episodes(directory_path: str, name: str, special_rules: str = "") -> None:
    """Rename subtitle files in a directory according to specified rules."""
    pattern = re.compile(r"(\d+)")
    files = os.listdir(directory_path)

    for file_name in files:

        if file_name.endswith(extensions):
            old_path = os.path.join(directory_path, file_name)

            file_name = re.sub(rf"{special_rules}|Season[-_]?\s?\d+|season[-_]?\s?\d+|S[-_]?\d+|\d+p", '', file_name)
            match = pattern.search(file_name)
            
            if match:
                episode_number = match.group(1) 
                file_extension = os.path.splitext(file_name)[1]
                formatted_name = f"{name}_{int(episode_number):d}{file_extension}"
                new_path = os.path.join(directory_path, formatted_name)

                try:
                    os.rename(old_path, new_path)
                    print(f"Renamed '{old_path}' to '{new_path}'")
                except OSError as e:
                    print(f"Error renaming '{old_path}': {e}") 

def move_files(directory: str, subtitles_directory:str) -> None:
    """Move subtitle files into their respective subdirectories based on episode number."""

    files = os.listdir(subtitles_directory)

    for file_name in files:
        match = re.search(r'_(\d+)\.', file_name)
        if match:
            subdirectory_path = os.path.join(directory, match.group(1))

            if file_name.endswith(extensions) and os.path.exists(subdirectory_path):
                old_path = os.path.join(directory, file_name)
                new_path = os.path.join(subdirectory_path, file_name)
                try:
                    os.rename(old_path, new_path)
                    print(f"Moved '{old_path}' to '{new_path}'")
                except OSError as e:
                    print(f"Error moving '{old_path}': {e}")

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Rename subtitle files in a directory.")
    parser.add_argument("-d", "--directory", type=str, required=True, help="Path to the directory containing subtitle files.")
    parser.add_argument("-n", "--name", type=str, required=True, help="Base name for the renamed episodes.")
    parser.add_argument("-r", "--rules", type=str, default="", help="Special rules for renaming (optional).")
    parser.add_argument("-a", "--add", type=str,default=False, help="Specifies directory where to check for subdirectories to put the files in")
    args = parser.parse_args()

    # Call the renaming function
    rename_all_episodes(args.directory, args.name, args.rules)

    if args.add:
        move_files(args.add,args.directory) 
