import json
import numpy as np
from pynput.keyboard import Controller

class GestureMapping:
    def __init__(self, mapping_file="gesture_mapping.json"):
        self.mapping_file = mapping_file
        self.keyboard = Controller()
        self.load_mappings()

    def load_mappings(self):
        try:
            with open(self.mapping_file, "r") as f:
                self.gesture_map = json.load(f)
        except FileNotFoundError:
            self.gesture_map = {}

    def save_mappings(self):
        with open(self.mapping_file, "w") as f:
            json.dump(self.gesture_map, f)

    def add_mapping(self, gesture_name, landmarks, key):
        self.gesture_map[gesture_name] = {
            "landmarks": landmarks,
            "key": key
        }
        self.save_mappings()

    def remove_mapping(self, gesture_name):
        if gesture_name in self.gesture_map:
            del self.gesture_map[gesture_name]
            self.save_mappings()

    def match_gesture(self, detected_landmarks):
        if not detected_landmarks:
            return None
        
        for gesture_name, gesture_data in self.gesture_map.items():
            stored_landmarks = gesture_data["landmarks"]
            # Calculate the Euclidean distance between the stored and detected landmarks
            if self.compare_landmarks(stored_landmarks, detected_landmarks):
                return gesture_name
        
        return None

    def compare_landmarks(self, stored_landmarks, detected_landmarks, threshold=0.05):
        stored_landmarks = np.array(stored_landmarks)
        detected_landmarks = np.array(detected_landmarks)

        if stored_landmarks.shape != detected_landmarks.shape:
            return False

        distance = np.linalg.norm(stored_landmarks - detected_landmarks)
        return distance < threshold

    def execute_mapping(self, gesture_name):
        if gesture_name and gesture_name in self.gesture_map:
            key = self.gesture_map[gesture_name]["key"]
            self.keyboard.press(key)
            self.keyboard.release(key)
