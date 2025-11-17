import cv2
import numpy as np
from ultralytics import YOLO
from typing import Tuple

# Load YOLOv8 model (load once at module level for efficiency)
model = YOLO("yolov8n.pt")

# Classes YOLO can detect (from COCO dataset)
VIOLENT_OBJECTS = {"knife", "gun"}
PERSON_CLASS = "person"

# Thresholds
MIN_CONF = 0.4  # Confidence for detection
MIN_RED_RATIO = 0.08  # Red pixels indicating blood


def detect_violence_in_image(image_path: str) -> Tuple[bool, str]:
    """
    Detect violence in an image using YOLO and color analysis.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Tuple of (is_violent: bool, reason: str)
        - is_violent: True if violence detected, False otherwise
        - reason: Explanation of why image was flagged
    """
    try:
        img = cv2.imread(image_path)
        
        if img is None:
            return True, "Unable to read image file"

        # Run YOLO detection
        results = model(img, verbose=False)[0]

        has_person = False
        has_weapon = False
        detected_weapons = []

        for box in results.boxes:
            cls = int(box.cls[0])
            label = results.names[cls]
            conf = float(box.conf[0])

            if conf > MIN_CONF:
                if label == PERSON_CLASS:
                    has_person = True
                if label in VIOLENT_OBJECTS:
                    has_weapon = True
                    detected_weapons.append(label)

        # Blood detection (red color ratio in image)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_red1 = np.array([0, 50, 50])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([170, 50, 50])
        upper_red2 = np.array([180, 255, 255])

        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        red_mask = mask1 + mask2

        red_pixels = np.sum(red_mask > 0)
        total_pixels = img.shape[0] * img.shape[1]
        red_ratio = red_pixels / total_pixels

        # Decision logic
        if has_weapon and has_person:
            weapons_str = ", ".join(detected_weapons)
            return True, f"Weapon detected: {weapons_str}"
        
        if red_ratio > MIN_RED_RATIO:
            return True, "Potential blood or violent content detected"
        
        return False, "Image is safe"

    except Exception as e:
        print(f"❌ Error in violence detection: {e}")
        # In case of error, reject the image to be safe
        return True, f"Error processing image: {str(e)}"