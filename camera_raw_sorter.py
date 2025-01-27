import os
from datetime import datetime

def filter_and_rename_raw_photos(folder_path="./", time_window=2, prefix="Group", raw_extensions=None):
    """
    Filters RAW photos taken within a few seconds of each other, groups them into brackets,
    and renames them with group and exposure tags (Group 1, E1, Group 2, E1, etc.).

    Args:
        folder_path (str): Path to the folder containing the RAW photos (default: current directory).
        time_window (int): Time window (in seconds) to group photos into brackets.
        prefix (str): Prefix for the renamed files (e.g., "Group").
        raw_extensions (list): List of RAW file extensions to process.
    
    Returns:
        None
    """
    if raw_extensions is None:
        raw_extensions = [".arw", ".cr2", ".nef", ".orf", ".dng", ".raf"]  # Common RAW formats

    # Get all RAW files sorted by modification time
    raw_files = sorted(
        [f for f in os.listdir(folder_path) if f.lower().endswith(tuple(raw_extensions))],
        key=lambda f: os.path.getmtime(os.path.join(folder_path, f))
    )

    if not raw_files:
        print("No RAW files found in the folder.")
        return

    last_time = None
    group_index = 0
    exposure_index = 0

    for raw_file in raw_files:
        raw_path = os.path.join(folder_path, raw_file)
        timestamp = datetime.fromtimestamp(os.path.getmtime(raw_path))

        # Check if this is a new bracket group
        if last_time is None or (timestamp - last_time).total_seconds() > time_window:
            group_index += 1
            exposure_index = 1  # Reset exposure index for a new group
        else:
            exposure_index += 1  # Increment exposure index within the same group

        # Rename the file with group and exposure tags
        new_name = f"{prefix}_{group_index}_E{exposure_index}{os.path.splitext(raw_file)[1]}"
        new_path = os.path.join(folder_path, new_name)

        os.rename(raw_path, new_path)
        print(f"Renamed: {raw_file} -> {new_name}")

        last_time = timestamp

if __name__ == "__main__":
    # Run the script from the current folder
    filter_and_rename_raw_photos(folder_path="./", time_window=2, prefix="Group")
