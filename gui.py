import tkinter as tk
from tkinter import simpledialog, messagebox
from gesture_recognition import GestureRecognition
from gesture_mapping import GestureMapping
import cv2
import threading

class GestureApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Gesture Recognition System")
        self.gesture_recognition = GestureRecognition()
        self.gesture_mapping = GestureMapping()
        self.is_running = False

        self.create_widgets()

    def create_widgets(self):
        tk.Button(self.root, text="Turn On Hand Gesture System", command=self.toggle_gesture_system).pack(pady=10)
        tk.Button(self.root, text="Add or Edit Gesture", command=self.add_or_edit_gesture).pack(pady=10)
        tk.Button(self.root, text="Delete Gesture", command=self.delete_gesture).pack(pady=10)
        tk.Button(self.root, text="Exit", command=self.exit_app).pack(pady=10)

    def toggle_gesture_system(self):
        self.is_running = not self.is_running
        if self.is_running:
            threading.Thread(target=self.run_gesture_system, daemon=True).start()

    def run_gesture_system(self):
        cap = cv2.VideoCapture(0)
        while self.is_running:
            ret, frame = cap.read()
            if not ret:
                break

            frame, detected_landmarks = self.gesture_recognition.detect_gesture(frame)
            matched_gesture = self.gesture_mapping.match_gesture(detected_landmarks)
            if matched_gesture:
                self.gesture_mapping.execute_mapping(matched_gesture)

            cv2.imshow("Hand Gesture Recognition", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def add_or_edit_gesture(self):
        gesture_name = simpledialog.askstring("Input", "Enter gesture name:")
        if gesture_name:
            messagebox.showinfo("Info", "Show the gesture in front of the camera for capture.")
            captured_landmarks = self.capture_gesture()
            if captured_landmarks:
                key = simpledialog.askstring("Input", "Enter key to map:")
                if key:
                    self.gesture_mapping.add_mapping(gesture_name, captured_landmarks, key)
                    messagebox.showinfo("Info", f"Gesture '{gesture_name}' mapped to key '{key}'")

    def delete_gesture(self):
        gesture_name = simpledialog.askstring("Input", "Enter gesture name to delete:")
        if gesture_name:
            self.gesture_mapping.remove_mapping(gesture_name)
            messagebox.showinfo("Info", f"Gesture '{gesture_name}' deleted")

    def capture_gesture(self):
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if not ret:
            return None

        _, landmarks = self.gesture_recognition.detect_gesture(frame)
        cap.release()
        return landmarks

    def exit_app(self):
        self.is_running = False
        self.root.quit()

    def run(self):
        self.root.mainloop()
