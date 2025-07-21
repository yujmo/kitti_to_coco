import os
import random
import shutil

def split_kitti_dataset(
    image_dir,
    label_dir,
    train_img_dir,
    train_label_dir,
    val_img_dir,
    val_label_dir,
    train_ratio=0.9,
    seed=42
):
    """
    Split KITTI-style image and label dataset into train/val sets by a given ratio.

    Args:
        image_dir (str): Path to source images directory.
        label_dir (str): Path to source label files directory.

        train_img_dir (str): Destination directory for training images.
        train_label_dir (str): Destination directory for training label files.
        val_img_dir (str): Destination directory for validation images.
        val_label_dir (str): Destination directory for validation label files.

        train_ratio (float): Ratio of images to use for training. Default is 0.9 (90% train, 10% val).
        seed (int): Random seed for reproducibility.
    """

    # Ensure reproducibility
    random.seed(seed)

    # Create destination folders if they don't exist
    os.makedirs(train_img_dir, exist_ok=True)
    os.makedirs(train_label_dir, exist_ok=True)
    os.makedirs(val_img_dir, exist_ok=True)
    os.makedirs(val_label_dir, exist_ok=True)

    # Collect all image file names
    all_images = os.listdir(image_dir)

    num_images = len(all_images)
    random.shuffle(all_images)

    # Calculate split index
    split_index = int(train_ratio * num_images)

    # Copy training images and labels
    for image_name in all_images[:split_index]:
        src_path = os.path.join(image_dir, image_name)
        dst_path = os.path.join(train_img_dir, image_name)
        shutil.copyfile(src_path, dst_path)

        src_label_path = os.path.join(label_dir, image_name[:-4] + '.txt')
        dst_label_path = os.path.join(train_label_dir, image_name[:-4] + '.txt')
        shutil.copyfile(src_label_path, dst_label_path)

    # Copy validation images and labels
    for image_name in all_images[split_index:]:
        src_path = os.path.join(image_dir, image_name)
        dst_path = os.path.join(val_img_dir, image_name)
        shutil.copyfile(src_path, dst_path)

        src_label_path = os.path.join(label_dir, image_name[:-4] + '.txt')
        dst_label_path = os.path.join(val_label_dir, image_name[:-4] + '.txt')
        shutil.copyfile(src_label_path, dst_label_path)
        
    print("Dataset split completed!" + "Training set size: " + str(split_index) + 'Validation set size: '+ str(num_images - split_index))

if __name__ == "__main__":
    '''
    Example usage of split_kitti_dataset for splitting a KITTI-format dataset.

    1. Directory structure:
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

    
    2. Output structure:
    data_root
    ├── labels
    │   ├── train_labels
    │   │   ├── 000000.txt
    │   │   ├── 000001.txt
    │   │   ├── 000002.txt
    │   │   ├── 000004.txt
    │   │   └── 000005.txt
    │   └── val_labels
    │       └── 000003.txt
    ├── train2017
    │   ├── 000000.png
    │   ├── 000001.png
    │   ├── 000002.png
    │   ├── 000004.png
    │   └── 000005.png
    └── val2017
        └── 000003.png
    '''

    # Source data root
    data_root = "data_root"

    # Source image/label directories
    image_dir = os.path.join(data_root + 'mergeimage_2')
    label_dir = os.path.join(data_root + 'mergelabel_2')

    # Destination directories
    dest_dir = data_root
    train_img_dir = os.path.join(dest_dir, 'train2017')
    train_label_dir = os.path.join(dest_dir, 'labels/train_labels')
    val_img_dir = os.path.join(dest_dir, 'val2017')
    val_label_dir = os.path.join(dest_dir, 'labels/val_labels')

    # Split ratio and seed
    split_kitti_dataset(
        image_dir=image_dir,
        label_dir=label_dir,
        train_img_dir=train_img_dir,
        train_label_dir=train_label_dir,
        val_img_dir=val_img_dir,
        val_label_dir=val_label_dir,
        train_ratio=0.9,
        seed=42
    )