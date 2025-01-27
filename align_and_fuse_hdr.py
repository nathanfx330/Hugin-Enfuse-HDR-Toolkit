import os
import subprocess
from collections import defaultdict
import re

def group_images_by_group_number(folder_path="./", image_extensions=None):
    """
    Groups images by their 'Group_X' number in filenames.

    Args:
        folder_path (str): Path to the folder containing the JPG photos.
        image_extensions (list): List of image file extensions to process (default: .jpg).
    
    Returns:
        dict: A dictionary with the group number as key and a list of image paths as values.
    """
    if image_extensions is None:
        image_extensions = [".jpg"]  # Only process JPG files

    # Get all JPG files
    jpg_files = [f for f in os.listdir(folder_path) if f.lower().endswith(tuple(image_extensions))]

    grouped_files = defaultdict(list)

    # Regex to match the group number in filenames like 'Group_19_E1.jpg'
    group_pattern = re.compile(r"(Group_\d+)")

    for jpg_file in jpg_files:
        match = group_pattern.search(jpg_file)
        if match:
            group_name = match.group(1)  # Extract "Group_X"
            grouped_files[group_name].append(os.path.join(folder_path, jpg_file))

    return grouped_files

def align_images_with_hugin(files, output_folder="./aligned"):
    """
    Aligns images using Hugin's align_image_stack tool and saves aligned TIFF files in the specified folder.

    Args:
        files (list): List of file paths to align.
        output_folder (str): Folder to save the aligned TIFF images.
    
    Returns:
        list: List of paths to the aligned TIFF images.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    group_prefix = "aligned_"
    cmd = ["align_image_stack", "-a", os.path.join(output_folder, group_prefix), *files]
    try:
        subprocess.run(cmd, check=True)
        print(f"Images aligned for {files[0]}...")

        # Collect all aligned images starting with 'aligned_' and having .tif extension
        aligned_files = [os.path.join(output_folder, f) for f in os.listdir(output_folder) if f.startswith(group_prefix) and f.lower().endswith(".tif")]
        return aligned_files
    except subprocess.CalledProcessError as e:
        print(f"Error aligning images: {e}")
        return []

def process_hdr_with_enfuse(grouped_files, folder_path, output_folder="./out", batch_size=3):
    """
    Process each group of bracketed images with Enfuse to create HDR images in smaller batches.

    Args:
        grouped_files (dict): A dictionary of grouped images.
        folder_path (str): Path to the folder containing the images.
        output_folder (str): Path to the folder where HDR images will be saved.
        batch_size (int): Number of files to process in each Enfuse command.
    
    Returns:
        None
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    total_groups = len(grouped_files)
    print(f"Total groups to process: {total_groups}")

    # Process each group
    for group_index, (group_name, files) in enumerate(grouped_files.items(), 1):
        print(f"\nProcessing group {group_index} of {total_groups}: {group_name}...")

        # Align the images using Hugin before processing with Enfuse
        aligned_files = align_images_with_hugin(files, output_folder="./aligned")

        if aligned_files:
            # Process in smaller batches to reduce memory usage
            total_batches = (len(aligned_files) + batch_size - 1) // batch_size  # Ceiling division
            print(f"Total batches: {total_batches}")

            for batch_index, i in enumerate(range(0, len(aligned_files), batch_size), 1):
                batch = aligned_files[i:i + batch_size]
                output_file = os.path.join(output_folder, f"HDR_{group_name}_batch_{batch_index}.jpg")
                cmd = ["enfuse", "-o", output_file, "-g"] + batch  # Align images and output as JPG

                try:
                    subprocess.run(cmd, check=True)
                    print(f"Created HDR image: {output_file} (Batch {batch_index}/{total_batches})")
                except subprocess.CalledProcessError as e:
                    print(f"Error processing {group_name} batch {batch_index}: {e}")
        else:
            print(f"Skipping group {group_name} due to alignment failure.")

if __name__ == "__main__":
    # Run the grouping and HDR processing
    folder_path = "./"  # Current folder, or specify another path
    grouped_files = group_images_by_group_number(folder_path)
    
    if grouped_files:
        process_hdr_with_enfuse(grouped_files, folder_path)
