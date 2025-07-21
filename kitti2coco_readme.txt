
# kitti2coco

Convert the [KITTI object detection dataset](http://www.cvlibs.net/datasets/kitti/eval_object.php) to the [COCO annotation format](https://mmdetection.readthedocs.io/en/latest/user_guides/train.html#coco-annotation-format) for 2D object detection tasks.

---

## Features

- Merge similar KITTI classes for simplified 2D detection (Car, Pedestrian, Cyclist).
- Split the dataset into train and validation sets with configurable ratio.
- Convert KITTI labels to COCO-compliant JSON annotation files.
- Well-documented, modular code suitable for research and practical use.

---

## COCO Annotation Format

Each annotation dictionary contains:

```python
annotation = {
    "id": int,
    "image_id": int,
    "category_id": int,
    "area": float,
    "bbox": [x, y, width, height], # (x, y): upper left corner
    "iscrowd": 0 or 1,
}
```

---

## Pipeline Overview

This repository provides **three scripts** to process the dataset step-by-step:

1. **modify_annotations_txt.py**  
   Merge similar classes in KITTI:
   - 'Van', 'Truck', 'Tram' → 'Car'
   - 'Person_sitting' → 'Pedestrian'
   - Ignore 'Misc' and 'DontCare'

2. **split_datasets.py**  
   Split images and labels into train and val sets by a specified ratio (default: 9:1).

3. **kitti2coco.py**  
   Convert train/val labels and images to COCO format and save as JSON files.

---

## Step-by-step Usage

### 1. Prepare Initial KITTI Data Structure

Organize your data as follows before any processing:

```
data_root/
├── image_2/
│   ├── 000000.png
│   ├── 000001.png
│   └── ...
└── label_2/
    ├── 000000.txt
    ├── 000001.txt
    └── ...
```

### 2. Merge KITTI Classes

Run `modify_annotations_txt.py` to merge/ignore classes and generate normalized label files:

```
python modify_annotations_txt.py
```

The result will be:

```
data_root/
├── mergeimage_2/   # all images copied from image_2
└── mergelabel_2/   # normalized/merged label files
```

### 3. Split Dataset into Train and Val

Run `split_datasets.py` to split images and labels into train/val sets:

```
python split_datasets.py
```

This creates:

```
data_root/
├── train2017/
├── val2017/
└── labels/
    ├── train_labels/
    └── val_labels/
```

### 4. Convert to COCO Format

Run `kitti2coco.py` to generate COCO-style annotation JSON files for training and validation:

```
python kitti2coco.py
```

Resulting structure:

```
data_root/
├── annotations/
│   ├── instances_train2017.json
│   └── instances_val2017.json
├── train2017/
├── val2017/
└── labels/
    ├── train_labels/
    └── val_labels/
```

---

## Example COCO Categories

```json
"categories": [
    {"id": 1, "name": "Car"},
    {"id": 2, "name": "Pedestrian"},
    {"id": 3, "name": "Cyclist"}
]
```

---

## Notes

- The whole process assumes images and labels have matching filenames (`000123.png` and `000123.txt`).
- Area calculation in COCO annotations: `area = width * height`.
- Non-target or rare KITTI classes ('Misc', 'DontCare') are ignored for standard detection.
- All scripts are Python 3.x compatible and can be adapted for other object detection datasets with similar structure.

---

## License

This project is released under the MIT License.

---

Feel free to open issues or submit PRs for improvements!
