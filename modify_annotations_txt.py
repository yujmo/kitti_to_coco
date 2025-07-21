import glob
import string
import os
import shutil

def copy_all_images(image_root_path, merge_image_root_path, extensions=('.png', '.jpg', '.jpeg')):
    """
    Copy all images from image_root_path to merge_image_root_path.

    Args:
        image_root_path (str): Source directory containing images.
        merge_image_root_path (str): Destination directory.
        extensions (tuple): Tuple of allowed image extensions.
    """
    os.makedirs(merge_image_root_path, exist_ok=True)
    files = os.listdir(image_root_path)
    image_files = [f for f in files if f.lower().endswith(extensions)]
    print(f"Found {len(image_files)} images in {image_root_path}")
    for img in image_files:
        src = os.path.join(image_root_path, img)
        dst = os.path.join(merge_image_root_path, img)
        shutil.copyfile(src, dst)
    print(f"Copied {len(image_files)} images to {merge_image_root_path}")


def show_category(labels_list):
    """
    Print all unique class names present in a list of KITTI label files.
    Args:
        labels_list (list): List of label file paths.
    """
    
    category_list = []
    for label_file in labels_list:
        try:
            with open(label_file) as f:
                for line in f:
                    label_data = line.strip().split(' ')
                    category_list.append(label_data[0])
        except IOError as ioerr:
            print('File error:'+str(ioerr))
    print("Categories in dataset:", set(category_list))


def merge(line):
    """
    Merge a list of fields into a single line string (space separated, with newline at end).
    Args:
        line_fields (list): List of string fields.
    Returns:
        str: Space-separated string ending with newline.
    """
    each_line = ''
    for i in range(len(line)):
        if i != (len(line)-1):
            each_line = each_line + line[i] + ' '
        else:
            each_line = each_line + line[i]
    each_line = each_line + '\n'
    return (each_line)

def merge_kitti_classes(label_root_path, merge_label_root_path):
    """
    Merge KITTI label classes according to predefined mapping, and write results to new directory.

    - 'Truck', 'Van', 'Tram' are merged into 'Car'
    - 'Person_sitting' is merged into 'Pedestrian'
    - Ignore 'Misc' and 'DontCare' classes

    Args:
        label_root_path (str): Source directory containing KITTI label .txt files.
        merge_label_root_path (str): Destination directory to save merged label .txt files.
    """
    os.makedirs(merge_label_root_path, exist_ok=True)

    # Collect all label files
    labels_list = glob.glob(label_root_path + '*.txt')

    print('before modify categories are:\n')
    show_category(labels_list)

    for src_label_path in labels_list:
        print(src_label_path)
        merged_lines = []
        try:
            with open(src_label_path, 'r') as f:
                for each_line in f:
                    label_data = each_line.strip().split(' ')
                    if label_data[0] in ['Truck','Van','Tram']:  
                        label_data[0] = label_data[0].replace(label_data[0], 'Car')
                    if label_data[0] == 'Person_sitting':       
                        label_data[0] = label_data[0].replace(label_data[0], 'Pedestrian')
                    if label_data[0] == 'DontCare':         
                        continue
                    if label_data[0] == 'Misc': 
                        continue
                    merged_lines.append(merge(label_data))
            
            # Write merged label file to destination directory
            label_txt_name = src_label_path.replace('label_2','mergelabel_2')
            with open(label_txt_name, 'w+') as w_tdf:
                for temp in merged_lines:
                    w_tdf.write(temp)
        except IOError as ioerr:
            print('File error:' + str(ioerr))
    
    print(f"Merged KITTI labels saved to: {merge_label_root_path}")


if __name__ == '__main__':
    """
    Merge KITTI label classes according to detection task requirements.
    
    1. Directory structure:
    data_root
    │── image_2
    │   ├── 000000.png
    │   ├── 000001.png
    │   ├── 000002.png
    │   ├── 000003.png
    │   ├── 000004.png
    │   └── 000005.png
    └── label_2
    │   ├── 000000.txt
    │   ├── 000001.txt
    │   ├── 000002.txt
    │   ├── 000003.txt
    │   ├── 000004.txt
    │   └── 000005.txt

    
    2. Output structure:
    data_root
    │── mergeimage_2
    │   ├── 000000.png
    │   ├── 000001.png
    │   ├── 000002.png
    │   ├── 000003.png
    │   ├── 000004.png
    │   └── 000005.png
    └── mergelabel_2
    │   ├── 000000.txt
    │   ├── 000001.txt
    │   ├── 000002.txt
    │   ├── 000003.txt
    │   ├── 000004.txt
    │   └── 000005.txt
    """

    label_root_path = 'data_root/label_2'
    merge_label_root_path = 'data_root/mergelabel_2'
    merge_kitti_classes(label_root_path, merge_label_root_path)

    image_root_path = 'data_root/image_2'
    merge_image_root_path = 'data_root/mergeimage_2'
    copy_all_images(image_root_path, merge_image_root_path)