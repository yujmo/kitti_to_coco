import os
import json
import argparse
import cv2


def kitti2coco(label_dir, img_dir, output_dir, suffix):
    """
    Convert KITTI-format 2D detection labels to COCO-format JSON annotations.

    Args:
        label_dir (str): Directory containing KITTI .txt label files.
        img_dir (str): Directory containing the corresponding .png image files.
        output_json (str): Output path for the COCO-format JSON annotation file.
    """

    # Initialize the COCO annotation structure
    coco = {}
    coco['images'] = []
    coco['annotations'] = []
    coco['categories'] = []
    coco['info'] = []

    # Add info
    info = {
            "description": "KITTI 2D converted COCO format",
            "version": "1.0",
            "year": 2025
        }
    coco['info'] = info

    # Add categories
    categories = [
        {'id': 1, 'name': 'Car'},
        {'id': 2, 'name': 'Pedestrian'},
        {'id': 3, 'name': 'Cyclist'}
    ]
    coco['categories'] = categories

    # Add images and annotations
    image_id = 0
    annotation_id = 0

    # Iterate over all label files
    for file in os.listdir(label_dir):
        if file.endswith('.txt'):
            image_path = os.path.join(img_dir, file[:-4] + '.png')
            
            # Read the image to get its dimensions
            img = cv2.imread(image_path)
            if img is None:
                print(f"Warning: image not found {image_path}")
                continue

            img_height, img_width = img.shape[0], img.shape[1]
            
            image = {
                'id': image_id,
                'file_name': file[:-4] + '.png',
                'height': img_height,   # KITTI image height
                'width': img_width      # KITTI image width
            }
            coco['images'].append(image)

            # Parse the corresponding label file
            with open(os.path.join(label_dir, file), 'r') as f:
                lines = f.readlines()
                for line in lines:
                    line = line.strip().split(' ')
                    if len(parts) < 8:
                        continue  # Skip invalid lines
                    
                    # Map KITTI class name to COCO category_id
                    category_id = 1 if line[0] == 'Car' else 2 if line[0] == 'Pedestrian' else 3
                    if category_id is None:
                        continue  # Skip unknown classes
                    
                    # Extract 2D bounding box and convert to COCO format [x, y, width, height]
                    bbox = [float(coord) for coord in line[4:8]]
                    x1, y1, x2, y2 = bbox
                    bbox_width = x2 - x1
                    bbox_height = y2 - y1

                    annotation = {
                        'id': annotation_id,
                        'image_id': image_id,
                        'category_id': category_id,
                        'bbox': [x1, y1, bbox_width, bbox_height],
                        'area': bbox_height * bbox_width,
                        'iscrowd': 0
                    }
                    coco['annotations'].append(annotation)
                    annotation_id += 1

            image_id += 1

    # Save the COCO-format JSON annotation
    with open(os.path.join(output_dir, 'instances_'+ suffix + '2017' +'.json'), 'w') as f:
        json.dump(coco, f)


def main():

    '''
    Main function for converting KITTI-format labels to COCO-format annotations
    for both training and validation datasets.

    Directory Structure: 
    data_root
      ├── annotations
      ├── labels
      │    ├── train_labels
      │    └── val_labels
      ├── train2017
      └── val2017


    '''
    data_root = 'data_root/'

    outputs_path = os.path.join(data_root, 'annotations')
    os.makedirs(outputs_path, exist_ok=True)

    # Train set conversion
    train_img_dir = os.path.join(data_root, 'train2017')               
    train_label_dir = os.path.join(data_root, 'labels/train_labels')   
    kitti2coco(train_label_dir, train_img_dir, outputs_path, 'train')
    
    # Validation set conversion
    val_img_dir = os.path.join(data_root, 'val2017')
    val_label_dir = os.path.join(data_root, 'labels/val_labels') 
    kitti2coco(val_label_dir, val_img_dir, outputs_path, 'val') 

    print('KITTI to COCO conversion completed.')


if __name__ == '__main__':
    main()
