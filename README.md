Hugin-Enfuse HDR Toolkit

The Hugin-Enfuse HDR Toolkit is a set of scripts designed to automate the HDR workflow for RAW photos directly from the memory card. It organizes bracketed RAW images, aligns them using Hugin, and merges the exposures into HDR images using Enfuse.
Contents

    camera_raw_sorter.py: A script to sort and rename RAW photos into exposure brackets.
    align_and_fuse_hdr.py: A script to align and fuse bracketed images into HDR images.

Purpose

This toolkit is for photographers who want to automate the process of sorting RAW bracketed images, aligning them, and creating HDRs without the need to manually manage file names, groupings, or alignment steps.
Installation
Prerequisites

Before using the scripts, ensure you have the following installed:

    Hugin (for image alignment)
    Enfuse (for exposure fusion)
    Python 3.6+ with the following dependencies:
        os
        subprocess
        re
        collections

To install Python dependencies:

pip install -r requirements.txt

Install Hugin and Enfuse

    Hugin: Download from Hugin's official website or use your package manager (e.g., Homebrew on macOS, APT on Linux).
    Enfuse: Typically bundled with Hugin. If not, you can install it from Enfuse's website.

Usage
1. Sorting RAW Photos (camera_raw_sorter.py)

This script sorts RAW photos by their timestamp, groups them into exposure brackets, and renames them with group and exposure tags (e.g., Group_1_E1, Group_1_E2).
Running the Script

python camera_raw_sorter.py --folder_path /path/to/raw/photos --time_window 2 --prefix "Group"

Arguments:

    folder_path: Path to the folder with RAW files (default: current directory).
    time_window: Time window (in seconds) to group photos into brackets (default: 2 seconds).
    prefix: Prefix for renamed files (default: "Group").
    raw_extensions: List of RAW file extensions (default: .arw, .cr2, .nef, etc.).

2. Aligning and Fusing Images (align_and_fuse_hdr.py)

This script groups the images by their exposure bracket, aligns them using Hugin, and then creates HDR images using Enfuse.
Running the Script

python align_and_fuse_hdr.py --folder_path /path/to/your/images

Arguments:

    folder_path: Path to the folder with grouped images (default: current directory).

The script will:

    Group the images based on their "Group_X" number.
    Align the images using Hugin's align_image_stack tool.
    Fuse the aligned images into HDRs with Enfuse.
